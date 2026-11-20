"""
Module Đọc và Tiền Xử lý Dữ liệu Định tuyến (Data Loader Module)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Quy chuẩn: Step 2 - Chuẩn hóa và khóa dữ liệu

Hỗ trợ:
- Đọc bộ dữ liệu chuẩn CVRPLIB (.vrp, .sol) thông qua CVRPLIBLoader và vrplib.
- Đọc bộ dữ liệu Case Study cấp phường chuẩn hóa (data/ward/processed/).
- Kiểm định nghiêm ngặt (Strict Validation): từ chối NaN/Null, ID trùng, demand âm/vượt tải,
  thiếu file hoặc sai kích thước ma trận khoảng cách OSMnx (tuyệt đối không dùng Haversine fallback).
"""

import os
from typing import Dict, Tuple, Any, Optional
import numpy as np
import pandas as pd

from ..config import DEPOT_INDEX, CAPACITY_Q_MAX
from .cvrplib_loader import CVRPLIBLoader


class DataLoader:
    """
    Lớp quản trị và kiểm định dữ liệu bài toán định tuyến (Data Layer).
    """

    def __init__(self, depot_index: int = DEPOT_INDEX):
        self.depot_index = int(depot_index)
        self.cvrp_loader = CVRPLIBLoader()

    def preprocess_case_study_data(
        self,
        points_df: pd.DataFrame,
        dist_matrix: np.ndarray,
        capacity_q_max: float = CAPACITY_Q_MAX
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Hàm kiểm định và tiền xử lý dữ liệu thực tế nghiêm ngặt (Strict Validation).
        Tuân thủ nguyên tắc trung thực khoa học:
        - Không tự ý xóa dòng khuyết dữ liệu (dropna).
        - Không tự ý cắt giảm/gán đè demand khi vượt tải (gây mất mát lượng rác).
        - Không tự ý tái tạo ma trận bằng khoảng cách đối xứng Haversine.
        """
        df = points_df.copy()

        # Chuẩn hóa tên cột lat/lon/demand
        if "latitude" in df.columns and "lat" not in df.columns:
            df["lat"] = df["latitude"]
        if "longitude" in df.columns and "lon" not in df.columns:
            df["lon"] = df["longitude"]
        if "demand_kg" in df.columns and "demand" not in df.columns:
            df["demand"] = df["demand_kg"]

        # Kiểm tra khuyết dữ liệu: Báo lỗi nghiêm ngặt thay vì tự động xóa dòng (dropna)
        missing_mask = df[['lat', 'lon', 'demand']].isna().any(axis=1)
        if missing_mask.any():
            missing_ids = df.loc[missing_mask, 'point_id'].tolist() if 'point_id' in df.columns else df.index[missing_mask].tolist()
            raise ValueError(
                f"Lỗi dữ liệu đầu vào: Phát hiện {missing_mask.sum()} điểm chứa giá trị rỗng (NaN/Null) tại các điểm {missing_ids}. "
                f"Yêu cầu làm sạch và bổ sung đầy đủ dữ liệu gốc, không tự ý drop làm mất điểm thu gom!"
            )

        # Kiểm tra Depot và khóa chính trùng lặp
        if 'point_id' in df.columns:
            if df['point_id'].duplicated().any():
                dup_ids = df.loc[df['point_id'].duplicated(), 'point_id'].unique().tolist()
                raise ValueError(f"Lỗi dữ liệu: Phát hiện khóa chính point_id bị trùng lặp: {dup_ids}.")
            if self.depot_index not in df['point_id'].values:
                raise ValueError(f"Lỗi dữ liệu: Không tìm thấy trạm tập kết Depot với ID={self.depot_index} trong file.")

        # Kiểm tra miền giá trị demand: không âm và không vượt sức chứa xe Q_max
        negative_points = []
        overloaded_points = []
        for idx, row in df.iterrows():
            pt_id = int(row.get('point_id', idx))
            dmd = float(row['demand'])
            if dmd < 0.0:
                negative_points.append((pt_id, dmd))
            elif pt_id != self.depot_index and dmd > capacity_q_max:
                overloaded_points.append((pt_id, dmd))

        if negative_points:
            detail_neg = ", ".join([f"Điểm {p}: {d} kg" for p, d in negative_points])
            raise ValueError(f"Lỗi dữ liệu tải trọng: Phát hiện nhu cầu rác âm bất hợp lệ ({detail_neg}).")

        if overloaded_points:
            detail_str = ", ".join([f"Điểm {p}: {d} kg > {capacity_q_max} kg" for p, d in overloaded_points])
            raise ValueError(
                f"Lỗi dữ liệu tải trọng: Phát hiện các điểm vượt quá sức chứa phương tiện ({detail_str}). "
                f"Không tự ý cắt giảm demand làm thất thoát khối lượng rác! "
                f"Yêu cầu áp dụng Customer Splitting (tách thành nhiều chuyến gom bổ sung) hoặc tăng tải trọng xe Q."
            )

        # Ma trận khoảng cách: Kiểm tra nghiêm ngặt kích thước, cấm tự ý nội suy bằng Haversine
        clean_matrix = np.asarray(dist_matrix, dtype=float).copy()
        n = len(df)
        if clean_matrix.shape[0] != n or clean_matrix.shape[1] != n:
            raise ValueError(
                f"Lỗi ma trận khoảng cách: Kích thước ma trận ({clean_matrix.shape}) không khớp với số điểm ({n}). "
                f"Tuyệt đối không tự động tái tạo bằng Haversine (vì Haversine là đối xứng, không phản ánh đường 1 chiều, vòng xoay của OSMnx). "
                f"Yêu cầu trích xuất lại ma trận Dijkstra có hướng từ đồ thị OSMnx!"
            )

        np.fill_diagonal(clean_matrix, 0.0)

        # Kiểm tra nghiêm ngặt: Tuyệt đối không tự ý thay khoảng cách thiếu/không kết nối bằng 0 (Quy chuẩn Step 2 - Mục 2.6 & 2.7)
        if np.any(np.isnan(clean_matrix)) or np.any(np.isinf(clean_matrix)):
            bad_indices = np.argwhere(np.isnan(clean_matrix) | np.isinf(clean_matrix))
            pairs_str = ", ".join([f"({int(u)}->{int(v)})" for u, v in bad_indices[:10]])
            raise ValueError(
                f"Lỗi ma trận khoảng cách: Phát hiện {len(bad_indices)} cặp điểm không có đường đi (NaN/Inf): {pairs_str}. "
                f"Tuyệt đối không tự động gán bằng 0!"
            )

        if np.any(clean_matrix < 0.0):
            raise ValueError("Lỗi ma trận khoảng cách: Tồn tại khoảng cách âm bất hợp lệ.")

        return df, clean_matrix

    def load_case_study(
        self, points_csv_path: Optional[str] = None, distance_matrix_csv_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Đọc bộ dữ liệu Case Study Phường thực tế:
        - Mặc định tìm kiếm trong data/ward/processed/.
        - Chuẩn hóa khoảng cách ra km cho hàm fitness và lưu khoảng cách gốc mét.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

        # Tìm đường dẫn points_csv_path
        if points_csv_path is None or not os.path.exists(points_csv_path):
            candidates = [
                os.path.join(root_dir, "data", "ward", "processed", "collection_points.csv"),
            ]
            for c in candidates:
                if os.path.exists(c):
                    points_csv_path = c
                    break

        if not points_csv_path or not os.path.exists(points_csv_path):
            raise FileNotFoundError(f"Không tìm thấy file danh sách điểm thu gom: {points_csv_path}")

        # Tìm đường dẫn distance_matrix_csv_path (bắt buộc tồn tại ma trận Dijkstra OSMnx)
        if distance_matrix_csv_path is None:
            default_matrix = os.path.join(root_dir, "data", "ward", "processed", "distance_matrix.csv")
            if os.path.exists(default_matrix):
                distance_matrix_csv_path = default_matrix

        if not distance_matrix_csv_path or not os.path.exists(distance_matrix_csv_path):
            raise FileNotFoundError(
                f"Không tìm thấy file ma trận khoảng cách đường bộ có hướng: {distance_matrix_csv_path}. "
                f"Tuyệt đối không dùng khoảng cách đường chim bay Haversine thay thế! "
                f"Yêu cầu chạy script src/map/extract_map.py để trích xuất ma trận Dijkstra từ đồ thị OSMnx."
            )

        points_df = pd.read_csv(points_csv_path)
        dist_matrix_raw = pd.read_csv(distance_matrix_csv_path, header=None).to_numpy(dtype=float)

        # Kiểm định nghiêm ngặt dữ liệu (Strict Validation)
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
