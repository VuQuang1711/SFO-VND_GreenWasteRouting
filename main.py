"""
Điểm Khởi Chạy Hệ Thống Toàn Cục (Main Pipeline Orchestrator)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Điều phối toàn bộ luồng từ Nạp dữ liệu -> Giải thuật -> Đánh giá đối chứng -> Xuất bản đồ -> Khởi chạy Web

Tham chiếu kiến trúc:
- Universal XAI & 3-Tier Blueprint (Presentation Layer - main.py điều phối toàn bộ luồng)
- Coding Style: 100% Tiếng Việt cho chú thích, câu lệnh in terminal và thông báo lỗi.
"""

import os
import sys
import time
import argparse
from typing import Dict, Any

# Đảm bảo import được các module trong gói src dù chạy từ thư mục gốc hay thư mục Source/
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Thiết lập bảng mã UTF-8 cho terminal Windows để tránh lỗi font tiếng Việt
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.config import (
    CAPACITY_Q_MAX,
    DEPOT_INDEX,
    DEFAULT_MAX_ITERATIONS,
    DEFAULT_NUMBER_OF_SARDINES,
    DEFAULT_PERCENTAGE_OF_POPULATION,
    DEFAULT_INITIAL_ATTACK_POWER,
    DEFAULT_ATTACK_POWER_EPSILON
)
from src.core.data_loader import DataLoader
from src.core.decoder import RouteDecoder
from src.core.evaluator import RouteEvaluator
from src.core.validator import RouteValidator
from src.algorithms.sfo import SailfishOptimizer
from src.algorithms.vnd import VariableNeighborhoodDescent
from src.algorithms.hybrid_sfo_vnd import HybridSFOVND
from src.baselines.greedy import GreedyNearestNeighbor
from src.map.route_mapper import RouteMapper


def print_banner():
    """In biểu ngữ giới thiệu đồ án."""
    banner = """
========================================================================================
   🚛 GREENWASTE ROUTE AI - HỆ THỐNG TỐI ƯU HÓA TUYẾN THU GOM RÁC ĐÔ THỊ XANH
   Đề tài NCKH Sinh viên: Hybrid SFO-VND (Sailfish Optimizer + Variable Neighborhood Descent)
   Địa bàn thử nghiệm: Phường Sơn Kỳ, Quận Tân Phú, TP. Hồ Chí Minh
========================================================================================
    """
    print(banner)


