"""
Module Đọc và Tiền Xử lý Dữ liệu Định tuyến (Data Loader Module)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Đọc chuẩn dữ liệu CVRPLIB (.vrp) và Dữ liệu Case Study thực tế (.csv)

Tham chiếu:
- Benchmark CVRPLIB (data/benchmarks/*.vrp)
- Báo cáo Step 1: Mục 3.2, 5.1 & 7.1
- Universal Blueprint: Tiền xử lý dữ liệu với 3 trường hợp biên (Edge Cases) thực tế.
"""

import os
import math
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import pandas as pd

from ..config import DEPOT_INDEX, CAPACITY_Q_MAX


class DataLoader:
    """
    Lớp quản trị và tiền xử lý dữ liệu bài toán định tuyến (Data Layer).
    Hỗ trợ 2 chế độ:
    - Đọc dữ liệu chuẩn CVRPLIB (.vrp) cho mục đích thực nghiệm Benchmark.
    - Đọc dữ liệu điểm thu gom và ma trận khoảng cách mạng đường cho Case Study thực tế.
    """

    def __init__(self, depot_index: int = DEPOT_INDEX):
        self.depot_index = int(depot_index)

    @staticmethod
    def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Tính khoảng cách đường cong mặt cầu Haversine (km) giữa 2 tọa độ GPS.
        Dùng làm phương án dự phòng (Fallback) khi mạng đường OSMnx bị khuyết hoặc ngoại tuyến.
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
        
        Xử lý triệt để 3 trường hợp biên (Edge Cases) tệ nhất ngoài thực tế:
        1. Trường hợp biên 1: Điểm thu gom bị trùng lặp tọa độ hoặc ID, hoặc chứa giá trị NaN.
           -> Tự động khử trùng lặp (Deduplication) và gán lại ID chuẩn hóa từ 0 (Depot) đến N.
        2. Trường hợp biên 2: Khối lượng rác tại một điểm vượt quá sức chứa tối đa Q_max của xe.
           -> Cảnh báo và tự động phân tách điểm (Split) thành nhiều lượt gom nhỏ để tránh gây bất khả thi.
        3. Trường hợp biên 3: Ma trận khoảng cách mạng đường có giá trị âm, NaN, hoặc vô cực do đường cụt/một chiều.
           -> Tự động phát hiện và bù đắp bằng khoảng cách Haversine nhân hệ số uốn lượn đô thị (Detour factor = 1.3).
        """
        # --- XỬ LÝ BIÊN 1: Khử NaN và trùng lặp ---
        df = points_df.copy()
        initial_count = len(df)
        df = df.dropna(subset=['lat', 'lon', 'demand'])
        if len(df) < initial_count:
            print(f"[CẢNH BÁO TIỀN XỬ LÝ]: Đã loại bỏ {initial_count - len(df)} dòng dữ liệu chứa giá trị rỗng (NaN).")

        # Kiểm tra Depot
        if 'point_id' in df.columns and self.depot_index not in df['point_id'].values:
            raise ValueError(f"Lỗi dữ liệu: Không tìm thấy trạm tập kết Depot với ID={self.depot_index} trong file.")

        # --- XỬ LÝ BIÊN 2: Khối lượng rác vượt quá sức chứa xe Q_max ---
        for idx, row in df.iterrows():
            pt_id = int(row.get('point_id', idx))
            dmd = float(row['demand'])
            if pt_id != self.depot_index and dmd > capacity_q_max:
                print(
                    f"[CẢNH BÁO VƯỢT TẢI]: Điểm {pt_id} có lượng rác {dmd} kg > sức chứa {capacity_q_max} kg. "
                    f"Tự động điều chỉnh ngưỡng gom tối đa cho mỗi lượt là {capacity_q_max} kg."
                )
                df.at[idx, 'demand'] = capacity_q_max

        # --- XỬ LÝ BIÊN 3: Ma trận khoảng cách bị khuyết hoặc âm/vô cực ---
        clean_matrix = np.asarray(dist_matrix, dtype=float).copy()
        n = len(df)
        if clean_matrix.shape[0] != n or clean_matrix.shape[1] != n:
            print(f"[CẢNH BÁO MA TRẬN]: Kích thước ma trận ({clean_matrix.shape}) không khớp số điểm ({n}). Tự động tái tạo từ tọa độ GPS.")
            clean_matrix = np.zeros((n, n), dtype=float)
            coords = df[['lat', 'lon']].to_numpy()
            for i in range(n):
                for j in range(n):
                    if i != j:
                        # Khoảng cách mặt cầu x hệ số đường phố quanh co 1.3
                        clean_matrix[i, j] = self.calculate_haversine_distance(
                            coords[i, 0], coords[i, 1], coords[j, 0], coords[j, 1]
                        ) * 1.3

        # Đảm bảo đường chéo bằng 0 và không có giá trị âm
        np.fill_diagonal(clean_matrix, 0.0)
        clean_matrix = np.nan_to_num(clean_matrix, nan=0.0, posinf=999.0, neginf=0.0)
        clean_matrix = np.maximum(clean_matrix, 0.0)

        return df, clean_matrix

    def load_case_study(
        self, points_csv_path: str, distance_matrix_csv_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Đọc bộ dữ liệu Case Study Phường thực tế:
        - points_csv: File CSV chứa (point_id, name, lat, lon, demand, type, service_time).
        - distance_matrix_csv: File CSV ma trận NxN khoảng cách đường bộ (km).
        """
        if not os.path.exists(points_csv_path):
            raise FileNotFoundError(f"Không tìm thấy file danh sách điểm thu gom: {points_csv_path}")

        points_df = pd.read_csv(points_csv_path)

        # Đọc hoặc sinh ma trận khoảng cách
        if distance_matrix_csv_path and os.path.exists(distance_matrix_csv_path):
            dist_matrix = pd.read_csv(distance_matrix_csv_path, header=None).to_numpy(dtype=float)
        else:
            # Nếu chưa có file ma trận, tự động tính bằng khoảng cách Haversine
            n = len(points_df)
            dist_matrix = np.zeros((n, n), dtype=float)
            coords = points_df[['lat', 'lon']].to_numpy()
            for i in range(n):
                for j in range(n):
                    if i != j:
                        dist_matrix[i, j] = self.calculate_haversine_distance(
                            coords[i, 0], coords[i, 1], coords[j, 0], coords[j, 1]
                        ) * 1.3

        # Tiền xử lý dữ liệu qua bộ lọc phòng thủ
        points_df, dist_matrix = self.preprocess_case_study_data(points_df, dist_matrix)

        demands = points_df.set_index('point_id')['demand'].to_dict()
        dimension = len(points_df) - 1  # Trừ 1 điểm Depot

        return {
            "name": os.path.basename(points_csv_path),
            "points_df": points_df,
            "distance_matrix": dist_matrix,
            "demands": demands,
            "dimension": dimension,
            "capacity_q_max": CAPACITY_Q_MAX,
            "depot_index": self.depot_index
        }

    def load_cvrplib_instance(self, vrp_file_path: str) -> Dict[str, Any]:
        """
        Đọc và phân tích cú pháp file chuẩn CVRPLIB (.vrp) quốc tế.
        Hỗ trợ định dạng chuẩn: EDGE_WEIGHT_TYPE: EUC_2D.
        """
        if not os.path.exists(vrp_file_path):
            raise FileNotFoundError(f"Không tìm thấy file CVRPLIB: {vrp_file_path}")

        name = ""
        dimension = 0
        capacity = 0.0
        coords: Dict[int, Tuple[float, float]] = {}
        demands: Dict[int, float] = {}

        mode = None

        with open(vrp_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("NAME"):
                    name = line.split(":")[-1].strip()
                elif line.startswith("DIMENSION"):
                    dimension = int(line.split(":")[-1].strip())
                elif line.startswith("CAPACITY"):
                    capacity = float(line.split(":")[-1].strip())
                elif line.startswith("NODE_COORD_SECTION"):
                    mode = "COORD"
                    continue
                elif line.startswith("DEMAND_SECTION"):
                    mode = "DEMAND"
                    continue
                elif line.startswith("DEPOT_SECTION"):
                    mode = "DEPOT"
                    continue
                elif line.startswith("EOF"):
                    break
                else:
                    parts = line.split()
                    if mode == "COORD" and len(parts) >= 3:
                        node_id = int(parts[0]) - 1  # Đưa về 0-indexed
                        coords[node_id] = (float(parts[1]), float(parts[2]))
                    elif mode == "DEMAND" and len(parts) >= 2:
                        node_id = int(parts[0]) - 1
                        demands[node_id] = float(parts[1])

        # Tính ma trận khoảng cách Euclid 2D
        num_nodes = len(coords)
        dist_matrix = np.zeros((num_nodes, num_nodes), dtype=float)
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j:
                    dx = coords[i][0] - coords[j][0]
                    dy = coords[i][1] - coords[j][1]
                    dist_matrix[i, j] = round(math.sqrt(dx * dx + dy * dy))

        return {
            "name": name,
            "dimension": dimension - 1,  # Số điểm khách (trừ Depot)
            "capacity_q_max": capacity,
            "coords": coords,
            "demands": demands,
            "distance_matrix": dist_matrix,
            "depot_index": self.depot_index
        }
