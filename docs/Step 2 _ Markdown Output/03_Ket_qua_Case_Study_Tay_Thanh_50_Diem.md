# 🏙️ KẾT QUẢ 3: CASE STUDY PHƯỜNG TÂY THẠNH 50 ĐIỂM & PHÂN TÍCH CHUYÊN SÂU

> **Đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu  
> **Thành viên phụ trách chính:** Lê Nguyễn Tâm Đức *(GIS & Mạng đường giao thông)*, Vũ Thế Quang *(Khóa Schema & Kịch bản)*  
> **Tài liệu tham chiếu:** *STEP2_Huong_dan_chi_tiet_SFO_VND_Green_Waste_Routing.pdf (Mục 2.1, 2.5 & 3)*

---

## 📌 1. BẢNG TỔNG HỢP KẾT QUẢ ĐẦU RA CASE STUDY

Nhóm đã xây dựng và chuẩn hóa thành công bộ dữ liệu thực địa **Phường Tây Thạnh, Quận Tân Phú, Thành phố Hồ Chí Minh**:

| Hạng mục dữ liệu | Giá trị cụ thể đã chuẩn hóa | Nguồn dữ liệu & Phương pháp xác minh | Tệp tin lưu trữ đối chứng |
| :--- | :--- | :--- | :--- |
| **Ranh giới hành chính** | Đa giác khép kín EPSG:4326, diện tích $4.12\text{ km}^2$ | OpenStreetMap Nominatim Overpass API (`admin_level = 8`), ngày lấy: 24/10/2026 | [`data/ward/raw/ward_boundary.geojson`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson) |
| **Vùng đệm mạng đường (Buffer)** | **400 mét** mở rộng đa giác | Khuyến nghị chuẩn 300–500m để bảo đảm kết nối thông suốt với đường vành đai ngoài | [`docs/ward_selection.md`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/ward_selection.md) |
| **Quy mô đồ thị giao thông** | **935 nút (nodes), 2,123 cung đường (edges)** | Thư viện `osmnx` tải đồ thị xe ô tô (`network_type = "drive"`) | [`data/ward/raw/road_network.graphml`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml) |
| **Thành phần liên thông mạnh (SCC)** | **868 nút (chiếm 92.8% toàn mạng)** | Thuật toán Tarjan/Kosaraju xác định SCC lớn nhất, loại bỏ ngõ cụt 1 chiều | [`src/map/generate_tay_thanh_dataset.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/map/generate_tay_thanh_dataset.py) |
| **Số điểm thu gom** | **50 điểm khách hàng + 1 Depot (= 51 điểm)** | Lấy trực tiếp từ các nút thuộc SCC trên 13 trục phố chính của Tây Thạnh | [`data/ward/processed/collection_points.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/collection_points.csv) |
| **Khoảng cách Snap** | **0.0 m (100% điểm nằm khít trên tim đường)** | Triệt tiêu hoàn toàn hiện tượng điểm trôi nổi ngoài mạng đường | Cột `snap_distance_m` trong `collection_points.csv` |
| **Trạm trung chuyển (Depot)** | Tọa độ $(10.8122, 106.6215)$ tại **KCN Tân Bình** | Vị trí bãi tập kết và trạm trung chuyển rác quy hoạch thực tế, tiếp giáp đường CN13 | [`data/ward/processed/depot.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/depot.csv) |
| **Cấu hình Đội xe** | $K = 4$ xe chuyên dụng; Sức chứa $Q = 1,500\text{ kg}$/xe | Quy chuẩn thực tế xe ép rác mini đô thị 1.5 tấn (CITENCO) | [`data/ward/processed/vehicles.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/vehicles.csv) |
| **Phân phối rác (Demand)** | • **35 điểm dân cư:** $35 - 75\text{ kg}$<br>• **15 điểm thương mại/dịch vụ:** $80 - 120\text{ kg}$ | Sinh ngẫu nhiên có kiểm soát, cố định `seed = 42`. Tổng demand: **3,345.0 kg** | [`data/ward/processed/scenario.json`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/scenario.json) |

---

## 🧠 2. PHÂN TÍCH CHUYÊN SÂU: TẠI SAO LẠI THỰC HIỆN NHƯ VẬY?