def run_pipeline(
    dataset_type: str = "case_study",
    iterations: int = 50,
    num_sardines: int = 30,
    vnd_interval: int = 3,
    capacity: float = CAPACITY_Q_MAX,
    seed: int = 42,
    export_map: bool = True
) -> Dict[str, Any]:
    """
    Thực thi luồng tính toán toàn diện:
    1. Tải và tiền xử lý dữ liệu.
    2. Chạy phương án Before: Greedy Nearest Neighbor (Kinh nghiệm thực tế).
    3. Chạy phương án đối chứng: SFO thuần (Khám phá toàn cục).
    4. Chạy phương án After: Hybrid SFO-VND (Đề xuất tối ưu xanh).
    5. In bảng so sánh đối chứng khoa học và xuất bản đồ HTML.
    """
    data_loader = DataLoader(depot_index=DEPOT_INDEX)

    # 1. NẠP DỮ LIỆU
    print("\n[BƯỚC 1/4] Đang nạp và kiểm tra tính toàn vẹn của dữ liệu...")
    if dataset_type == "case_study":
        points_path = os.path.join(current_dir, "data", "case_study", "collection_points.csv")
        matrix_path = os.path.join(current_dir, "data", "case_study", "distance_matrix.csv")

        if not os.path.exists(points_path):
            raise FileNotFoundError(f"Lỗi: Không tìm thấy file dữ liệu {points_path}")

        data = data_loader.load_case_study(points_path, matrix_path)
        is_benchmark = False
        print(f" -> Đã nạp thành công dữ liệu Case Study Phường Sơn Kỳ với {data['dimension']} điểm thu gom rác.")
    else:
        vrp_path = os.path.join(current_dir, "data", "benchmarks", "E-n33-k4.vrp")
        if not os.path.exists(vrp_path):
            raise FileNotFoundError(f"Lỗi: Không tìm thấy file benchmark {vrp_path}")

        data = data_loader.load_cvrplib_instance(vrp_path)
        capacity = data["capacity_q_max"]
        is_benchmark = True
        print(f" -> Đã nạp thành công bộ dữ liệu Benchmark quốc tế {data['name']} (Sức chứa Q={capacity}).")

    # Khởi tạo các thành phần hạt nhân
    decoder = RouteDecoder(capacity_q_max=capacity, depot_index=DEPOT_INDEX)
    evaluator = RouteEvaluator(
        distance_matrix=data["distance_matrix"],
        demands=data["demands"],
        capacity_q_max=capacity,
        depot_index=DEPOT_INDEX,
        benchmark_mode=is_benchmark
    )
    validator = RouteValidator(capacity_q_max=capacity, depot_index=DEPOT_INDEX)

    total_customers = data["dimension"]

    # 2. CHẠY THUẬT TOÁN THAM ĂN (BEFORE - BASELINE)
    print("\n[BƯỚC 2/4] Đang tính toán phương án cơ sở Before (Thuật toán Tham ăn Nearest Neighbor)...")
    greedy = GreedyNearestNeighbor(evaluator=evaluator, capacity_q_max=capacity)
    t0 = time.time()
    res_greedy = greedy.solve(total_customers)
    time_greedy = time.time() - t0
    res_greedy["runtime"] = time_greedy
    print(f" -> Hoàn tất trong {time_greedy:.3f}s. Tổng quãng đường: {res_greedy['total_distance_km']:.2f} km.")

    # 3. CHẠY SFO THUẦN
    print("\n[BƯỚC 3/4] Đang chạy thuật toán Sailfish Optimizer (SFO thuần) để tìm kiếm toàn cục...")
    sfo = SailfishOptimizer(
        evaluator=evaluator,
        decoder=decoder,
        dimension=total_customers,
        number_of_sardines=num_sardines,
        max_iterations=iterations,
        random_seed=seed
    )
    t0 = time.time()
    res_sfo = sfo.optimize()
    time_sfo = time.time() - t0
    print(f" -> Hoàn tất trong {time_sfo:.3f}s. Điểm Fitness tốt nhất: {res_sfo['best_fitness']:.2f}.")

    # 4. CHẠY HYBRID SFO-VND (AFTER - ĐỀ XUẤT)
    print("\n[BƯỚC 4/4] Đang thực thi thuật toán lai đề xuất Hybrid SFO-VND (Có cơ chế Re-encoding)...")
    hybrid = HybridSFOVND(
        evaluator=evaluator,
        decoder=decoder,
        dimension=total_customers,
        number_of_sardines=num_sardines,
        max_iterations=iterations,
        vnd_trigger_interval=vnd_interval,
        random_seed=seed
    )
    t0 = time.time()
    res_hybrid = hybrid.optimize()
    time_hybrid = time.time() - t0
    print(f" -> Hoàn tất trong {time_hybrid:.3f}s. Điểm Fitness tối ưu: {res_hybrid['best_fitness']:.2f}.")

    # Kiểm tra tính hợp lệ của nghiệm lai
    is_valid, viol_cnt, msgs = validator.validate_solution(
        routes=res_hybrid["best_routes"],
        demands=data["demands"],
        total_customers=total_customers,
        capacity_q_max=capacity
    )

    # 5. IN BẢNG SO SÁNH ĐỐI CHỨNG (GREEN IMPACT COMPARISON TABLE)
    g_dist = res_greedy["total_distance_km"]
    h_dist = res_hybrid["metrics"]["total_distance_km"]
    dist_diff = (g_dist - h_dist) / g_dist * 100.0 if g_dist > 0 else 0.0

    g_fuel = res_greedy["total_fuel_liters"]
    h_fuel = res_hybrid["metrics"]["total_fuel_liters"]
    fuel_diff = (g_fuel - h_fuel) / g_fuel * 100.0 if g_fuel > 0 else 0.0

    g_co2 = res_greedy["total_co2_kg"]
    h_co2 = res_hybrid["metrics"]["total_co2_kg"]
    co2_diff = (g_co2 - h_co2) / g_co2 * 100.0 if g_co2 > 0 else 0.0

    g_cost = res_greedy["fuel_cost_vnd"]
    h_cost = res_hybrid["metrics"]["fuel_cost_vnd"]
    cost_diff = (g_cost - h_cost) / g_cost * 100.0 if g_cost > 0 else 0.0

    g_cost_str = f"{g_cost:,.0f} đ"
    h_cost_str = f"{h_cost:,.0f} đ"
    g_veh_str = f"{res_greedy['metrics']['active_vehicles']} xe"
    h_veh_str = f"{res_hybrid['metrics']['active_vehicles']} xe"
    g_util_str = f"{res_greedy['metrics']['capacity_utilization_pct']:.1f}%"
    h_util_str = f"{res_hybrid['metrics']['capacity_utilization_pct']:.1f}%"
    g_time_str = f"{time_greedy:.3f} s"
    h_time_str = f"{time_hybrid:.2f} s"
    g_valid_str = "100% HỢP LỆ" if res_greedy['is_valid'] else "VI PHẠM"
    h_valid_str = "100% HỢP LỆ" if is_valid else "VI PHẠM"

    print("\n" + "=" * 92)
    print("                      BÁO CÁO KẾT QUẢ ĐỐI CHỨNG (GREEN IMPACT REPORT)")
    print("=" * 92)
    print(f"{'Chỉ số đánh giá':<38} | {'Before (Greedy)':<16} | {'After (SFO-VND)':<16} | {'Hiệu quả cải thiện':<14}")
    print("-" * 92)
    print(f"{'Tổng quãng đường di chuyển (km)':<38} | {g_dist:<16.2f} | {h_dist:<16.2f} | {f'Giảm {dist_diff:.2f}%':<14}")
    print(f"{'Lượng dầu Diesel tiêu thụ (Lít)':<38} | {g_fuel:<16.2f} | {h_fuel:<16.2f} | {f'Tiết kiệm {fuel_diff:.2f}%':<14}")
    print(f"{'Lượng phát thải CO2 (ISO 14064 - kg)':<38} | {g_co2:<16.2f} | {h_co2:<16.2f} | {f'Cắt giảm {co2_diff:.2f}%':<14}")
    print(f"{'Chi phí nhiên liệu vận hành (VNĐ)':<38} | {g_cost_str:<16} | {h_cost_str:<16} | {f'Tiết kiệm {cost_diff:.2f}%':<14}")
    print(f"{'Số lượng xe kích hoạt':<38} | {g_veh_str:<16} | {h_veh_str:<16} | {'-':<14}")
    print(f"{'Hệ số lấp đầy tải trọng bình quân':<38} | {g_util_str:<16} | {h_util_str:<16} | {'-':<14}")
    print(f"{'Thời gian tính toán CPU (giây)':<38} | {g_time_str:<16} | {h_time_str:<16} | {'-':<14}")
    print(f"{'Tính hợp lệ 4 ràng buộc cứng':<38} | {g_valid_str:<16} | {h_valid_str:<16} | {'-':<14}")
    print("=" * 92)

    # 6. IN SƠ ĐỒ LỘ TRÌNH CHI TIẾT TỪNG XE (HUMAN-READABLE ROUTE BREAKDOWN)
    print("\n" + "=" * 92)
    print("               SƠ ĐỒ HÀNH TRÌNH CHI TIẾT TỪNG XE (KẾT QUẢ TỐI ƯU SFO-VND)")
    print("=" * 92)

    points_dict = {}
    if "points_df" in data:
        for _, row in data["points_df"].iterrows():
            points_dict[int(row["point_id"])] = {
                "name": str(row["name"]),
                "demand": float(row["demand"]),
                "node_type": str(row.get("node_type", "Dân cư"))
            }

    color_names = ["Đỏ", "Xanh dương", "Xanh ngọc", "Cam đất", "Tím", "Đỏ cam", "Xanh lam"]
    active_idx = 0
    for r_idx, r in enumerate(res_hybrid["best_routes"]):
        pts = [p for p in r if p != 0]
        if not pts:
            continue
        active_idx += 1
        load = sum(data["demands"].get(p, 0.0) for p in pts)
        util = (load / capacity) * 100.0
        color_label = color_names[(active_idx - 1) % len(color_names)]

        print(f"\n🚚 XE THU GOM #{active_idx} (Màu {color_label}) | Tải gom: {load:,.1f} / {capacity:,.0f} kg ({util:.1f}%) | Phục vụ {len(pts)} điểm:")
        depot_title = points_dict.get(0, {}).get("name", "Trạm tập kết rác Sơn Kỳ") if points_dict else "Depot 0"
        print(f"   [Bắt đầu] 🏁 {depot_title}")

        for step, p in enumerate(pts, 1):
            if points_dict and p in points_dict:
                p_info = points_dict[p]
                print(f"      └──► Điểm #{step:02d}: {p_info['name']} (Gom: {p_info['demand']:.0f} kg - {p_info['node_type']})")
            else:
                dmd = data["demands"].get(p, 0.0)
                print(f"      └──► Điểm #{step:02d}: Điểm số {p} (Gom: {dmd:.0f} kg)")

        print(f"   [Kết thúc] 🏁 Quay về {depot_title} (Xả rác hoàn tất tuyến)")

    print("\n" + "=" * 92)

    # 7. XUẤT BẢN ĐỒ TƯƠNG TÁC HTML NẾU CÓ DỮ LIỆU TỌA ĐỘ
    if export_map and dataset_type == "case_study":
        print("\n[BẢN ĐỒ] Đang xuất bản đồ lộ trình đa màu HTML...")
        points_df = data["points_df"]
        points_info = {}
        for _, row in points_df.iterrows():
            pid = int(row["point_id"])
            points_info[pid] = {
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "demand": float(row["demand"]),
                "name": str(row["name"]),
                "node_type": str(row.get("node_type", "Dân cư"))
            }

        depot_coords = (points_info[0]["lat"], points_info[0]["lon"])
        mapper = RouteMapper(depot_coords=depot_coords, zoom_start=15)
        output_map = os.path.join(current_dir, "green_waste_routing_map.html")
        mapper.generate_map(res_hybrid["best_routes"], points_info, output_map)
        print(f" -> Bạn có thể mở trực tiếp file '{output_map}' trên trình duyệt để xem lộ trình từng xe!")

    # Giải phóng tài nguyên sau khi hoàn tất
    sfo.shutdown_resources()
    hybrid.shutdown_resources()

    return {
        "greedy": res_greedy,
        "sfo": res_sfo,
        "hybrid": res_hybrid
    }


