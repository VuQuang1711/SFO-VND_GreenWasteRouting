"""
Module Trích xuất Mạng đường Thực tế từ OpenStreetMap (Extract Map Module)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Tải đồ thị đường phố qua OSMnx, ánh xạ điểm thu gom và tính ma trận khoảng cách N x N

Tham chiếu:
- Mục 5 của Bản mô tả đề tài (GVHD/01_Mo_ta_de_tai_SFO_VND_Green_Waste_Routing.docx)
- Nhiệm vụ Step 2 của thành viên Tâm Đức (Báo cáo Step 1, Mục 10.2)
"""

import os
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd


class MapExtractor:
    """
    Lớp tải và trích xuất ma trận khoảng cách mạng đường giao thông thực tế:
    - Tải đồ thị mạng đường cấp phường (OSMnx).
    - Ánh xạ (snap) tọa độ GPS các thùng rác vào nút đường gần nhất.
    - Tính toán ma trận khoảng cách ngắn nhất theo mạng đường bộ bằng thuật toán Dijkstra.
    - Hỗ trợ phương án dự phòng (Fallback Haversine) nếu không có kết nối Internet hoặc chưa cài OSMnx.
    """

    def __init__(self, place_query: str = "Phường Sơn Kỳ, Quận Tân Phú, Thành phố Hồ Chí Minh, Vietnam"):
        """
        Khởi tạo bộ trích xuất mạng đường.

        Tham số:
        - place_query: Địa chỉ ranh giới hành chính cần tải mạng đường từ OpenStreetMap.
        """
        self.place_query = place_query
        self.graph = None

    def download_road_network(self):
        """Tải đồ thị đường bộ từ OpenStreetMap bằng OSMnx."""
        try:
            import osmnx as ox
            print(f"[THÔNG BÁO]: Đang tải mạng lưới giao thông từ OpenStreetMap cho khu vực: '{self.place_query}'...")
            self.graph = ox.graph_from_place(self.place_query, network_type="drive")
            print(f"[THÀNH CÔNG]: Đã tải thành công đồ thị giao thông với {len(self.graph.nodes)} nút đường.")
            return self.graph
        except ImportError:
            print(
                "[CẢNH BÁO MÔI TRƯỜNG]: Chưa cài đặt thư viện 'osmnx'. "
                "Hệ thống sẽ tự động kích hoạt chế độ tính khoảng cách mặt cầu Haversine kết hợp hệ số uốn lượn đường phố (1.3)."
            )
            return None
        except Exception as e:
            print(f"[CẢNH BÁO KẾT NỐI]: Không thể tải bản đồ trực tuyến ({e}). Kích hoạt chế độ dự phòng ngoại tuyến.")
            return None

    def compute_distance_matrix(
        self, points_df: pd.DataFrame, output_csv_path: Optional[str] = None
    ) -> np.ndarray:
        """
        Tính toán ma trận khoảng cách N x N giữa tất cả các điểm thu gom:
        - Nếu có đồ thị OSMnx: Dùng thuật toán Dijkstra tìm đường ngắn nhất trên mạng đường thực tế.
        - Nếu ngoại tuyến: Dùng công thức Haversine có nhân hệ số uốn lượn đô thị (Detour Factor = 1.3).
        """
        n = len(points_df)
        dist_matrix = np.zeros((n, n), dtype=float)
        coords = points_df[['lat', 'lon']].to_numpy()

        if self.graph is not None:
            try:
                import osmnx as ox
                import networkx as nx

                # Ánh xạ tọa độ các điểm vào nút đường gần nhất
                nearest_nodes = ox.distance.nearest_nodes(self.graph, X=coords[:, 1], Y=coords[:, 0])

                # Tính đường đi ngắn nhất Dijkstra
                for i in range(n):
                    for j in range(n):
                        if i != j:
                            try:
                                dist_meters = nx.shortest_path_length(
                                    self.graph, nearest_nodes[i], nearest_nodes[j], weight="length"
                                )
                                dist_matrix[i, j] = round(dist_meters / 1000.0, 3)  # Quy đổi ra km
                            except nx.NetworkXNoPath:
                                # Nếu hai nút không liên thông (ví dụ đường 1 chiều bị cụt), dùng đường dự phòng
                                d_lat = coords[i, 0] - coords[j, 0]
                                d_lon = coords[i, 1] - coords[j, 1]
                                dist_matrix[i, j] = round(np.sqrt(d_lat**2 + d_lon**2) * 111.0 * 1.5, 3)
            except Exception as e:
                print(f"[CẢNH BÁO TÍNH TOÁN]: Xảy ra lỗi khi tính Dijkstra ({e}). Chuyển sang tính Haversine.")
                self.graph = None

        if self.graph is None:
            # Chế độ tính khoảng cách dự phòng Haversine
            import math
            for i in range(n):
                for j in range(n):
                    if i != j:
                        lat1, lon1 = coords[i, 0], coords[i, 1]
                        lat2, lon2 = coords[j, 0], coords[j, 1]
                        r = 6371.0
                        dlat = math.radians(lat2 - lat1)
                        dlon = math.radians(lon2 - lon1)
                        a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin(dlon / 2.0)**2)
                        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
                        dist_matrix[i, j] = round(r * c * 1.3, 3)

        if output_csv_path:
            parent_dir = os.path.dirname(output_csv_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            np.savetxt(output_csv_path, dist_matrix, delimiter=",", fmt="%.3f")
            print(f"[THÀNH CÔNG]: Đã lưu ma trận khoảng cách ({n}x{n}) ra file: {output_csv_path}")

        return dist_matrix
