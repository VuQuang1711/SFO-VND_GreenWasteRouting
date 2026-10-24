"""
Module Nạp và Đối chứng Dữ liệu Benchmark CVRPLIB (cvrplib_loader.py)
Đề tài: Tối ưu hóa lộ trình thu gom rác đô thị bằng thuật toán lai SFO-VND
Quy chuẩn: Step 2 - Công việc 2.3 (Chuẩn bị và khóa bộ dữ liệu Benchmark)

Chức năng:
- Đọc file .vrp chuẩn CVRPLIB bằng thư viện vrplib.read_instance.
- Đọc file nghiệm tham chiếu .sol bằng vrplib.read_solution khi file có mặt.
- Trích xuất và in đầy đủ: tên instance, dimension, capacity, demand, depot,
  kiểu khoảng cách (edge_weight_type), dạng ma trận khoảng cách.
- Tính toán lại tổng chi phí lộ trình từ file nghiệm (.sol) theo đúng ma trận
  khoảng cách và quy tắc làm tròn nguyên TSPLIB/CVRPLIB (nint), đối chiếu với BKS công bố.
"""

import os
import sys
import math
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import vrplib

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def compute_euc2d_matrix(coords: Dict[int, Tuple[float, float]], round_integers: bool = True) -> np.ndarray:
    """
    Tính ma trận khoảng cách Euclid 2 chiều theo quy ước chuẩn TSPLIB/CVRPLIB (EUC_2D).
    Quy tắc làm tròn: round(sqrt(dx*dx + dy*dy)) (nearest integer).
    """
    n = len(coords)
    matrix = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = coords[i][0] - coords[j][0]
                dy = coords[i][1] - coords[j][1]
                dist = math.sqrt(dx * dx + dy * dy)
                matrix[i, j] = round(dist) if round_integers else dist
            else:
                matrix[i, j] = 0.0
    return matrix


