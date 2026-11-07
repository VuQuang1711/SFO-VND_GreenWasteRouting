"""
Script trực quan hóa file đồ thị road_network.graphml lên Bản đồ Tương tác HTML
Sử dụng các nguồn bản đồ nền ổn định (CartoDB, Google Maps) không bị chặn lỗi OSM 403.
"""

import os
import folium
import pandas as pd
import osmnx as ox

current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
graphml_path = os.path.join(current_dir, "data", "ward", "raw", "road_network.graphml")
depot_path = os.path.join(current_dir, "data", "ward", "processed", "depot.csv")
points_path = os.path.join(current_dir, "data", "ward", "processed", "collection_points.csv")
output_html = os.path.join(current_dir, "results", "view_road_network.html")

def generate_interactive_map():
    print(f"[1/3] Đang nạp đồ thị từ: {graphml_path}...")
    G = ox.load_graphml(graphml_path)
    nodes, edges = ox.graph_to_gdfs(G)
    
    centroid = [float(nodes["y"].mean()), float(nodes["x"].mean())]
    
    # Khởi tạo bản đồ không dùng tiles mặc định của OSM để tránh lỗi 403 Access Blocked
    m = folium.Map(location=centroid, zoom_start=15, tiles=None)
    
    # Lớp 1: Google Maps Đường phố (Mặc định: sắc nét, tải cực nhanh, không cần API key, không bị chặn)
    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attr="Google Maps",
        name="Google Maps (Đường phố)",
        control=True
    ).add_to(m)
    
    # Lớp 2: Google Maps Ảnh Vệ Tinh (Satellite Hybrid)
    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attr="Google Satellite",
        name="Google Maps (Ảnh Vệ Tinh)",
        control=True
    ).add_to(m)
    
    # Lớp 3: Esri World Street Map (Dự phòng bản đồ địa hình/đường phố quốc tế)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri WorldStreetMap",
        name="Bản đồ Esri World Street Map",
        control=True
    ).add_to(m)
    
    print("[2/3] Đang vẽ 2,123 cung đường và thông tin thuộc tính...")
    folium.GeoJson(
        edges[["geometry", "name", "length", "oneway"]].to_json(),
        name="Mạng đường ô tô (2,123 cạnh)",
        style_function=lambda x: {"color": "#1D3557", "weight": 2.5, "opacity": 0.8},
        tooltip=folium.GeoJsonTooltip(
            fields=["name", "length", "oneway"],
            aliases=["Tên đường:", "Chiều dài (m):", "Một chiều:"]
        )
    ).add_to(m)
    
    # Thêm Depot nếu có
    if os.path.exists(depot_path):
        depot_df = pd.read_csv(depot_path)
        depot_fg = folium.FeatureGroup(name="★ Trạm trung chuyển (Depot)", show=True)
        for _, row in depot_df.iterrows():
            folium.Marker(
                location=[float(row["latitude"]), float(row["longitude"])],
                popup=f"<b>DEPOT: {row['name']}</b><br>Tọa độ: {row['latitude']}, {row['longitude']}",
                icon=folium.Icon(color="red", icon="star")
            ).add_to(depot_fg)
        depot_fg.add_to(m)
            
    # Thêm 50 điểm thu gom nếu có
    if os.path.exists(points_path):
        pts_df = pd.read_csv(points_path)
        points_fg = folium.FeatureGroup(name="50 Điểm thu gom rác", show=True)
        for _, row in pts_df.iterrows():
            if row["point_id"] == 0:
                continue
            folium.CircleMarker(
                location=[float(row["latitude"]), float(row["longitude"])],
                radius=4.5,
                color="#E63946",
                fill=True,
                fill_color="#E63946",
                fill_opacity=0.9,
                popup=(
                    f"<b>Điểm #{int(row['point_id'])}: {row['name']}</b><br>"
                    f"Rác gom: {row['demand_kg']} kg<br>"
                    f"Loại điểm: {row.get('point_type', 'residential')}<br>"
                    f"Khoảng cách snap: {row.get('snap_distance_m', 0):.1f} m"
                )
            ).add_to(points_fg)
        points_fg.add_to(m)
            
    # Thêm bảng điều khiển bật tắt các lớp (Layer Control)
    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    m.save(output_html)
    print(f"[3/3] Đã xuất thành công bản đồ mạng đường tại: {output_html}")
    return output_html

if __name__ == "__main__":
    generate_interactive_map()