### 2.1. Tại sao phải chuyển địa bàn sang Phường Tây Thạnh thay vì giữ tên "Sơn Kỳ cũ" (Giải quyết vấn đề R1)?
* **Vấn đề lịch sử hành chính:** Trong Step 1, nhóm khảo sát theo tên quen thuộc là "Phường Sơn Kỳ". Tuy nhiên, sau các đợt sắp xếp địa giới hành chính của TP.HCM, địa bàn Sơn Kỳ cũ đã được phân bổ vào các phường lân cận như Bình Hưng Hòa, Tây Thạnh và Tân Sơn Nhì.
* **Nguyên tắc liêm chính học thuật từ GVHD:** Thầy hướng dẫn nhấn mạnh: *"Không được tự vẽ ranh giới rồi gọi là ranh giới hành chính. Nhóm phải đối chiếu ranh giới thực tế, không lấy tên 'phường Sơn Kỳ' làm mặc định"*.
* **Giải pháp lựa chọn:** Nhóm đã phân tích 3 ứng viên và chính thức chọn **Phường Tây Thạnh (Quận Tân Phú)** vì:
  1. Có ranh giới GIS pháp lý chính thức trên OpenStreetMap (`admin_level = 8`).
  2. Kế thừa trực tiếp các trục đường khảo sát thực tế của đề tài từ Step 1 (Lê Trọng Tấn, Chế Lan Viên, Tây Thạnh, CN13).
  3. Có quỹ đất Khu công nghiệp Tân Bình cực kỳ thuận lợi để đặt Trạm trung chuyển Depot xe tải mà không gây xung đột quy hoạch đô thị.

### 2.2. Tại sao phải thiết lập vùng đệm mạng đường (Buffer 400m)?
* Nếu cắt đồ thị đường bộ đúng khít theo đường biên ranh giới hành chính (Polygon), các con đường vành đai bao quanh phường (như Lê Trọng Tấn, Trường Chinh, Kênh 19/5) sẽ bị cắt đứt làm đôi:
  - Xe gom rác đi đến mép phường sẽ bị coi là "rơi xuống vực", không thể quay đầu xe.
  - Xe không thể rẽ vào các nút giao và bùng binh nằm ngay sát ngoài ranh giới để đổi làn hoặc quay về Depot.
* Vùng đệm **400m** (nằm trong dải khuyến nghị 300–500m của GVHD) bảo đảm mạng lưới giao thông xung quanh phường được liên tục, giúp đồ thị có đầy đủ các giao lộ quay đầu và kết nối với các trục đường huyết mạch.

### 2.3. Tại sao phải lấy các điểm thu gom TRỰC TIẾP TRÊN MẠNG ĐƯỜNG (Snap distance = 0.0m)?
* **Lỗi trước đây:** Ban đầu, 50 điểm thu gom lấy tọa độ rải rác từ khu đô thị Celadon City và các ngõ hẻm sâu, dẫn tới việc khi chiếu vuông góc vào đồ thị ô tô Tây Thạnh, có điểm bị văng xa tới **659.6 m**, hiển thị trên bản đồ như những điểm trôi nổi ngoài không gian.
* **Quy định chuẩn hóa của GVHD (Mục 15):**  
  > *"Đặt vị trí các điểm thu gom trên các đoạn đường có thể tiếp cận. Nếu là điểm mô phỏng, chỉ ghi 'điểm thu gom giả lập trên mạng đường OSM'"*.
* **Giải pháp chuẩn hóa:** Nhóm đã lấy 50 điểm thu gom trực tiếp từ tập nút của mạng đường ô tô (`G_scc`) trên 13 tuyến đường thực tế. Nhờ vậy:
  - Khoảng cách snap đạt **0.0 m tuyệt đối**.
  - Xe ép rác ô tô chắc chắn tiếp cận được tận nơi mà không gặp trở ngại cấm tải hay ngõ hẻm quá hẹp.
  - Trên bản đồ trực quan, các điểm thu gom hiển thị nằm khít trên tim đường, tạo nên một trực quan hóa dữ liệu vô cùng chuyên nghiệp và thuyết phục trước hội đồng.

### 2.4. Tại sao phải phân tầng Demand (35 dân cư + 15 thương mại) và cố định Seed 42?
* **Thực tế đô thị:** Lượng rác tại một hộ gia đình/ngõ dân cư (35–75 kg) hoàn toàn khác với lượng rác thải phát sinh tại một nhà hàng, quán ăn, siêu thị tiện lợi hay cơ sở dịch vụ ven đường (80–120 kg). Việc phân tầng giúp bài toán phản ánh sát thực tế cấu trúc phát sinh rác đô thị tại TP.HCM.
* **Cố định `seed = 42`:** Đảm bảo **tính tái lập 100% (Reproducibility)**. Dù giảng viên, hội đồng hay thành viên khác trong nhóm chạy lại mã nguồn trên máy tính khác ở bất kỳ thời điểm nào, toàn bộ 50 điểm thu gom, lượng rác và thứ tự các nút vẫn giữ nguyên vẹn không đổi.

---

## 📁 3. MINH CHỨNG VÀ LIÊN KẾT TỆP LIÊN QUAN

1. Tệp ranh giới GIS: [`data/ward/raw/ward_boundary.geojson`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson)
2. Tệp đồ thị mạng đường: [`data/ward/raw/road_network.graphml`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml)
3. Danh sách 50 điểm thu gom: [`data/ward/processed/collection_points.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/collection_points.csv)
4. Trạm trung chuyển Depot: [`data/ward/processed/depot.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/depot.csv)
5. Kịch bản tham số: [`data/ward/processed/scenario.json`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/scenario.json)
6. Từ điển dữ liệu: [`docs/data_dictionary.md`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/data_dictionary.md)

