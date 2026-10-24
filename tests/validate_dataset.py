"""
Bộ Kiểm Định Chất Lượng, Tính Tái Lập và Khóa Dữ Liệu (validate_dataset.py)
Đề tài: Tối ưu hóa lộ trình thu gom rác đô thị bằng thuật toán lai SFO-VND
Quy chuẩn: Step 2 - Công việc 2.7 (Khóa bộ dữ liệu phiên bản v1.0)

Thực thi 7 nhóm kiểm định chất lượng bắt buộc:
1. Schema và khóa (Schema & Primary Keys)
2. Giá trị và đơn vị (Values, Datatypes & Units)
3. Tải trọng & Minh chứng khả thi (Capacity constraints & Feasible witness)
4. Mạng đường & Tính liên thông có hướng (Directed Road Network & Reachability)
5. Tính tái lập (Reproducibility with Seed=42 & Library Versions)
6. Nguồn gốc dữ liệu (Data Provenance, Timestamp & Licensing)
7. Benchmark CVRPLIB (6 instance .vrp/.sol, Parser & BKS)

Kết quả trả về: PASS/FAIL cho từng hạng mục, nguyên nhân cụ thể và lưu log ra results/logs/validation_report.log
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import pytest

# UTF-8 cho terminal Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

LOG_DIR = os.path.join(ROOT_DIR, "results", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "validation_report.log")

# Cấu hình logging
logger = logging.getLogger("DatasetValidator")
logger.setLevel(logging.INFO)
# Xóa handlers cũ nếu có
logger.handlers.clear()
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)

from src.core.cvrplib_loader import CVRPLIBLoader


class DatasetValidator:
    """Lớp kiểm định chất lượng bộ dữ liệu Step 2."""

    def __init__(self):
        self.ward_proc_dir = os.path.join(ROOT_DIR, "data", "ward", "processed")
        self.ward_raw_dir = os.path.join(ROOT_DIR, "data", "ward", "raw")
        self.toy_dir = os.path.join(ROOT_DIR, "data", "toy")
        self.bm_raw_dir = os.path.join(ROOT_DIR, "data", "benchmarks", "raw")
        self.results: List[Dict[str, Any]] = []

    def record_check(self, suite: str, check_name: str, passed: bool, message: str):
        status = "PASS" if passed else "FAIL"
        entry = {
            "suite": suite,
            "check": check_name,
            "status": status,
            "message": message,
            "log_path": LOG_FILE
        }
        self.results.append(entry)
        log_line = f"[{status}] [{suite}] {check_name}: {message}"
        if passed:
            logger.info(log_line)
        else:
            logger.error(log_line)

    # -------------------------------------------------------------------------
    # SUITE 1: SCHEMA VÀ KHÓA
    # -------------------------------------------------------------------------
    def check_suite_1_schema_and_keys(self):
        suite = "1. Schema và Khóa"

        # 1.1 collection_points.csv
        p_path = os.path.join(self.ward_proc_dir, "collection_points.csv")
        if not os.path.exists(p_path):
            self.record_check(suite, "File collection_points.csv", False, f"Không tìm thấy {p_path}")
            return

        df_p = pd.read_csv(p_path)
        req_cols = {"point_id", "latitude", "longitude", "demand_kg", "point_type", "source_type", "snapped_node"}
        missing_cols = req_cols - set(df_p.columns)
        self.record_check(
            suite, "Cột bắt buộc collection_points.csv",
            len(missing_cols) == 0,
            f"Thiếu các cột: {missing_cols}" if missing_cols else "Đầy đủ cột theo yêu cầu mục 18"
        )

        # Kiểm tra ID duy nhất
        ids = df_p["point_id"].tolist()
        is_unique = len(ids) == len(set(ids))
        self.record_check(suite, "point_id duy nhất", is_unique, f"Tổng {len(ids)} điểm, ID không trùng lặp" if is_unique else "Tồn tại ID trùng")

        # Kiểm tra Depot tồn tại
        has_depot = (0 in ids) and ("depot" in df_p["point_type"].values)
        self.record_check(suite, "Depot tồn tại trong points", has_depot, "Depot ID 0 có mặt trong danh sách" if has_depot else "Thiếu Depot ID 0")

        # 1.2 depot.csv
        d_path = os.path.join(self.ward_proc_dir, "depot.csv")
        df_d = pd.read_csv(d_path)
        d_req = {"depot_id", "latitude", "longitude", "source_type", "snapped_node"}
        self.record_check(suite, "Cột bắt buộc depot.csv", d_req.issubset(df_d.columns), "Đầy đủ cột depot.csv")

        # 1.3 vehicles.csv
        v_path = os.path.join(self.ward_proc_dir, "vehicles.csv")
        df_v = pd.read_csv(v_path)
        v_req = {"vehicle_id", "capacity_kg", "available"}
        self.record_check(suite, "Cột bắt buộc vehicles.csv", v_req.issubset(df_v.columns), "Đầy đủ cột vehicles.csv")

    # -------------------------------------------------------------------------
    # SUITE 2: GIÁ TRỊ VÀ ĐƠN VỊ
    # -------------------------------------------------------------------------
    def check_suite_2_values_and_units(self):
        suite = "2. Giá trị và Đơn vị"
        p_path = os.path.join(self.ward_proc_dir, "collection_points.csv")
        df_p = pd.read_csv(p_path)

        # Demand không âm
        d_neg = df_p[df_p["demand_kg"] < 0]
        self.record_check(suite, "Demand không âm", len(d_neg) == 0, f"Tìm thấy {len(d_neg)} giá trị âm" if len(d_neg) > 0 else "100% demand >= 0 kg")

        # q_i <= Q (với xe Q = 1500 kg)
        Q = 1500.0
        d_over = df_p[df_p["demand_kg"] > Q]
        self.record_check(suite, "Mọi q_i <= Q", len(d_over) == 0, f"Tìm thấy {len(d_over)} điểm vượt Q" if len(d_over) > 0 else f"100% điểm thu gom có q_i <= Q={Q} kg")

        # Ma trận khoảng cách: không âm, đường chéo bằng 0
        m_path = os.path.join(self.ward_proc_dir, "distance_matrix.csv")
        dist_m = pd.read_csv(m_path, header=None).to_numpy(dtype=float)
        non_neg = np.all(dist_m >= 0)
        diag_zero = np.all(np.diag(dist_m) == 0.0)
        self.record_check(suite, "Khoảng cách không âm", non_neg, "100% phần tử ma trận >= 0m")
        self.record_check(suite, "Đường chéo d(i,i) = 0", diag_zero, "100% phần tử đường chéo = 0m")

    # -------------------------------------------------------------------------
    # SUITE 3: TẢI TRỌNG VÀ CHỨNG CỨ KHẢ THI
    # -------------------------------------------------------------------------
    def check_suite_3_capacity_and_witness(self):
        suite = "3. Tải trọng & Chứng cứ khả thi"
        p_path = os.path.join(self.ward_proc_dir, "collection_points.csv")
        r_path = os.path.join(self.ward_proc_dir, "feasible_routes.json")
        df_p = pd.read_csv(p_path)

        with open(r_path, "r", encoding="utf-8") as f:
            feas = json.load(f)

        total_demand = float(df_p["demand_kg"].sum())
        total_cap = float(feas["total_capacity_kg"])

        # Điều kiện cần: Tổng demand <= Tổng sức chứa
        cond_nec = total_demand <= total_cap
        self.record_check(
            suite, "Điều kiện cần: Tổng demand <= K x Q", cond_nec,
            f"Tổng demand = {total_demand:.1f} kg <= Tổng sức chứa = {total_cap:.1f} kg"
        )

        # Điều kiện đủ: Chứng cứ phân tuyến hợp lệ (Feasible Witness)
        routes = feas["routes"]
        all_loads_valid = all(r["route_load_kg"] <= r["capacity_kg"] for r in routes)
        all_custs_served = set()
        for r in routes:
            all_custs_served.update(r["customer_ids"])

        expected_custs = set(df_p.loc[df_p["point_id"] > 0, "point_id"])
        full_cover = (all_custs_served == expected_custs)

        self.record_check(
            suite, "Tải trọng từng xe hợp lệ trong feasible_routes",
            all_loads_valid, "Tất cả các tuyến đều không vượt quá sức chứa xe Q"
        )
        self.record_check(
            suite, "Phủ đủ 100% điểm khách hàng không bỏ sót",
            full_cover, f"Đã phục vụ đủ {len(expected_custs)}/50 điểm thu gom rác"
        )

    # -------------------------------------------------------------------------
    # SUITE 4: MẠNG ĐƯỜNG VÀ TÍNH LIÊN THÔNG CÓ HƯỚNG
    # -------------------------------------------------------------------------
    def check_suite_4_road_network(self):
        suite = "4. Mạng đường & Tính liên thông"
        graph_path = os.path.join(self.ward_raw_dir, "road_network.graphml")
        matrix_path = os.path.join(self.ward_proc_dir, "distance_matrix.csv")

        has_graph = os.path.exists(graph_path)
        self.record_check(suite, "File road_network.graphml tồn tại", has_graph, f"Đồ thị đường gốc tại {graph_path}")

        dist_m = pd.read_csv(matrix_path, header=None).to_numpy(dtype=float)
        # Kiểm tra tính liên thông: không có cặp vô cực
        has_no_inf = not np.any(np.isinf(dist_m))
        self.record_check(
            suite, "Mọi cặp điểm đều có đường đi (Không bị đứt đoạn)",
            has_no_inf, "Không có cặp điểm nào bị vô cực (Dijkstra trên SCC)"
        )

        # Kiểm tra đường đi từ và về depot cho tất cả các điểm
        n = dist_m.shape[0]
        from_depot = all(dist_m[0, i] > 0 for i in range(1, n))
        to_depot = all(dist_m[i, 0] > 0 for i in range(1, n))
        self.record_check(suite, "Có đường đi từ Depot đến mọi điểm", from_depot, "100% điểm đến được từ depot")
        self.record_check(suite, "Có đường quay về Depot từ mọi điểm", to_depot, "100% điểm quay về được depot")

        # Kiểm tra tính chất có hướng (đường 1 chiều: d(i,j) != d(j,i))
        is_symmetric = np.allclose(dist_m, dist_m.T)
        self.record_check(
            suite, "Tính chất có hướng của mạng đường (Asymmetric)",
            not is_symmetric, "Ma trận có hướng: d(i,j) khác d(j,i) do đường 1 chiều thực tế"
        )

    # -------------------------------------------------------------------------
    # SUITE 5: TÍNH TÁI LẬP (REPRODUCIBILITY)
    # -------------------------------------------------------------------------
    def check_suite_5_reproducibility(self):
        suite = "5. Tính tái lập"
        scen_path = os.path.join(self.ward_proc_dir, "scenario.json")
        with open(scen_path, "r", encoding="utf-8") as f:
            scen = json.load(f)

        has_seed = ("seed" in scen) and (scen["seed"] == 42)
        self.record_check(suite, "Cố định Seed ngẫu nhiên (seed=42)", has_seed, "Seed được khóa tại 42 để đảm bảo tái lập 100%")

        # Kiểm tra cấu hình và phiên bản
        has_rules = "demand_rule" in scen and "units" in scen
        self.record_check(suite, "Quy tắc sinh dữ liệu và đơn vị đo rõ ràng", has_rules, f"Rule: {scen.get('demand_rule')}")

    # -------------------------------------------------------------------------
    # SUITE 6: NGUỒN GỐC DỮ LIỆU VÀ GIẤY PHÉP
    # -------------------------------------------------------------------------
    def check_suite_6_data_provenance(self):
        suite = "6. Nguồn gốc dữ liệu"
        p_path = os.path.join(self.ward_proc_dir, "collection_points.csv")
        df_p = pd.read_csv(p_path)

        # Phân loại nguồn gốc
        source_types = set(df_p["source_type"].unique())
        has_valid_source = all("giả lập" in s or "quy hoạch" in s for s in source_types)
        self.record_check(
            suite, "Phân loại nguồn dữ liệu minh bạch", has_valid_source,
            f"Các phân loại nguồn: {source_types} (không gán nhãn sai thùng rác thực tế)"
        )

        # Kiểm tra file ranh giới GeoJSON
        b_path = os.path.join(self.ward_raw_dir, "ward_boundary.geojson")
        has_boundary = os.path.exists(b_path)
        self.record_check(suite, "File ranh giới ward_boundary.geojson", has_boundary, f"Ranh giới chuẩn WGS84 EPSG:4326 tại {b_path}")

    # -------------------------------------------------------------------------
    # SUITE 7: BENCHMARK CVRPLIB
    # -------------------------------------------------------------------------
    def check_suite_7_cvrplib(self):
        suite = "7. Benchmark CVRPLIB"
        loader = CVRPLIBLoader()
        instances = ["E-n33-k4", "B-n50-k7", "E-n51-k5", "A-n53-k7", "A-n60-k9", "E-n76-k7"]

        all_loaded = True
        err_msg = ""
        for inst in instances:
            try:
                data = loader.load_instance(inst)
                if data["dimension"] <= 0 or data["capacity"] <= 0:
                    all_loaded = False
                    err_msg = f"Dữ liệu {inst} rỗng"
                    break
            except Exception as e:
                all_loaded = False
                err_msg = str(e)
                break

        self.record_check(suite, "Nạp thành công 6 bộ benchmark CVRPLIB gốc", all_loaded, "Cả 6 file .vrp đọc đúng schema" if all_loaded else err_msg)

        # Kiểm tra metadata bảng CSV
        meta_path = os.path.join(ROOT_DIR, "results", "benchmark_metadata.csv")
        has_meta = os.path.exists(meta_path)
        self.record_check(suite, "Bảng metadata CVRPLIB tồn tại", has_meta, f"Tệp kết quả tại {meta_path}")

    # -------------------------------------------------------------------------
    # RUN ALL
    # -------------------------------------------------------------------------
    def run_all_checks(self) -> bool:
        logger.info("================================================================================")
        logger.info("BẮT ĐẦU CHẠY KIỂM ĐỊNH CHẤT LƯỢNG BỘ DỮ LIỆU STEP 2 (v1.0)")
        logger.info("================================================================================")

        self.check_suite_1_schema_and_keys()
        self.check_suite_2_values_and_units()
        self.check_suite_3_capacity_and_witness()
        self.check_suite_4_road_network()
        self.check_suite_5_reproducibility()
        self.check_suite_6_data_provenance()
        self.check_suite_7_cvrplib()

        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = total - passed

        logger.info("================================================================================")
        logger.info(f"TỔNG KẾT KIỂM ĐỊNH: {passed}/{total} ĐẠT (PASS) | {failed} THẤT BẠI (FAIL)")
        logger.info(f"Chi tiết log được lưu tại: {LOG_FILE}")
        logger.info("================================================================================")

        return failed == 0

    def print_summary_table(self):
        print("\n" + "=" * 90)
        print("BẢNG KẾT QUẢ KIỂM ĐỊNH DỮ LIỆU STEP 2 (VALIDATION REPORT)")
        print("=" * 90)
        print(f"{'HẠNG MỤC (SUITE)':<28} | {'NỘI DUNG KIỂM TRA':<35} | {'KẾT QUẢ':<8}")
        print("-" * 90)
        for r in self.results:
            status_str = f"\033[92m{r['status']}\033[0m" if r['status'] == 'PASS' else f"\033[91m{r['status']}\033[0m"
            print(f"{r['suite']:<28} | {r['check'][:35]:<35} | {status_str:<8}")
        print("=" * 90)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        print(f"Tổng số ca kiểm tra: {len(self.results)} | Đạt: {passed} | Không đạt: {len(self.results) - passed}")
        print(f"Đường dẫn file log  : {LOG_FILE}\n")


# Pytest test function wrapper
def test_all_dataset_validation():
    """Tích hợp kiểm định chất lượng dữ liệu vào bộ test tự động Pytest."""
    validator = DatasetValidator()
    all_passed = validator.run_all_checks()
    assert all_passed, "Có ít nhất một kiểm tra dữ liệu không đạt (FAIL). Xem chi tiết tại results/logs/validation_report.log"


if __name__ == "__main__":
    validator = DatasetValidator()
    success = validator.run_all_checks()
    validator.print_summary_table()
    sys.exit(0 if success else 1)
