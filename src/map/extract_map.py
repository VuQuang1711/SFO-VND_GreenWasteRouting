"""
Module Trích xuất Mạng đường Thực tế từ OpenStreetMap (extract_map.py)
Đề tài: Tối ưu hóa lộ trình thu gom rác đô thị bằng thuật toán lai SFO-VND
Quy chuẩn: Step 2 - Công việc 2.1 & 2.6

Chức năng:
- Tải đồ thị đường bộ theo ranh giới hành chính và vùng đệm buffer (300-500m).
- Lưu và đọc đồ thị mạng đường dạng file chuẩn .graphml (road_network.graphml).
- Ánh xạ (snap) Depot và các điểm thu gom rác vào nút đường gần nhất trong đồ thị.
- Tính toán và lưu khoảng cách snap (m) theo yêu cầu mục 19.
- Tính ma trận khoảng cách ngắn nhất có hướng (Dijkstra có trọng số length)
  đảm bảo d(i, j) phản ánh đường một chiều, d(i, i) = 0 và không tự thay 0 khi mất kết nối.
"""

import os
import sys
import math
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd
import networkx as nx

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class MapExtractor:
    """
    Lớp tải và trích xuất mạng đường và ma trận khoảng cách có hướng từ OSMnx.
    """

    def __init__(
        self,
        ward_name: str = "Phường Tây Thạnh",
        district_name: str = "Quận Tân Phú",
        city_name: str = "Thành phố Hồ Chí Minh",
        buffer_meters: float = 400.0
    ):
        self.ward_name = ward_name
        self.district_name = district_name
        self.city_name = city_name
        self.buffer_meters = float(buffer_meters)
        self.graph = None
        self.boundary_gdf = None

    def load_or_extract_network(self, graphml_path: Optional[str] = None) -> nx.MultiDiGraph:
        """
        Nạp đồ thị từ file .graphml có sẵn (để tái lập nhanh mà không cần gọi lại OSM),
        hoặc tải trực tiếp từ OSMnx nếu file chưa tồn tại.
        """
        if graphml_path and os.path.exists(graphml_path):
            import osmnx as ox
            print(f"[THÔNG BÁO]: Đang nạp đồ thị mạng đường đã lưu từ: {graphml_path}")
            self.graph = ox.load_graphml(graphml_path)
            print(f" -> Đã nạp thành công: {len(self.graph.nodes)} nút, {len(self.graph.edges)} cạnh.")
            return self.graph

        # Tải từ OpenStreetMap
        try:
            import osmnx as ox
            import geopandas as gpd

            print(f"[THÔNG BÁO]: Đang truy vấn ranh giới hành chính cho: '{self.ward_name}, {self.district_name}'...")
            query = f"{self.district_name}, {self.city_name}, Vietnam"
            tags = {"admin_level": "8", "boundary": "administrative"}
            gdf_dist = ox.features_from_place(query, tags=tags)
            sub = gdf_dist[gdf_dist["name"] == self.ward_name]

            if sub.empty:
                raise ValueError(f"Không tìm thấy ranh giới của {self.ward_name} trong OSM.")

            ward_poly = sub.geometry.iloc[0]
            self.boundary_gdf = gpd.GeoDataFrame([{"name": self.ward_name}], geometry=[ward_poly], crs="EPSG:4326")

            # Mở rộng buffer theo mét
            gdf_proj = self.boundary_gdf.to_crs(epsg=3857)
            buffered_proj = gdf_proj.geometry.iloc[0].buffer(self.buffer_meters)
            buffered_poly = gpd.GeoSeries([buffered_proj], crs="EPSG:3857").to_crs(epsg=4326).iloc[0]

            print(f"[THÔNG BÁO]: Đang tải đồ thị đường cho ô tô (network_type='drive') có buffer={self.buffer_meters}m...")
            self.graph = ox.graph_from_polygon(buffered_poly, network_type="drive")
            print(f"[THÀNH CÔNG]: Đồ thị đã tải: {len(self.graph.nodes)} nút, {len(self.graph.edges)} cạnh.")

            if graphml_path:
                os.makedirs(os.path.dirname(os.path.abspath(graphml_path)), exist_ok=True)
                ox.save_graphml(self.graph, filepath=graphml_path)
                print(f" -> Đã lưu đồ thị ra file .graphml: {graphml_path}")

            return self.graph
        except Exception as e:
            print(f"[LỖI TRÍCH XUẤT OSM]: {e}")
            raise

    def snap_points(
        self, points_df: pd.DataFrame, lat_col: str = "latitude", lon_col: str = "longitude"
    ) -> Tuple[List[int], List[float]]:
        """
        Snap từng điểm vào nút gần nhất trên đồ thị.
        Trả về danh sách snapped_nodes và khoảng cách snap (m).
        """
        if self.graph is None:
            raise ValueError("Đồ thị đường chưa được khởi tạo. Hãy gọi load_or_extract_network trước.")

        # Lấy thành phần liên thông mạnh lớn nhất để đảm bảo kết nối
        scc_nodes = max(nx.strongly_connected_components(self.graph), key=len)
        G_scc = self.graph.subgraph(scc_nodes)

        node_ids = list(G_scc.nodes)
        node_lats = np.array([G_scc.nodes[n]["y"] for n in node_ids])
        node_lons = np.array([G_scc.nodes[n]["x"] for n in node_ids])

        snapped_nodes = []
        snap_distances = []

        for _, row in points_df.iterrows():
            lat = float(row[lat_col])
            lon = float(row[lon_col])

            dists = (node_lats - lat) ** 2 + (node_lons - lon) ** 2
            best_idx = np.argmin(dists)
            best_node = node_ids[best_idx]

            # Khoảng cách snap xấp xỉ bằng mét
            dx = (lon - node_lons[best_idx]) * 111000.0 * math.cos(math.radians(lat))
            dy = (lat - node_lats[best_idx]) * 111000.0
            dist_m = round(math.sqrt(dx * dx + dy * dy), 1)

            snapped_nodes.append(best_node)
            snap_distances.append(dist_m)

        return snapped_nodes, snap_distances

    def compute_directed_distance_matrix(
        self, snapped_nodes: List[int], output_csv_path: Optional[str] = None
    ) -> np.ndarray:
        """
        Tính ma trận khoảng cách ngắn nhất có hướng (Dijkstra, weight='length') bằng mét.
        Mỗi phần tử D[i, j] là độ dài đường ngắn nhất từ node i tới node j.
        """
        if self.graph is None:
            raise ValueError("Đồ thị đường chưa được khởi tạo.")

        scc_nodes = max(nx.strongly_connected_components(self.graph), key=len)
        G_scc = self.graph.subgraph(scc_nodes)

        n = len(snapped_nodes)
        dist_matrix = np.zeros((n, n), dtype=float)

        for i, u_node in enumerate(snapped_nodes):
            lengths = nx.single_source_dijkstra_path_length(G_scc, u_node, weight="length")
            for j, v_node in enumerate(snapped_nodes):
                if i == j:
                    dist_matrix[i, j] = 0.0
                else:
                    if v_node in lengths:
                        dist_matrix[i, j] = round(lengths[v_node], 1)
                    else:
                        dist_matrix[i, j] = np.inf

        if output_csv_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
            np.savetxt(output_csv_path, dist_matrix, delimiter=",", fmt="%.1f")
            print(f"[THÀNH CÔNG]: Đã lưu ma trận khoảng cách có hướng ra file: {output_csv_path}")

        return dist_matrix
