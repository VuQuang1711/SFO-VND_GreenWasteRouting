"""
Module Trực quan hóa Lộ trình Thu gom Rác trên Bản đồ Tương tác (Route Mapper Module)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Vẽ bản đồ trực quan bằng Folium/Leaflet với đa màu sắc cho từng xe và mũi tên chỉ hướng

Tham chiếu:
- Mục 5 của Bản mô tả đề tài (GVHD/01_Mo_ta_de_tai_SFO_VND_Green_Waste_Routing.docx)
- Code thực nghiệm của thành viên Tâm Đức (Members/Tâm Đức/Week 2/Untitled16.ipynb)
"""

import os
from typing import List, Dict, Tuple, Any, Optional
import numpy as np


class RouteMapper:
    """
    Lớp vẽ và xuất bản đồ trực quan hóa lộ trình xe thu gom rác:
    - Hiển thị trạm tập kết Depot bằng biểu tượng ngôi sao màu đen nổi bật.
    - Phân tách từng xe bằng màu sắc và nét vẽ riêng biệt (PolyLine).
    - Hiển thị mũi tên chỉ hướng di chuyển của dòng xe (Directional Arrows).
    - Đánh số thứ tự ghé thăm từng thùng rác (#1, #2, #3...) trên đầu mỗi nút.
    """

    DEFAULT_COLORS = [
        "#E63946",  # Đỏ tươi
        "#1D3557",  # Xanh dương đậm
        "#2A9D8F",  # Xanh ngọc
        "#F4A261",  # Cam đất
        "#9B5DE5",  # Tím phong lan
        "#E76F51",  # Đỏ cam
        "#457B9D",  # Xanh lam
        "#00F5D4"   # Xanh lục bảo
    ]

    def __init__(self, depot_coords: Tuple[float, float] = (10.808521, 106.623105), zoom_start: int = 15):
        """
        Khởi tạo bộ vẽ bản đồ.

        Tham số:
        - depot_coords: Tọa độ GPS [vĩ độ, kinh độ] của bãi tập kết Depot (mặc định tại Phường Sơn Kỳ).
        - zoom_start: Mức độ phóng to ban đầu khi mở bản đồ tương tác.
        """
        self.depot_coords = list(depot_coords)
        self.zoom_start = int(zoom_start)

    def _fetch_road_geometry(self, path_coords: List[List[float]]) -> List[List[float]]:
        """
        Truy vấn mạng đường bộ OSRM để lấy tọa độ uốn lượn chính xác theo tim đường giao thông.
        Nếu ngoại tuyến hoặc lỗi kết nối, tự động trả về path_coords gốc (đường thẳng dự phòng).
        """
        if len(path_coords) < 2:
            return path_coords

        import json
        import urllib.request

        full_road_path = []
        chunk_size = 20

        for idx in range(0, len(path_coords) - 1, chunk_size - 1):
            sub_coords = path_coords[idx:idx + chunk_size]
            if len(sub_coords) < 2:
                continue
            coord_str = ';'.join(f'{c[1]:.6f},{c[0]:.6f}' for c in sub_coords)
            url = f'http://router.project-osrm.org/route/v1/driving/{coord_str}?overview=full&geometries=geojson'
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'WasteRoutingGreen/1.0'})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    if data.get('code') == 'Ok' and data.get('routes'):
                        osrm_pts = data['routes'][0]['geometry']['coordinates']
                        # OSRM trả về [lon, lat], folium cần [lat, lon]
                        sub_road = [[p[1], p[0]] for p in osrm_pts]
                        if full_road_path:
                            full_road_path.extend(sub_road[1:])
                        else:
                            full_road_path.extend(sub_road)
                    else:
                        full_road_path.extend(sub_coords)
            except Exception:
                # Cơ chế phòng thủ: Tự động dùng đường nối trực tiếp nếu mất mạng
                full_road_path.extend(sub_coords)

        return full_road_path if full_road_path else path_coords

    def generate_map(
        self,
        routes: List[List[int]],
        points_info: Dict[int, Dict[str, Any]],
        output_html_path: str = "green_waste_routing_map.html"
    ) -> str:
        """
        Vẽ bản đồ lộ trình các xe và xuất ra file HTML tương tác.

        Tham số:
        - routes: Danh sách các tuyến xe (ví dụ: [[0, 1, 2, 0], [0, 3, 4, 0]]).
        - points_info: Từ điển chứa tọa độ và thông tin từng điểm:
          {node_id: {'lat': float, 'lon': float, 'demand': float, 'name': str}}
        - output_html_path: Đường dẫn lưu file kết quả HTML.

        Trả về:
        - output_html_path: Đường dẫn đến file HTML đã tạo.
        """
        try:
            import folium
            from folium.plugins import PolyLineTextPath
        except ImportError:
            # Lập trình phòng thủ: Nếu máy chưa cài folium, thông báo hướng dẫn cài đặt và trả về file rỗng
            print(
                "[CẢNH BÁO MÔI TRƯỜNG]: Chưa tìm thấy thư viện 'folium'. "
                "Vui lòng cài đặt bằng lệnh: pip install folium để xem bản đồ tương tác!"
            )
            return ""

        # Khởi tạo bản đồ nền Google Maps sắc nét, chi tiết đường phố và địa danh thực tế
        route_map = folium.Map(
            location=self.depot_coords,
            zoom_start=self.zoom_start,
            tiles=None
        )

        # Lớp 1: Google Maps Đường phố / Giao thông tiêu chuẩn (Mặc định tải cực nhanh)
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attr="Google Maps",
            name="Google Maps (Đường phố)",
            control=True
        ).add_to(route_map)

        # Lớp 2: Google Maps Ảnh Vệ Tinh Lai (Satellite Hybrid - nhìn rõ từng khu phố, tòa nhà)
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            attr="Google Satellite",
            name="Google Maps (Ảnh Vệ Tinh)",
            control=True
        ).add_to(route_map)

        # Lớp 3: OpenStreetMap (Dự phòng)
        folium.TileLayer(
            tiles="OpenStreetMap",
            name="OpenStreetMap",
            control=True
        ).add_to(route_map)

        # 1. Đánh dấu Trạm tập kết Depot trung tâm
        depot_fg = folium.FeatureGroup(name="★ Trạm tập kết (Depot 0)", show=True)
        depot_popup = f"""
        <div style="font-family: Arial, sans-serif; min-width: 240px; line-height: 1.5;">
            <div style="background-color: #0f172a; color: white; padding: 6px 10px; border-radius: 4px; font-weight: bold; margin-bottom: 6px;">
                ★ TRẠM TẬP KẾT RÁC SƠN KỲ (DEPOT 0)
            </div>
            <div style="font-size: 12px; color: #334155;">
                <b>Vị trí:</b> Trung tâm điều phối rác Phường Sơn Kỳ<br>
                <i>100% các xe thu gom bắt buộc xuất phát từ đây và quay về đây xả rác để hoàn tất chu trình.</i>
            </div>
        </div>
        """
        folium.Marker(
            location=self.depot_coords,
            popup=depot_popup,
            tooltip="★ Trạm tập kết rác Sơn Kỳ (Depot 0) - Xuất phát & Quay về",
            icon=folium.Icon(color="black", icon="star", prefix="fa")
        ).add_to(depot_fg)
        depot_fg.add_to(route_map)

        # 2. Vẽ lộ trình và các điểm thu gom cho từng xe dưới dạng FeatureGroup độc lập
        color_labels = ["Đỏ", "Xanh dương", "Xanh ngọc", "Cam đất", "Tím", "Đỏ cam"]
        active_route_idx = 0
        truck_legend_data = []

        for r_idx, route in enumerate(routes):
            # Lọc bỏ tuyến rỗng
            non_depot_pts = [pt for pt in route if pt != 0]
            if not non_depot_pts:
                continue

            color = self.DEFAULT_COLORS[active_route_idx % len(self.DEFAULT_COLORS)]
            c_label = color_labels[active_route_idx % len(color_labels)]
            truck_name = f"Xe Thu Gom #{active_route_idx + 1}"
            active_route_idx += 1

            # FeatureGroup riêng cho xe này, cho phép bật/tắt hoặc xem độc lập
            truck_fg = folium.FeatureGroup(name=f"🚚 {truck_name} (Màu {c_label})", show=True)

            # Lấy danh sách tọa độ dọc theo tuyến (BẮT BUỘC KHÉP KÍN: Xuất phát tại Depot và Quay về Depot)
            path_coords = [self.depot_coords]
            for pt in non_depot_pts:
                if pt in points_info:
                    path_coords.append([points_info[pt]['lat'], points_info[pt]['lon']])
            path_coords.append(self.depot_coords)

            # Lấy danh sách tọa độ uốn lượn thực tế theo mạng đường giao thông (turn-by-turn road geometry)
            road_path = self._fetch_road_geometry(path_coords)

            # Vẽ đường lộ trình chạy liên tục trên mặt đường nhựa (ĐƯỜNG NÉT LIỀN, KHÔNG CÓ MŨI TÊN GÂY RỐI MẮT)
            folium.PolyLine(
                road_path,
                color=color,
                weight=5,
                opacity=0.9,
                tooltip=f"Chu trình khép kín của {truck_name}: Depot ➔ {len(non_depot_pts)} điểm ➔ Depot"
            ).add_to(truck_fg)

            # Đánh dấu các điểm dừng hình tròn mang màu của xe với số thứ tự ghé thăm ở giữa
            total_pts = len(non_depot_pts)
            for step_order, pt in enumerate(non_depot_pts, 1):
                info = points_info.get(pt, {})
                lat = info.get('lat', self.depot_coords[0])
                lon = info.get('lon', self.depot_coords[1])
                demand = info.get('demand', 0.0)
                pt_name = info.get('name', f'Điểm #{pt}')
                node_type = info.get('node_type', 'Nhà dân')

                is_last_stop = (step_order == total_pts)
                next_step_str = "Quay về Trạm tập kết Sơn Kỳ (Depot 0) xả rác hoàn tất chu trình 🏁" if is_last_stop else f"Tiếp tục ghé Điểm dừng #{step_order + 1}"

                popup_content = f"""
                <div style="font-family: Arial, sans-serif; min-width: 230px; line-height: 1.5;">
                    <div style="background-color: {color}; color: white; padding: 6px 10px; border-radius: 4px; font-weight: bold; margin-bottom: 6px;">
                        🚚 {truck_name} (Điểm dừng #{step_order} / {total_pts})
                    </div>
                    <div style="font-size: 13px; font-weight: bold; color: #0f172a;">{pt_name}</div>
                    <div style="font-size: 12px; color: #475569; margin: 4px 0;">Loại địa điểm: <b>{node_type}</b></div>
                    <div style="font-size: 13px; color: #dc2626; font-weight: bold;">Khối lượng rác: {demand:.1f} kg</div>
                    <div style="font-size: 12px; color: #0284c7; margin-top: 5px; border-top: 1px dashed #cbd5e1; padding-top: 4px;">
                        <b>Chặng tiếp theo:</b> {next_step_str}
                    </div>
                </div>
                """

                # Hình tròn mang màu của xe với số thứ tự ghé thăm ở tâm
                badge_html = f"""
                <div style="
                    width: 20px;
                    height: 20px;
                    background-color: {color};
                    color: #ffffff;
                    border: 2px solid #ffffff;
                    border-radius: 50%;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.35);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 10px;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                    line-height: 20px;
                    text-align: center;
                    cursor: pointer;
                ">
                    {step_order}
                </div>
                """

                folium.Marker(
                    location=[lat, lon],
                    icon=folium.DivIcon(
                        icon_size=(20, 20),
                        icon_anchor=(10, 10),
                        html=badge_html
                    ),
                    popup=popup_content,
                    tooltip=f"#{step_order}: {pt_name} ({demand:.0f} kg) - {truck_name}"
                ).add_to(truck_fg)

            truck_fg.add_to(route_map)
            total_load = sum(points_info.get(p, {}).get('demand', 0.0) for p in non_depot_pts)
            truck_legend_data.append((truck_name, color, c_label, len(non_depot_pts), total_load, active_route_idx - 1))

        # 3. Thêm Bảng Chú Giải (Legend) tương tác có các nút bấm lọc xem từng xe hoặc xem tất cả
        legend_items_html = ""
        btn_filter_html = """
        <button onclick="filterTruck(-1)" style="font-size: 11px; padding: 4px 8px; background: #0f172a; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; margin: 2px;">
            Hiện tất cả
        </button>
        """

        for t_name, color, c_label, n_pts, t_load, fg_idx in truck_legend_data:
            legend_items_html += f"""
            <div style="margin-bottom: 5px; display: flex; align-items: center; justify-content: space-between;">
                <span>
                    <span style="display: inline-block; width: 14px; height: 14px; background-color: {color}; border-radius: 3px; margin-right: 6px; vertical-align: middle;"></span>
                    <b>{t_name}:</b> {n_pts} điểm
                </span>
                <span style="color: #b91c1c; font-weight: bold; margin-left: 8px;">{t_load:,.1f} kg</span>
            </div>
            """
            btn_filter_html += f"""
            <button onclick="filterTruck({fg_idx})" style="font-size: 11px; padding: 4px 8px; background: {color}; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; margin: 2px;">
                Chỉ Xe #{fg_idx + 1}
            </button>
            """

        legend_html = f"""
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            width: 310px;
            background-color: rgba(255, 255, 255, 0.96);
            border: 2px solid #cbd5e1;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.25);
            z-index: 9999;
            font-family: Arial, sans-serif;
            font-size: 13px;
            padding: 12px 14px;
        ">
            <h4 style="margin: 0 0 8px 0; color: #0f172a; font-size: 14px; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; font-weight: bold;">
                🚛 CHÚ GIẢI & ĐIỀU KHIỂN ĐỘI XE
            </h4>
            <div style="margin-bottom: 8px; padding-bottom: 6px; border-bottom: 1px dashed #e2e8f0;">
                <span style="color: black; font-size: 15px; margin-right: 4px;">★</span>
                <b>Depot 0:</b> Trạm tập kết Sơn Kỳ (Bắt đầu & Kết thúc)
            </div>
            {legend_items_html}
            
            <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #cbd5e1;">
                <div style="font-size: 11px; font-weight: bold; color: #334155; margin-bottom: 4px;">
                    👁️ Chọn chế độ hiển thị tuyến đường:
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 2px;">
                    {btn_filter_html}
                </div>
            </div>
            
            <div style="font-size: 11px; color: #64748b; margin-top: 8px; font-style: italic;">
                * Tuyến khép kín xuất phát từ Depot 0 và quay về Depot 0.<br>
                * Bạn cũng có thể tích chọn các ô ở góc trên bên trái.
            </div>
        </div>

        <script>
        function filterTruck(targetIdx) {{
            const overlays = document.querySelectorAll('.leaflet-control-layers-overlays input[type="checkbox"]');
            if (!overlays || overlays.length === 0) return;
            
            overlays.forEach((cb, idx) => {{
                // idx = 0 là Depot 0 (luôn bật)
                if (idx === 0) {{
                    if (!cb.checked) cb.click();
                    return;
                }}
                
                const truckIdx = idx - 1;
                if (targetIdx === -1) {{
                    // Bật tất cả các xe
                    if (!cb.checked) cb.click();
                }} else if (truckIdx === targetIdx) {{
                    // Bật duy nhất xe được chọn
                    if (!cb.checked) cb.click();
                }} else {{
                    // Tắt các xe khác
                    if (cb.checked) cb.click();
                }}
            }});
        }}
        </script>
        """
        route_map.get_root().html.add_child(folium.Element(legend_html))

        # Thêm bảng điều khiển chuyển đổi các lớp bản đồ (mở sẵn bên góc trên bên trái để dễ dàng tích chọn)
        folium.LayerControl(position="topleft", collapsed=False).add_to(route_map)

        # Lưu bản đồ ra file
        parent_dir = os.path.dirname(output_html_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        route_map.save(output_html_path)
        print(f"[THÀNH CÔNG]: Đã xuất bản đồ lộ trình trực quan ra: {output_html_path}")
        return output_html_path
