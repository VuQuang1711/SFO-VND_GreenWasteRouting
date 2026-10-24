# 🗺️ BÁO CÁO LỰA CHỌN PHƯỜNG NGHIÊN CỨU & PHẠM VI MẠNG ĐƯỜNG (WARD SELECTION)

> **Đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai Sailfish Optimizer và Variable Neighborhood Descent (SFO-VND)  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu (Công việc 2.1)  
> **Thành viên phụ trách:** Lê Nguyễn Tâm Đức (Mạng đường & GIS), Vũ Thế Quang (Điều phối)

---

## 📌 1. Bối cảnh & Xử lý vấn đề địa danh hành chính (Vấn đề R1)

Theo định hướng quy hoạch và đề xuất ban đầu từ Step 1, nhóm khảo sát khu vực mang tên gọi lịch sử "Phường Sơn Kỳ" (Quận Tân Phú). Tuy nhiên, căn cứ theo hướng dẫn chi tiết của Thầy hướng dẫn tại Step 2:
* **Thực trạng hành chính:** Địa bàn "Phường Sơn Kỳ" cũ sau quá trình sắp xếp, điều chỉnh địa giới hành chính tại TP. Hồ Chí Minh đã được phân bổ vào các phường lân cận: **Bình Hưng Hòa (Quận Bình Tân), Tây Thạnh và Tân Sơn Nhì (Quận Tân Phú)**.
* **Nguyên tắc khoa học:** Nghiên cứu không lấy tên "phường Sơn Kỳ" làm mặc định hành chính pháp lý hiện hành, không tự vẽ ranh giới tự phát rồi gán nhãn ranh giới hành chính. Ranh giới phải được trích xuất từ dữ liệu GIS có nguồn gốc mở được kiểm chứng (**OpenStreetMap / Nominatim Administrative Boundary Level 8**) với hệ tọa độ chuẩn quốc tế **WGS84 (EPSG:4326)**.

---

## 📊 2. Bảng so sánh các khu vực ứng viên nghiên cứu

Nhóm tiến hành lập bảng so sánh chi tiết giữa 2 khu vực ứng viên tiềm năng liền kề khu vực Sơn Kỳ cũ:

| Tiêu chí đánh giá | Khu vực Ứng viên 1 (CHÍNH THỨC)<br>**Phường Tây Thạnh, Quận Tân Phú** | Khu vực Ứng viên 2 (DỰ PHÒNG)<br>**Phường Tân Sơn Nhì, Quận Tân Phú** |
| :--- | :--- | :--- |
| **Tên đơn vị hiện hành** | Phường Tây Thạnh, Quận Tân Phú, TP.HCM | Phường Tân Sơn Nhì, Quận Tân Phú, TP.HCM |
| **Mã cấp hành chính** | `admin_level = 8` (Cấp Phường) | `admin_level = 8` (Cấp Phường) |
| **Nguồn trích xuất GIS** | OpenStreetMap Overpass API (Relation ID verified) | OpenStreetMap Overpass API (Relation ID verified) |
| **Hệ tọa độ tham chiếu** | EPSG:4326 (WGS84 Lat/Lon) | EPSG:4326 (WGS84 Lat/Lon) |
| **Diện tích địa bàn** | Khoảng **4.12 km²** | Khoảng **3.65 km²** |
| **Tọa độ bao viền (Bounds)** | Lon: `[106.6074, 106.6358]`, Lat: `[10.8032, 10.8247]` | Lon: `[106.6099, 106.6383]`, Lat: `[10.7931, 10.8093]` |
| **Kế thừa dữ liệu Sơn Kỳ** | **Rất cao**: Bao hàm trực tiếp đoạn trục chính Lê Trọng Tấn, đường CN13, Chế Lan Viên, Tây Thạnh nơi nhóm đã có dữ liệu khảo sát thực địa. | **Trung bình**: Tiếp giáp phía Nam, chủ yếu là khu dân cư hẻm và trục Tân Kỳ Tân Quý. |
| **Mức đầy đủ đường OSM** | **Rất hoàn chỉnh**: Đầy đủ các cấp đường từ trục chính (Primary), thứ cấp (Secondary), đường nội bộ (Residential) đến đường khu công nghiệp (Industrial). | **Đầy đủ**: Mật độ hẻm dân cư cao, một số hẻm sâu có khả năng hạn chế xe gom cỡ vừa. |
| **Khả năng chọn Depot** | **Rất thuận lợi**: Có khu công nghiệp Tân Bình và quỹ đất trạm trung chuyển chất thải quy hoạch (đường CN13 / Lê Trọng Tấn), xe tải dễ dàng ra vào. | **Khá**: Khó bố trí depot độc lập hơn do mật độ nhà ở dày đặc. |
| **Quy mô điểm thu gom** | Bố trí 50 điểm thu gom (dân cư + thương mại) cách nhau 80 - 200m hợp lý. | Bố trí được 40 - 50 điểm thu gom. |
| **Quyết định lựa chọn** | **CHỌN LÀM ĐỊA BÀN CHÍNH THỨC** | **LƯU LÀM PHƯƠNG ÁN DỰ PHÒNG** |

---

## 🛣️ 3. Phạm vi mạng đường và Vùng đệm Buffer

Nhằm tránh hiện tượng mạng đường bị cắt đứt gãy một cách cơ học đúng mép viền hành chính (khiến xe thu gom không thể quay đầu hoặc không kết nối được với Depot và đường vành đai bên ngoài), nhóm thiết lập vùng đệm:
* **Khoảng mở rộng đã chọn:** **400 mét** (nằm trong dải khuyến nghị 300 – 500 mét của hướng dẫn Step 2).
* **Mô hình giao thông:** Xe ô tô chuyên dụng (`network_type = "drive"`).
* **Thống kê mạng lưới:**
  * Tổng số nút giao thông (Nodes): **935 nút**
  * Tổng số đoạn đường (Edges): **2,123 cạnh**
  * Thành phần liên thông mạnh lớn nhất (Strongly Connected Component - SCC): **868 nút (chiếm 92.8% toàn mạng)**.
* **Quy tắc bảo đảm kết nối:** 100% các điểm thu gom rác và Depot đều được snap vào các nút thuộc thành phần liên thông mạnh SCC này, bảo đảm tuyệt đối mọi cặp điểm đều có đường đi ngắn nhất hai chiều ($d(0, i) < \infty$ và $d(i, 0) < \infty$).

---

## 📷 4. Bản đồ minh chứng

Bản đồ ranh giới hành chính Phường Tây Thạnh chồng lớp lên mạng đường bộ OSMnx, vị trí Depot và 50 điểm thu gom rác đã được xuất ra định dạng hình ảnh chuẩn tại:
* [map_boundary.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/map_boundary.png)
* [map.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/map.png)

---

## 📦 5. Danh mục tệp bàn giao Công việc 2.1

1. [ward_boundary.geojson](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson): Ranh giới hành chính EPSG:4326 chuẩn GeoJSON.
2. [road_network.graphml](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml): Đồ thị đường ô tô có hướng có thuộc tính `length` (m).
3. [extract_map.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/map/extract_map.py): Script tái tạo mạng đường, snap tọa độ và tính Dijkstra.
4. [map_boundary.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/map_boundary.png): Ảnh minh chứng ranh giới chồng mạng đường.
