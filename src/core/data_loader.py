"""
Module Đọc và Tiền Xử lý Dữ liệu Định tuyến (Data Loader Module)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Quy chuẩn: Step 2 - Chuẩn hóa và khóa dữ liệu

Hỗ trợ:
- Đọc bộ dữ liệu chuẩn CVRPLIB (.vrp, .sol) thông qua CVRPLIBLoader và vrplib.
- Đọc bộ dữ liệu Case Study cấp phường chuẩn hóa (data/ward/processed/ hoặc data/case_study/).
- Hỗ trợ phòng thủ dữ liệu: phát hiện NaN, duplicate, vượt tải, ma trận khuyết.
"""

import os
import sys
import math
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import pandas as pd

from ..config import DEPOT_INDEX, CAPACITY_Q_MAX
from .cvrplib_loader import CVRPLIBLoader


class DataLoader:
    """
    Lớp quản trị và tiền xử lý dữ liệu bài toán định tuyến (Data Layer).
    """

    def __init__(self, depot_index: int = DEPOT_INDEX):
        self.depot_index = int(depot_index)
        self.cvrp_loader = CVRPLIBLoader()

    @staticmethod
    def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Tính khoảng cách đường cong mặt cầu Haversine (km) giữa 2 tọa độ GPS.
        """
        r = 6371.0  # Bán kính Trái Đất (km)
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return r * c

    def preprocess_case_study_data(
        self,
        points_df: pd.DataFrame,
        dist_matrix: np.ndarray,
        capacity_q_max: float = CAPACITY_Q_MAX
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Hàm tiền xử lý và khử nhiễu dữ liệu thực tế (Defensive Preprocessing).
        """
        df = points_df.copy()

        # Chuẩn hóa tên cột lat/lon/demand
        if "latitude" in df.columns and "lat" not in df.columns:
            df["lat"] = df["latitude"]
        if "longitude" in df.columns and "lon" not in df.columns:
            df["lon"] = df["longitude"]
        if "demand_kg" in df.columns and "demand" not in df.columns:
            df["demand"] = df["demand_kg"]

        initial_count = len(df)
        df = df.dropna(subset=['lat', 'lon', 'demand'])
        if len(df) < initial_count:
            print(f"[CẢNH BÁO TIỀN XỬ LÝ]: Đã loại bỏ {initial_count - len(df)} dòng dữ liệu chứa giá trị rỗng (NaN).")

        # Kiểm tra Depot
        if 'point_id' in df.columns and self.depot_index not in df['point_id'].values:
            raise ValueError(f"Lỗi dữ liệu: Không tìm thấy trạm tập kết Depot với ID={self.depot_index} trong file.")

        # Xử lý khối lượng rác vượt quá sức chứa xe Q_max
        for idx, row in df.iterrows():
            pt_id = int(row.get('point_id', idx))
            dmd = float(row['demand'])
            if pt_id != self.depot_index and dmd > capacity_q_max:
                print(
                    f"[CẢNH BÁO VƯỢT TẢI]: Điểm {pt_id} có lượng rác {dmd} kg > sức chứa {capacity_q_max} kg. "
                    f"Tự động điều chỉnh ngưỡng gom tối đa cho mỗi lượt là {capacity_q_max} kg."
                )
                df.at[idx, 'demand'] = capacity_q_max

        # Ma trận khoảng cách
        clean_matrix = np.asarray(dist_matrix, dtype=float).copy()
        n = len(df)
        if clean_matrix.shape[0] != n or clean_matrix.shape[1] != n:
            print(f"[CẢNH BÁO MA TRẬN]: Kích thước ma trận ({clean_matrix.shape}) không khớp số điểm ({n}). Tái tạo dự phòng.")
            clean_matrix = np.zeros((n, n), dtype=float)
            coords = df[['lat', 'lon']].to_numpy()
            for i in range(n):
                for j in range(n):
                    if i != j:
                        clean_matrix[i, j] = self.calculate_haversine_distance(
                            coords[i, 0], coords[i, 1], coords[j, 0], coords[j, 1]
                        ) * 1.3

        np.fill_diagonal(clean_matrix, 0.0)
        clean_matrix = np.nan_to_num(clean_matrix, nan=0.0, posinf=999.0, neginf=0.0)
        clean_matrix = np.maximum(clean_matrix, 0.0)

        return df, clean_matrix

    def load_case_study(
        self, points_csv_path: Optional[str] = None, distance_matrix_csv_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Đọc bộ dữ liệu Case Study Phường thực tế:
        - Mặc định tìm kiếm trong data/ward/processed/ hoặc data/case_study/.
        - Chuẩn hóa khoảng cách ra km cho hàm fitness và lưu khoảng cách gốc mét.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

        # Tìm đường dẫn points_csv_path
        if points_csv_path is None or not os.path.exists(points_csv_path):
            candidates = [
                os.path.join(root_dir, "data", "ward", "processed", "collection_points.csv"),
                os.path.join(root_dir, "data", "case_study", "collection_points.csv"),
            ]
            for c in candidates:
                if os.path.exists(c):
                    points_csv_path = c
                    break

        if not points_csv_path or not os.path.exists(points_csv_path):
            raise FileNotFoundError(f"Không tìm thấy file danh sách điểm thu gom: {points_csv_path}")

        # Tìm đường dẫn distance_matrix_csv_path
        if distance_matrix_csv_path is None or not os.path.exists(distance_matrix_csv_path):
            candidates = [
                os.path.join(root_dir, "data", "ward", "processed", "distance_matrix.csv"),
                os.path.join(root_dir, "data", "case_study", "distance_matrix.csv"),
            ]
            for c in candidates:
                if os.path.exists(c):
                    distance_matrix_csv_path = c
                    break

        points_df = pd.read_csv(points_csv_path)

        if distance_matrix_csv_path and os.path.exists(distance_matrix_csv_path):
            dist_matrix_raw = pd.read_csv(distance_matrix_csv_path, header=None).to_numpy(dtype=float)
        else:
            n = len(points_df)
            dist_matrix_raw = np.zeros((n, n), dtype=float)
            coords = points_df[['lat', 'lon']].to_numpy()
            for i in range(n):
                for j in range(n):
                    if i != j:
                        dist_matrix_raw[i, j] = self.calculate_haversine_distance(
                            coords[i, 0], coords[i, 1], coords[j, 0], coords[j, 1]
                        ) * 1.3

        # Tiền xử lý dữ liệu qua bộ lọc phòng thủ
        points_df, dist_matrix_clean = self.preprocess_case_study_data(points_df, dist_matrix_raw)

        # Nếu giá trị trung bình > 50 -> ma trận đang ở đơn vị mét -> quy đổi ra km cho thuật toán tính fitness
        if np.mean(dist_matrix_clean) > 50.0:
            dist_matrix_km = dist_matrix_clean / 1000.0
            dist_matrix_m = dist_matrix_clean
        else:
            dist_matrix_km = dist_matrix_clean
            dist_matrix_m = dist_matrix_clean * 1000.0

        demands = points_df.set_index('point_id')['demand'].to_dict()
        dimension = len(points_df) - 1

        return {
            "name": os.path.basename(points_csv_path),
            "points_df": points_df,
            "distance_matrix": dist_matrix_km,
            "distance_matrix_m": dist_matrix_m,
            "demands": demands,
            "dimension": dimension,
            "capacity_q_max": CAPACITY_Q_MAX,
            "depot_index": self.depot_index,
            "points_file": points_csv_path,
            "matrix_file": distance_matrix_csv_path
        }

    def load_cvrplib_instance(self, vrp_file_path: str) -> Dict[str, Any]:
        """
        Đọc và phân tích cú pháp file chuẩn CVRPLIB (.vrp) thông qua CVRPLIBLoader.
        """
        data = self.cvrp_loader.load_instance(vrp_file_path)
        return {
            "name": data["name"],
            "dimension": data["num_customers"],
            "capacity_q_max": data["capacity"],
            "coords": data["node_coord"],
            "demands": data["demand"],
            "distance_matrix": data["distance_matrix"],
            "depot_index": data["depot"]
        }
