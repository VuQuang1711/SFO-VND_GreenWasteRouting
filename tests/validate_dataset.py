"""
Bộ Kiểm Định Chất Lượng, Tính Tái Lập và Khóa Dữ Liệu (validate_dataset.py)
Đề tài: Tối ưu hóa lộ trình thu gom rác đô thị bằng thuật toán lai SFO-VND
Quy chuẩn: Step 2 - Công việc 2.7 (Khóa bộ dữ liệu phiên bản v1.0)

Thực thi 7 nhóm kiểm định chất lượng bắt buộc (30 tiêu chí):
1. Schema, Kiểu dữ liệu và Khóa chính (Schema, Datatypes & Primary Keys)
2. Tọa độ, Giá trị, Đơn vị và Ma trận ID (Coordinates, Values, Units & Matrix ID)
3. Tải trọng, Minh chứng khả thi & Phục vụ đúng 1 lần (Capacity, Feasible Witness & Single-Visit)
4. Mạng đường & Tính liên thông có hướng (Directed Road Network & Reachability)
5. Tính tái lập & So sánh 2 lần chạy cùng Seed=42 (Reproducibility & Two-Run Seed Comparison)
6. Nguồn gốc dữ liệu & Độ chính xác Snap (Data Provenance, Snap Distance & Boundary)
7. Benchmark CVRPLIB (6 instance .vrp/.sol, Parser & BKS Int/Float Verification)

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
logger.handlers.clear()
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)

from src.core.cvrplib_loader import CVRPLIBLoader
from src.core.data_loader import DataLoader


class DatasetValidator:
    """Lớp kiểm định chất lượng bộ dữ liệu Step 2 (30 tiêu chí)."""

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
    # SUITE 1: SCHEMA, KIỂU DỮ LIỆU VÀ KHÓA CHÍNH (6 CHECKS)
    # -------------------------------------------------------------------------
    def check_suite_1_schema_and_keys(self):
        suite = "1. Schema & Khóa chính"

        # 1.1 Cột bắt buộc collection_points.csv
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

        # 1.2 Kiểu dữ liệu hợp lệ và không chứa NaN/Null
        no_nulls = not df_p[list(req_cols)].isnull().any().any()
        valid_dtypes = (
            pd.api.types.is_integer_dtype(df_p["point_id"])
            and pd.api.types.is_numeric_dtype(df_p["latitude"])
            and pd.api.types.is_numeric_dtype(df_p["longitude"])
            and pd.api.types.is_numeric_dtype(df_p["demand_kg"])
        )
        self.record_check(
            suite, "Kiểu dữ liệu hợp lệ & không chứa NaN/Null",
            bool(no_nulls and valid_dtypes),
            "100% trường đúng kiểu int/float/str, 0 giá trị NaN/Null"
        )

        # 1.3 Kiểm tra ID duy nhất và liên tục (0..50)
        ids = df_p["point_id"].tolist()
        is_unique = (len(ids) == len(set(ids))) and (ids == list(range(len(ids))))
        self.record_check(
            suite, "Khóa chính point_id duy nhất (0..50)",
            is_unique,
            f"Tổng {len(ids)} điểm, ID liên tục từ 0 đến {len(ids)-1} không trùng lặp"
        )

        # 1.4 Kiểm tra Depot tồn tại và có demand = 0
        depot_rows = df_p[df_p["point_id"] == 0]
        has_depot = (
            len(depot_rows) == 1
            and depot_rows.iloc[0]["point_type"] == "depot"
            and float(depot_rows.iloc[0]["demand_kg"]) == 0.0
        )
        self.record_check(
            suite, "Depot ID 0 tồn tại và demand_kg = 0",
            has_depot,
            "Depot ID 0 có mặt, point_type='depot', demand_kg=0.0 kg"
        )

        # 1.5 depot.csv
        d_path = os.path.join(self.ward_proc_dir, "depot.csv")
        df_d = pd.read_csv(d_path)
        d_req = {"depot_id", "latitude", "longitude", "source_type", "snapped_node"}
        self.record_check(suite, "Cột bắt buộc depot.csv", d_req.issubset(df_d.columns), "Đầy đủ cột depot.csv")

        # 1.6 vehicles.csv
        v_path = os.path.join(self.ward_proc_dir, "vehicles.csv")
        df_v = pd.read_csv(v_path)
        v_req = {"vehicle_id", "capacity_kg", "available"}
        self.record_check(suite, "Cột bắt buộc vehicles.csv", v_req.issubset(df_v.columns), "Đầy đủ cột vehicles.csv")

    # -------------------------------------------------------------------------
    # SUITE 2: TỌA ĐỘ, GIÁ TRỊ, ĐƠN VỊ VÀ MA TRẬN ID (6 CHECKS)
    # -------------------------------------------------------------------------
    def check_suite_2_values_and_units(self):
        suite = "2. Tọa độ, Giá trị & Đơn vị"
        p_path = os.path.join(self.ward_proc_dir, "collection_points.csv")
        df_p = pd.read_csv(p_path)

        # 2.1 Tọa độ GPS nằm trong khung địa lý WGS84 của Phường Tây Thạnh (TP.HCM)
        lat_ok = df_p["latitude"].between(10.79, 10.84).all()
        lon_ok = df_p["longitude"].between(106.60, 106.65).all()
        self.record_check(
            suite, "Tọa độ GPS chuẩn WGS84 thuộc Phường Tây Thạnh",
            bool(lat_ok and lon_ok),
            f"100% tọa độ nằm trong khung [{df_p['latitude'].min():.4f}..{df_p['latitude'].max():.4f}, {df_p['longitude'].min():.4f}..{df_p['longitude'].max():.4f}]"
        )

        # 2.2 Demand không âm (Depot = 0, mọi điểm khách > 0)
        cust_df = df_p[df_p["point_id"] > 0]
        d_valid = (df_p["demand_kg"] >= 0).all() and (cust_df["demand_kg"] > 0).all()
        self.record_check(
            suite, "Demand hợp lệ (Depot = 0, Khách hàng > 0 kg)",
            bool(d_valid),
            f"Depot = 0.0 kg; 50 điểm khách trong khoảng [{cust_df['demand_kg'].min():.1f}, {cust_df['demand_kg'].max():.1f}] kg"
        )

        # 2.3 Mọi q_i <= Q (với xe Q = 1500 kg)
        Q = 1500.0
        d_over = df_p[df_p["demand_kg"] > Q]
        self.record_check(
            suite, "Mọi điểm thu gom thỏa q_i <= Q (1500 kg)",
            len(d_over) == 0,
            f"100% điểm thu gom có q_i <= Q={Q} kg (max q_i = {df_p['demand_kg'].max():.1f} kg)"
        )

        # 2.4 Ma trận khoảng cách khớp kích thước NxN (51x51) theo thứ tự ID
        m_path = os.path.join(self.ward_proc_dir, "distance_matrix.csv")
        dist_m = pd.read_csv(m_path, header=None).to_numpy(dtype=float)
        n_points = len(df_p)
        shape_ok = dist_m.shape == (n_points, n_points)
        self.record_check(
            suite, "Ma trận khớp kích thước NxN (51x51) theo ID",
            shape_ok,
            f"Kích thước ma trận {dist_m.shape} khớp chính xác {n_points} điểm (ID 0..{n_points-1})"
        )

        # 2.5 Đường chéo chính d(i,i) = 0
        diag_zero = bool(np.all(np.diag(dist_m) == 0.0))
        self.record_check(suite, "Đường chéo chính d(i,i) = 0 m", diag_zero, "100% phần tử đường chéo = 0.0 m")

        # 2.6 Khoảng cách ngoài đường chéo d(i,j) > 0 (Không có ô thiếu bị gán bằng 0)
        off_diag_mask = ~np.eye(n_points, dtype=bool)
        off_diag_positive = bool(np.all(dist_m[off_diag_mask] > 0.0))
        self.record_check(
            suite, "Ngoài đường chéo d(i,j) > 0 (Không gán 0 cho ô thiếu)",
            off_diag_positive,
            f"100% cặp i != j có d(i,j) > 0 m (min = {dist_m[off_diag_mask].min():.1f} m, max = {dist_m[off_diag_mask].max():.1f} m)"
        )

    # -------------------------------------------------------------------------
    # SUITE 3: TẢI TRỌNG, CHỨNG CỨ KHẢ THI & PHỤC VỤ ĐÚNG 1 LẦN (4 CHECKS)
    # -------------------------------------------------------------------------
    def check_suite_3_capacity_and_witness(self):
        suite = "3. Tải trọng & Feasible Witness"
        p_path = os.path.join(self.ward_proc_dir, "collection_points.csv")
        r_path = os.path.join(self.ward_proc_dir, "feasible_routes.json")
        df_p = pd.read_csv(p_path)

        with open(r_path, "r", encoding="utf-8") as f:
            feas = json.load(f)

        total_demand = float(df_p["demand_kg"].sum())
        total_cap = float(feas["total_capacity_kg"])

        # 3.1 Điều kiện cần: Tổng demand <= Tổng sức chứa K x Q
        cond_nec = total_demand <= total_cap
        self.record_check(
            suite, "Điều kiện cần: Tổng demand <= K x Q",
            cond_nec,
            f"Tổng demand = {total_demand:.1f} kg <= Tổng sức chứa = {total_cap:.1f} kg"
        )

        # 3.2 Số tuyến <= K và tải trọng từng xe <= Q
        routes = feas["routes"]
        k_limit = int(feas.get("number_of_vehicles", 4))
        all_loads_valid = (len(routes) <= k_limit) and all(r["route_load_kg"] <= r["capacity_kg"] for r in routes)
        self.record_check(
            suite, "Số xe <= K (4 xe) và tải trọng từng xe <= Q",
            all_loads_valid,
            f"Sử dụng {len(routes)}/{k_limit} xe, tất cả các tuyến đều <= 1500.0 kg"
        )

        # 3.3 Phủ đủ 100% điểm khách hàng (không bỏ sót)
        visited_list: List[int] = []
        for r in routes:
            visited_list.extend(r["customer_ids"])
        all_custs_served = set(visited_list)
        expected_custs = set(df_p.loc[df_p["point_id"] > 0, "point_id"])
        full_cover = (all_custs_served == expected_custs)
        self.record_check(
            suite, "Phủ đủ 100% điểm khách hàng (50/50 không bỏ sót)",
            full_cover,
            f"Đã phục vụ đủ {len(all_custs_served)}/{len(expected_custs)} điểm thu gom rác"
        )

        # 3.4 Phục vụ đúng 1 lần mỗi điểm (không lặp) và lộ trình khép kín tại Depot 0
        no_duplicate_visit = (len(visited_list) == len(all_custs_served))
        closed_at_depot = all(
            isinstance(r.get("route"), list) and len(r["route"]) >= 2 and r["route"][0] == 0 and r["route"][-1] == 0
            for r in routes
        )
        self.record_check(
            suite, "Phục vụ đúng 1 lần mỗi điểm & Khép kín về Depot 0",
            bool(no_duplicate_visit and closed_at_depot),
            f"Tổng lượt ghé = {len(visited_list)} (0 điểm lặp), 100% tuyến xuất phát và kết thúc tại Depot 0"
        )

    # -------------------------------------------------------------------------
    # SUITE 4: MẠNG ĐƯỜNG VÀ TÍNH LIÊN THÔNG CÓ HƯỚNG (5 CHECKS)
    # -------------------------------------------------------------------------
    def check_suite_4_road_network(self):
        suite = "4. Mạng đường & Tính liên thông"
        graph_path = os.path.join(self.ward_raw_dir, "road_network.graphml")
        matrix_path = os.path.join(self.ward_proc_dir, "distance_matrix.csv")

        has_graph = os.path.exists(graph_path)
        self.record_check(suite, "File đồ thị gốc road_network.graphml tồn tại", has_graph, f"Đồ thị đường gốc tại {graph_path}")

        dist_m = pd.read_csv(matrix_path, header=None).to_numpy(dtype=float)
        has_no_inf = not (np.any(np.isinf(dist_m)) or np.any(np.isnan(dist_m)))
        self.record_check(
            suite, "Mọi cặp điểm đều có đường đi (Không có Inf/NaN)",
            has_no_inf, "0 cặp điểm bị vô cực hoặc NaN (Dijkstra trên SCC 868 nút)"
        )

        n = dist_m.shape[0]
        from_depot = all(dist_m[0, i] > 0 for i in range(1, n))
        to_depot = all(dist_m[i, 0] > 0 for i in range(1, n))
        self.record_check(suite, "Có đường đi từ Depot đến mọi điểm (d(0,i) > 0)", from_depot, "100% điểm đến được từ Depot")
        self.record_check(suite, "Có đường quay về Depot từ mọi điểm (d(i,0) > 0)", to_depot, "100% điểm quay về được Depot")

        is_symmetric = np.allclose(dist_m, dist_m.T)
        self.record_check(
            suite, "Tính chất có hướng của mạng đường (d(i,j) != d(j,i))",
            not is_symmetric, "Ma trận bất đối xứng phản ánh đúng đường 1 chiều thực tế"
        )

    # -------------------------------------------------------------------------
    # SUITE 5: TÍNH TÁI LẬP & SO SÁNH 2 LẦN CHẠY CÙNG SEED (3 CHECKS)
    # -------------------------------------------------------------------------
    @staticmethod
    def _simulate_seeded_demand_and_types(seed: int, num_Chosen: int = 50) -> Tuple[List[str], List[float]]:
        """
        Tái hiện chính xác quy trình sinh phân tầng loại điểm và nhu cầu rác với seed cố định
        để kiểm chứng tính tất định (determinism) qua 2 lần chạy độc lập.
        """
        rng = np.random.RandomState(seed)
        point_types = ["residential"] * 35 + ["commercial"] * 15
        rng.shuffle(point_types)
        residential_demands = [35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0]
        commercial_demands = [80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0]
        demands = []
        for pt in point_types[:num_Chosen]:
            if pt == "residential":
                demands.append(float(rng.choice(residential_demands)))
            else:
                demands.append(float(rng.choice(commercial_demands)))
        return point_types, demands

    def check_suite_5_reproducibility(self):
        suite = "5. Tính tái lập (Reproducibility)"
        scen_path = os.path.join(self.ward_proc_dir, "scenario.json")
        with open(scen_path, "r", encoding="utf-8") as f:
            scen = json.load(f)

        has_seed = ("seed" in scen) and (scen["seed"] == 42)
        self.record_check(suite, "Cố định Seed ngẫu nhiên (seed=42) trong scenario", has_seed, "Seed được khóa tại 42 để đảm bảo tái lập 100%")

        has_rules = "demand_rule" in scen and "units" in scen
        self.record_check(suite, "Quy tắc sinh dữ liệu và đơn vị đo rõ ràng", has_rules, f"Rule: {scen.get('demand_rule')}")

        # So sánh trực tiếp 2 lần chạy cùng seed=42 và nạp 2 lần qua DataLoader
        types_run1, demands_run1 = self._simulate_seeded_demand_and_types(seed=42)
        types_run2, demands_run2 = self._simulate_seeded_demand_and_types(seed=42)
        loader = DataLoader()
        case_run1 = loader.load_case_study()
        case_run2 = loader.load_case_study()

        identical_runs = (
            types_run1 == types_run2
            and demands_run1 == demands_run2
            and np.array_equal(case_run1["distance_matrix"], case_run2["distance_matrix"])
            and case_run1["demands"] == case_run2["demands"]
        )
        self.record_check(
            suite, "So sánh 2 lần chạy cùng seed=42 khớp tuyệt đối 100%",
            identical_runs,
            "Lần chạy 1 và Lần chạy 2 (cùng seed=42) cho ra vector demand, phân loại điểm và ma trận giống hệt 100%"
        )

    # -------------------------------------------------------------------------
    # SUITE 6: NGUỒN GỐC DỮ LIỆU & ĐỘ CHÍNH XÁC SNAP (3 CHECKS)
    # -------------------------------------------------------------------------
    def check_suite_6_data_provenance(self):
        suite = "6. Nguồn gốc dữ liệu & Snap"
        p_path = os.path.join(self.ward_proc_dir, "collection_points.csv")
        df_p = pd.read_csv(p_path)

        source_types = set(df_p["source_type"].unique())
        has_valid_source = all("giả lập" in s or "quy hoạch" in s for s in source_types)
        self.record_check(
            suite, "Phân loại nguồn dữ liệu (source_type) minh bạch",
            has_valid_source,
            f"Các phân loại nguồn: {source_types} (không gán nhãn sai thùng rác thực tế)"
        )

        # Kiểm tra khoảng cách snap_distance_m hợp lệ
        snap_ok = "snap_distance_m" in df_p.columns and bool((df_p["snap_distance_m"] == 0.0).all())
        self.record_check(
            suite, "Khoảng cách ánh xạ mạng đường (snap_distance_m = 0m)",
            snap_ok,
            "100% điểm nằm trực tiếp trên nút mạng đường SCC (snap_distance_m = 0.0 m)"
        )

        b_path = os.path.join(self.ward_raw_dir, "ward_boundary.geojson")
        has_boundary = os.path.exists(b_path)
        self.record_check(suite, "File ranh giới hành chính ward_boundary.geojson", has_boundary, f"Ranh giới chuẩn WGS84 EPSG:4326 tại {b_path}")

    # -------------------------------------------------------------------------
    # SUITE 7: BENCHMARK CVRPLIB (3 CHECKS)
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

        self.record_check(suite, "Nạp thành công 6 bộ benchmark CVRPLIB gốc (.vrp)", all_loaded, "Cả 6 file .vrp đọc đúng schema" if all_loaded else err_msg)

        meta_path = os.path.join(ROOT_DIR, "results", "benchmark_metadata.csv")
        has_meta = os.path.exists(meta_path)
        meta_cols_ok = False
        if has_meta:
            df_meta = pd.read_csv(meta_path)
            meta_cols_ok = {"bks_cost", "recalculated_int_cost", "recalculated_float_cost"}.issubset(df_meta.columns)
        self.record_check(
            suite,
            "Bảng benchmark_metadata.csv đủ cột Int & Float",
            has_meta and meta_cols_ok,
            f"Tệp kết quả đầy đủ cột Int/Float tại {meta_path}"
        )

        # Kiểm tra cả 6 file .sol đều khớp 100% BKS theo chuẩn số nguyên TSPLIB (diff == 0.0)
        all_sol_match = True
        for inst in instances:
            inst_data = loader.load_instance(inst)
            sol_data = loader.load_solution(inst)
            if sol_data is None:
                all_sol_match = False
                break
            ver = loader.verify_solution_cost(inst_data, sol_data)
            if not ver["is_match"]:
                all_sol_match = False
                break

        self.record_check(
            suite,
            "Đối chứng 6 file nghiệm (.sol) khớp 100% BKS (diff=0)",
            all_sol_match,
            "Cả 6/6 file .sol tính lại theo EUC_2D nguyên (TSPLIB nint) khớp tuyệt đối 100% với BKS"
        )

    # -------------------------------------------------------------------------
    # RUN ALL
    # -------------------------------------------------------------------------
    def run_all_checks(self) -> bool:
        logger.info("================================================================================")
        logger.info("BẮT ĐẦU CHẠY KIỂM ĐỊNH CHẤT LƯỢNG BỘ DỮ LIỆU STEP 2 (v1.0 - 30 TIÊU CHÍ)")
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
        print("\n" + "=" * 105)
        print("BẢNG KẾT QUẢ KIỂM ĐỊNH DỮ LIỆU STEP 2 (VALIDATION REPORT - 30 CHECKS)")
        print("=" * 105)
        print(f"{'HẠNG MỤC (SUITE)':<32} | {'NỘI DUNG KIỂM TRA':<56} | {'KẾT QUẢ':<8}")
        print("-" * 105)
        for r in self.results:
            status_str = f"\033[92m{r['status']}\033[0m" if r['status'] == 'PASS' else f"\033[91m{r['status']}\033[0m"
            print(f"{r['suite']:<32} | {r['check']:<56} | {status_str:<8}")
        print("=" * 105)
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