def main():
    """Hàm phân tích đối số dòng lệnh và khởi chạy ứng dụng."""
    print_banner()

    parser = argparse.ArgumentParser(
        description="GreenWaste Route AI - Bộ điều phối thuật toán lai SFO-VND cho bài toán Green VRP"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="case_study",
        choices=["case_study", "benchmark"],
        help="Loại dữ liệu thử nghiệm: 'case_study' (Phường Sơn Kỳ) hoặc 'benchmark' (CVRPLIB E-n33-k4)."
    )
    parser.add_argument(
        "--iter",
        type=int,
        default=30,
        help="Số lượng thế hệ vòng lặp tối đa (mặc định: 30 vòng)."
    )
    parser.add_argument(
        "--sardines",
        type=int,
        default=30,
        help="Số lượng cá mòi trong quần thể SFO (mặc định: 30)."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=3,
        help="Chu kỳ kích hoạt VND tinh chỉnh sâu (mặc định: 3 vòng/lần)."
    )
    parser.add_argument(
        "--capacity",
        type=float,
        default=CAPACITY_Q_MAX,
        help=f"Tải trọng tối đa của xe thu gom rác (kg, mặc định: {CAPACITY_Q_MAX})."
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Hạt giống ngẫu nhiên cố định để đảm bảo so sánh công bằng (mặc định: 42)."
    )
    parser.add_argument(
        "--no-map",
        action="store_true",
        help="Tắt chế độ tự động xuất bản đồ tương tác HTML."
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Khởi chạy giao diện Web Streamlit Dashboard."
    )

    args = parser.parse_args()

    if args.web:
        print("\n[STREAMLIT] Đang khởi chạy máy chủ giao diện Web...")
        app_path = os.path.join(current_dir, "web", "app.py")
        python_exe = sys.executable
        # Lệnh chạy Streamlit thông qua module python
        cmd = f'"{python_exe}" -m streamlit run "{app_path}"'
        print(f"Lệnh thực thi: {cmd}")
        os.system(cmd)
    else:
        run_pipeline(
            dataset_type=args.dataset,
            iterations=args.iter,
            num_sardines=args.sardines,
            vnd_interval=args.interval,
            capacity=args.capacity,
            seed=args.seed,
            export_map=not args.no_map
        )


if __name__ == "__main__":
    main()