class CVRPLIBLoader:
    """Lớp nạp và kiểm tra dữ liệu benchmark CVRPLIB."""

    def __init__(self, raw_dir: Optional[str] = None):
        if raw_dir is None:
            # Mặc định trỏ đến data/benchmarks/raw trong repository
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.raw_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "data", "benchmarks", "raw"))
        else:
            self.raw_dir = raw_dir

    def load_instance(self, file_path_or_name: str) -> Dict[str, Any]:
        """
        Nạp instance CVRPLIB từ đường dẫn hoặc tên instance.
        Sử dụng vrplib.read_instance theo đúng yêu cầu Step 2.
        """
        if os.path.exists(file_path_or_name):
            path = file_path_or_name
        else:
            name = file_path_or_name
            if not name.endswith(".vrp"):
                name = f"{name}.vrp"
            path = os.path.join(self.raw_dir, name)

        if not os.path.exists(path):
            # Thử tìm trong thư mục cha (data/benchmarks) để đảm bảo tương thích ngược
            alt_path = os.path.join(os.path.dirname(self.raw_dir), os.path.basename(path))
            if os.path.exists(alt_path):
                path = alt_path
            else:
                raise FileNotFoundError(f"Không tìm thấy file benchmark CVRPLIB: {path}")

        instance_data = vrplib.read_instance(path)

        # Trích xuất thông số chuẩn hoá
        name = instance_data.get("name", os.path.splitext(os.path.basename(path))[0])
        dimension = int(instance_data.get("dimension", 0))
        capacity = float(instance_data.get("capacity", 0.0))
        edge_weight_type = instance_data.get("edge_weight_type", "EUC_2D")
        depot = instance_data.get("depot", [0])
        depot_idx = int(depot[0]) if isinstance(depot, (list, np.ndarray)) and len(depot) > 0 else 0

        # Toạ độ các nút
        coords_raw = instance_data.get("node_coord")
        coords: Dict[int, Tuple[float, float]] = {}
        if coords_raw is not None:
            for idx, c in enumerate(coords_raw):
                coords[idx] = (float(c[0]), float(c[1]))

        # Nhu cầu các nút
        demand_raw = instance_data.get("demand")
        demands: Dict[int, float] = {}
        if demand_raw is not None:
            for idx, d in enumerate(demand_raw):
                demands[idx] = float(d)

        # Ma trận khoảng cách
        edge_weight = instance_data.get("edge_weight")
        if edge_weight is not None:
            dist_matrix = np.array(edge_weight, dtype=float)
        elif len(coords) > 0:
            dist_matrix = compute_euc2d_matrix(coords, round_integers=True)
        else:
            dist_matrix = np.zeros((dimension, dimension), dtype=float)

        return {
            "name": name,
            "dimension": dimension,
            "num_customers": dimension - 1,
            "capacity": capacity,
            "demand": demands,
            "depot": depot_idx,
            "edge_weight_type": edge_weight_type,
            "node_coord": coords,
            "distance_matrix": dist_matrix,
            "comment": instance_data.get("comment", ""),
            "raw_keys": sorted(instance_data.keys()),
            "file_path": path
        }

    def load_solution(self, file_path_or_name: str) -> Optional[Dict[str, Any]]:
        """
        Đọc nghiệm tham khảo (.sol) bằng vrplib.read_solution khi file có mặt.
        """
        if os.path.exists(file_path_or_name):
            path = file_path_or_name
        else:
            name = file_path_or_name
            if not name.endswith(".sol"):
                name = f"{name}.sol"
            path = os.path.join(self.raw_dir, name)

        if not os.path.exists(path):
            alt_path = os.path.join(os.path.dirname(self.raw_dir), os.path.basename(path))
            if os.path.exists(alt_path):
                path = alt_path
            else:
                return None

        try:
            sol = vrplib.read_solution(path)
            return {
                "routes": sol.get("routes", []),
                "cost": sol.get("cost"),
                "file_path": path
            }
        except Exception as e:
            print(f"[CẢNH BÁO]: Không thể đọc file nghiệm {path}: {e}")
            return None

    def verify_solution_cost(
        self, instance_data: Dict[str, Any], solution_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Tính toán lại tổng độ dài các tuyến theo ma trận khoảng cách gốc và quy tắc làm tròn.
        So sánh với giá trị công bố trong .sol và giải thích sai lệch.
        """
        routes = solution_data.get("routes", [])
        dist_matrix = instance_data.get("distance_matrix")
        depot = instance_data.get("depot", 0)

        total_distance = 0.0
        route_details = []

        for r_idx, route in enumerate(routes):
            # Các node trong CVRPLIB solution có thể 1-indexed hoặc 0-indexed
            # Chuẩn VRPLIB là 1-indexed (depot là 1 hoặc được omit, khách hàng là 2..N)
            # Chuyển về 0-indexed đối chiếu với ma trận dist_matrix
            norm_route = []
            for node in route:
                idx = int(node) - 1 if min(min(r) for r in routes if len(r) > 0) >= 1 else int(node)
                norm_route.append(idx)

            # Lộ trình khép kín: Depot -> Khách hàng -> Depot
            full_cycle = [depot] + [n for n in norm_route if n != depot] + [depot]
            r_cost = 0.0
            r_demand = 0.0
            for i in range(len(full_cycle) - 1):
                u = full_cycle[i]
                v = full_cycle[i + 1]
                r_cost += dist_matrix[u, v]

            for c in norm_route:
                if c != depot:
                    r_demand += instance_data["demand"].get(c, 0.0)

            total_distance += r_cost
            route_details.append({
                "route_index": r_idx + 1,
                "nodes": norm_route,
                "cost": r_cost,
                "demand": r_demand,
                "is_capacity_valid": r_demand <= instance_data["capacity"]
            })

        published_cost = solution_data.get("cost")
        diff = None if published_cost is None else abs(total_distance - float(published_cost))

        return {
            "recalculated_cost": total_distance,
            "published_cost": published_cost,
            "difference": diff,
            "num_routes": len(routes),
            "routes": route_details,
            "is_match": (diff == 0.0) if diff is not None else False
        }


def print_instance_summary(file_path: str):
    """In tóm tắt thông số instance theo mẫu của hướng dẫn Step 2."""
    loader = CVRPLIBLoader()
    data = loader.load_instance(file_path)

    print("=" * 70)
    print(f"BÁO CÁO THÔNG SỐ INSTANCE: {data['name']}")
    print("=" * 70)
    print("Các trường đọc được:", data["raw_keys"])
    print(f"Tên instance        : {data['name']}")
    print(f"Dimension           : {data['dimension']} (Khách: {data['num_customers']}, Depot: 1)")
    print(f"Sức chứa xe Q       : {data['capacity']}")
    print(f"Vị trí Depot        : Node index {data['depot']}")
    print(f"Kiểu khoảng cách    : {data['edge_weight_type']}")
    print(f"Ma trận khoảng cách : Kích thước {data['distance_matrix'].shape}, Kiểu: {data['distance_matrix'].dtype}")
    print(f"Tổng nhu cầu rác    : {sum(data['demand'].values())} đơn vị")
    print(f"Ghi chú nguồn       : {data['comment']}")

    # Kiểm tra .sol nếu có
    sol_path = os.path.splitext(file_path)[0] + ".sol"
    if os.path.exists(sol_path):
        sol_data = loader.load_solution(sol_path)
        if sol_data:
            ver = loader.verify_solution_cost(data, sol_data)
            print("-" * 70)
            print("NGHIỆM THAM CHIẾU (.SOL):")
            print(f"  Số tuyến xe K        : {ver['num_routes']}")
            print(f"  Chi phí công bố      : {ver['published_cost']}")
            print(f"  Chi phí tính toán lại: {ver['recalculated_cost']}")
            print(f"  Sai lệch             : {ver['difference']}")
            print(f"  Khớp chuẩn BKS       : {'CHÍNH XÁC (PASS)' if ver['is_match'] else 'CÓ SAI LỆCH (CẦN GIẢI THÍCH)'}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    loader = CVRPLIBLoader()
    instances = ["E-n33-k4.vrp", "B-n50-k7.vrp", "E-n51-k5.vrp", "A-n53-k7.vrp", "A-n60-k9.vrp", "E-n76-k7.vrp"]
    print("KIỂM TRA ĐỌC BỘ BENCHMARK CVRPLIB:")
    for inst in instances:
        try:
            print_instance_summary(inst)
        except Exception as e:
            print(f"Lỗi khi đọc {inst}: {e}")
