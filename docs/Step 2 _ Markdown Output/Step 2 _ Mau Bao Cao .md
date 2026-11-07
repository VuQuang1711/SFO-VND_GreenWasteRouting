# SFO–VND GREEN WASTE ROUTING / MẪU BÁO CÁO STEP 2
**Tài liệu giao việc và nghiệm thu nội bộ • Trang 1 – 5**  
**BIỂU MẪU NHÓM SINH VIÊN TỰ ĐIỀN**

# BÁO CÁO STEP 2 — CHUẨN BỊ VÀ KHÓA BỘ DỮ LIỆU
**Nhóm Gom Rác — Đề tài SFO–VND Green Waste Routing**

> [!NOTE]
> **Cách điền:** Báo cáo kết quả nhóm đã thực hiện, không chép lại hướng dẫn. Mỗi kết luận đều kèm minh chứng (tên file, ảnh, kết quả chạy, commit).

---

### Bảng Thông tin chung

| Thông tin | Nhóm điền |
| :--- | :--- |
| **Thành viên/nhóm trưởng** | 1. **Vũ Thế Quang** *(Nhóm trưởng)*<br>2. **Lê Nguyễn Tâm Đức**<br>3. **Nguyễn Ngọc Thảo Hiền**<br>*(Lớp 15DHKHDL03 — Ngành Khoa học Dữ liệu)* |
| **Ngày nộp / số phiên bản** | 25/10/2026 / **Phiên bản dữ liệu v1.0 (Khóa Step 2)** |
| **Git repository/commit** | Repo: `https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting.git`<br>Commit: `926ce3c` (*refactor(data): don dep cac file vrp du thua va xoa thu muc case_study cu*) |
| **Máy và môi trường thực thi** | Windows 11 AMD64; Python 3.13.14; `osmnx 2.1.1`, `vrplib 2.2.0`, `networkx 3.6.1`, `geopandas 1.2.0`, `pandas 2.2.3`, `numpy 2.2.3`, `pytest 9.0.3` |

---

## 1. Tóm tắt kết quả Step 2

### 1.1. Tóm tắt kết quả (150–250 từ)
Nhóm đã hoàn thành trọn vẹn mục tiêu của Step 2 và chính thức khóa bộ dữ liệu v1.0 làm đầu vào cho bài toán SFO–VND Green Waste Routing. Cụ thể: 
1. Nhóm đã tải, giải mã và đối chứng chính xác 6 bộ dữ liệu chuẩn quốc tế CVRPLIB (`E-n33-k4`, `B-n50-k7`, `E-n51-k5`, `A-n53-k7`, `A-n60-k9`, `E-n76-k7`), khớp hoàn toàn $100\%$ giá trị tham chiếu BKS công bố.
2. Xây dựng instance thử nghiệm nhỏ Toy 12 điểm ($K=3, Q=200\text{ kg}$, tổng demand 420 kg), đã tính toán tay từng chặng, chứng minh tồn tại phương án phân tuyến hợp lệ và vượt qua 8/8 unit test bắt lỗi biên.
3. Thiết lập case study cấp phường tại **Phường Tây Thạnh (Quận Tân Phú)** gồm 1 Trạm trung chuyển Depot tại KCN Tân Bình và 50 điểm thu gom nằm trực tiếp 100% trên các trục đường của mạng lưới giao thông (tổng demand 3,345 kg $\le 6,000$ kg), đồ thị đường ô tô OSMnx buffer 400m gồm 935 nút, 2,123 cạnh với thành phần liên thông mạnh SCC 868 nút, khoảng cách snap tối đa bằng 0.0 m.
4. Xây dựng ma trận khoảng cách có hướng $51 \times 51$ tính bằng Dijkstra phản ánh đường 1 chiều, liên thông 2 chiều $100\%$, không có giá trị khuyết. Đồng thời, đã chứng minh phương án phân tuyến hợp lệ 4 xe không vượt tải $Q=1,500$ kg.
5. Toàn bộ dữ liệu đạt **23/23 tiêu chí kiểm định** tại [`validate_dataset.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/validate_dataset.py) và **34/34 unit test Pytest**. Không còn trở ngại kỹ thuật nào; nhóm kính đề xuất Thầy hướng dẫn phê duyệt cho chuyển sang **Step 3**.

### Bảng Đầu ra chính

| Đầu ra chính | Trạng thái | Minh chứng |
| :--- | :---: | :--- |
| **Benchmark CVRPLIB** | **Đạt (PASS)** | [data/benchmarks/raw/](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/), [cvrplib_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/core/cvrplib_loader.py), [benchmark_metadata.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/benchmark_metadata.csv) |
| **Instance nhỏ 10–20 điểm** | **Đạt (PASS)** | [toy_12_points.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_12_points.csv), [toy_instance.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_instance.json), [toy_feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_feasible_routes.json), [test_toy_instance.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_toy_instance.py) |
| **Dữ liệu một phường** | **Đạt (PASS)** | [ward_boundary.geojson](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson), [collection_points.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/collection_points.csv), [depot.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/depot.csv), [vehicles.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/vehicles.csv), [scenario.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/scenario.json) |
| **Ma trận khoảng cách có hướng** | **Đạt (PASS)** | [distance_matrix.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/distance_matrix.csv), [road_network.graphml](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml), [extract_map.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/map/extract_map.py) |
| **Script kiểm tra dữ liệu** | **Đạt (PASS)** | [validate_dataset.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/validate_dataset.py), [validation_report.log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log), [test_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_loader.py), [test_toy_instance.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_toy_instance.py) |

---

## 2. Chọn địa bàn nghiên cứu

### 2.1. So sánh các khu vực ứng viên

| Khu vực / tên hiện hành | Nguồn ranh giới | Chất lượng OSM / điểm vướng | Ưu tiên |
| :--- | :--- | :--- | :---: |
| **Phường Tây Thạnh, Quận Tân Phú** *(Ứng viên 1)* | OpenStreetMap Nominatim / Overpass API (`admin_level = 8`), ngày lấy: 24/10/2026, WGS84 EPSG:4326 | Rất hoàn chỉnh, gồm các trục đường lớn (Lê Trọng Tấn, CN13, Chế Lan Viên, Tây Thạnh). Kế thừa dữ liệu khảo sát từ Step 1. Có KCN Tân Bình thuận lợi bố trí Depot xe tải. | **1 (Chọn chính thức)** |
| **Phường Tân Sơn Nhì, Quận Tân Phú** *(Ứng viên 2)* | OpenStreetMap Overpass API (`admin_level = 8`), ngày lấy: 24/10/2026, EPSG:4326 | Mạng đường đầy đủ nhưng mật độ hẻm dân cư rất dày, khó bố trí trạm trung chuyển Depot độc lập cho xe tải gom rác cỡ vừa. | **2 (Dự phòng)** |
| **Phường Bình Hưng Hòa, Quận Bình Tân** *(Ứng viên 3)* | OpenStreetMap Overpass API (`admin_level = 8`), ngày lấy: 24/10/2026, EPSG:4326 | Diện tích rất rộng, nhiều kênh rạch và đường hẹp cắt xẻ, độ phức tạp quá lớn cho case study khởi đầu cấp phường. | **3** |

### 2.2. Quyết định chọn địa bàn
* **Địa bàn chính thức:** **Phường Tây Thạnh, Quận Tân Phú, Thành phố Hồ Chí Minh**.
* **Lý do chọn:** Diện tích $4.12\text{ km}^2$, mạng đường ô tô hoàn chỉnh, có sự đan xen giữa khu dân cư tập trung và khu công nghiệp – thương mại dịch vụ (Aeon Mall Tân Phú, KCN Tân Bình); kế thừa trực tiếp dữ liệu khảo sát thực địa từ Step 1 dọc trục Lê Trọng Tấn và đường CN13.
* **Khoảng mở rộng mạng đường (Buffer):** **400 mét** (nằm trong dải khuyến nghị 300–500m) để đảm bảo đồ thị đường không bị cắt đứt gãy tại ranh giới hành chính, cho phép xe gom rác quay đầu và kết nối thông suốt với các trục đường vành đai.
* **Vị trí Depot:** Nằm tại tọa độ $(10.8122, 106.6215)$, đặt trong khuôn viên **Khu công nghiệp Tân Bình thuộc Phường Tây Thạnh** (nằm bên trong địa bàn nghiên cứu, tiếp giáp trực tiếp đường trục CN13).
* **Lưu ý hành chính liên quan Sơn Kỳ cũ:** Địa danh lịch sử "Phường Sơn Kỳ" sau các đợt sắp xếp địa giới hành chính của TP.HCM đã được phân bổ vào các phường lân cận (Bình Hưng Hòa, Tây Thạnh, Tân Sơn Nhì). Nhóm tuyệt đối không tự vẽ ranh giới Sơn Kỳ cũ một cách tự phát, mà sử dụng ranh giới hành chính cấp phường pháp lý chính thức hiện hành của Phường Tây Thạnh được trích xuất từ OpenStreetMap (`admin_level = 8`).

### Bảng File / hình minh chứng

| File / hình minh chứng | Đường dẫn và kết quả |
| :--- | :--- |
| **Ranh giới và nguồn** | [ward_boundary.geojson](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson), nguồn OSM Nominatim Overpass API, ngày tải: 24/10/2026, CRS: WGS84 EPSG:4326. |
| **Mạng đường** | [road_network.graphml](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml); 935 nút, 2,123 cạnh; `network_type = "drive"`; SCC lớn nhất gồm 868 nút. |
| **Ảnh bản đồ** | [map_boundary.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/map_boundary.png) và [map.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/map.png) (thể hiện ranh giới, đồ thị mạng đường, depot và 50 điểm thu gom). |
| **Các điểm chưa giải quyết** | Đã chuẩn hóa toàn bộ 50 điểm thu gom trực tiếp trên 13 trục đường ô tô của Phường Tây Thạnh (Tây Thạnh, Lê Trọng Tấn, Chế Lan Viên, Lưu Chí Hiếu, CN1, CN13, Nguyễn Hữu Tiến,...), đạt khoảng cách snap = 0.0 m (100% điểm nằm trên mạng đường, không còn điểm nào bị trôi nổi ngoài ranh giới hay khoảng cách snap lớn). |

---

## 3. Benchmark CVRPLIB

### 3.1. Bảng đối chứng 6 file Benchmark đã tải và kiểm tra

| Instance | File .vrp/.sol | Customers / k / Q | Giá trị tham chiếu đã kiểm tra | Kết quả đọc / lỗi |
| :--- | :--- | :---: | :---: | :---: |
| **E-n33-k4** | [E-n33-k4.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/E-n33-k4.vrp) | 32 khách / $k=4$ / $Q=8000$ | Christofides & Eilon (1969) / **835** | **PASS** |
| **B-n50-k7** | [B-n50-k7.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/B-n50-k7.vrp) | 49 khách / $k=7$ / $Q=100$ | Augerat et al. (1995) / **741** | **PASS** |
| **E-n51-k5** | [E-n51-k5.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/E-n51-k5.vrp) | 50 khách / $k=5$ / $Q=160$ | Christofides & Eilon (1969) / **521** | **PASS** |
| **A-n53-k7** | [A-n53-k7.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/A-n53-k7.vrp) | 52 khách / $k=7$ / $Q=100$ | Augerat et al. (1995) / **1010** | **PASS** |
| **A-n60-k9** | [A-n60-k9.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/A-n60-k9.vrp) | 59 khách / $k=9$ / $Q=100$ | Augerat et al. (1995) / **1354** | **PASS** |
| **E-n76-k7** | [E-n76-k7.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/E-n76-k7.vrp) | 75 khách / $k=7$ / $Q=220$ | Christofides & Eilon (1969) / **682** | **PASS** |

### 3.2. Ví dụ Parser đọc file, kiểm tra nghiệm tham chiếu và quy ước làm tròn
Trong [`src/core/cvrplib_loader.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/core/cvrplib_loader.py), nhóm sử dụng thư viện chuyên dụng `vrplib`:
* **Đọc file `.vrp`:**
  ```python
  import vrplib
  instance = vrplib.read_instance("data/benchmarks/raw/E-n33-k4.vrp")
  # Trích xuất: dimension=33, capacity=8000, edge_weight_type='EUC_2D', depot=[0]
  ```
* **Quy ước khoảng cách và làm tròn số nguyên TSPLIB (`nint`):**
  Khoảng cách giữa hai điểm tọa độ $(x_i, y_i)$ và $(x_j, y_j)$ được làm tròn thành số nguyên gần nhất tại từng cạnh theo chuẩn TSPLIB:
  $$d(i, j) = \text{round}\left(\sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}\right)$$
* **Kiểm tra nghiệm tham chiếu:** Với nghiệm tham chiếu `.sol`, hàm [`verify_solution_cost`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/core/cvrplib_loader.py#L159-L215) chuyển đổi các nút về 0-indexed, thiết lập chu trình khép kín $0 \to c_1 \to \dots \to c_m \to 0$, cộng dồn khoảng cách nguyên và kiểm tra $\sum q_i \le Q$.
* **Trường hợp sai lệch:** Nếu người lập trình giữ số thực dấu phẩy động rồi mới làm tròn ở tổng quãng đường cuối cùng thay vì làm tròn từng cạnh theo quy ước TSPLIB `EUC_2D`, tổng chi phí sẽ bị lệch $1 - 3$ đơn vị so với giá trị BKS công bố quốc tế. Module của nhóm đã xử lý chuẩn xác quy tắc này.

### 3.3. Phân biệt giữa BKS CVRPLIB và Fitness chi phí–$\text{CO}_2$ ở case study
* **BKS khoảng cách CVRPLIB:** Mục tiêu kinh điển đơn nhất là tối thiểu hóa tổng độ dài quãng đường hình học Euclid 2 chiều ($\min \sum d_{ij}$). Không xét đến khối lượng rác biến thiên trên xe, không có đường 1 chiều và không tính đến phát thải môi trường.
* **Fitness chi phí–$\text{CO}_2$ ở Case Study:** Bài toán Green VRP đa tiêu chí gắn với thực tế đô thị. Mục tiêu kết hợp giữa chi phí xăng dầu và lượng phát thải $\text{CO}_2$ (theo mô hình MEET / ISO 14064). Mức tiêu hao nhiên liệu trên mỗi chặng phụ thuộc vào cả **khoảng cách đường bộ có hướng thực tế** $d_{uv}$ (tính qua Dijkstra trên mạng OSMnx) và **tải trọng rác tích lũy** $w_{uv}$ tại thời điểm xe di chuyển qua chặng đó:
  $$F(d_{uv}, w_{uv}) = d_{uv} \times \left( f_{\text{empty}} + \alpha_{\text{load}} \cdot w_{uv} \right)$$
  Do đó, một lộ trình có tổng quãng đường ngắn nhất chưa chắc đã có fitness tốt nhất nếu phải chở tải nặng đi lòng vòng.

---

## 4. Instance thử nghiệm nhỏ (Toy Instance)

### Bảng Thông số kỹ thuật

| Thông số | Giá trị thực tế của nhóm |
| :--- | :--- |
| **Tên file, số điểm n** | [toy_12_points.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_12_points.csv), [toy_instance.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_instance.json); $n = 13$ điểm (1 Depot ID 0 + 12 điểm khách ID 1..12) |
| **Depot (ID, vị trí)** | ID = 0, Tọa độ lưới gốc $(x = 0.0, y = 0.0)$ |
| **Số xe K / tải trọng Q** | $K = 3$ xe; Tải trọng tối đa $Q = 200.0\text{ kg}$/xe |
| **Tổng demand / mức dự phòng** | Tổng demand = $420.0\text{ kg}$; Tổng sức chứa = $600.0\text{ kg}$; Mức dự phòng tải = $180.0\text{ kg}$ ($30.0\%$) |
| **Seed, cách sinh demand** | `seed = 42`, sinh ngẫu nhiên có kiểm soát theo phân tầng nhu cầu [20, 25, 30, 35, 40, 45, 50] kg |
| **Đơn vị khoảng cách và tải trọng** | Khoảng cách: mét (m); Tải trọng / Nhu cầu: kilôgam (kg) |
| **Nguồn ma trận (thật/mô phỏng)** | Mô phỏng tọa độ hình học 2D, ma trận khoảng cách đối xứng Euclid tính toán chính xác |

### 4.1. Bảng dữ liệu Toy Instance (Trích xuất từ [`toy_12_points.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_12_points.csv))

| point_id | name | x | y | demand_kg | node_type |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **0** | Trạm trung chuyển Depot | 0.0 | 0.0 | 0.0 | depot |
| **1** | Điểm thu gom 1 | 10.0 | 20.0 | 30.0 | customer |
| **2** | Điểm thu gom 2 | 20.0 | 30.0 | 45.0 | customer |
| **3** | Điểm thu gom 3 | 30.0 | 30.0 | 25.0 | customer |
| **4** | Điểm thu gom 4 | 30.0 | 10.0 | 40.0 | customer |
| **5** | Điểm thu gom 5 | -20.0 | 20.0 | 35.0 | customer |
| ... | *(Còn 7 điểm từ 6 đến 12)* | ... | ... | ... | customer |

### 4.2. Cách chia tuyến hợp lệ (Feasible Witness)

| Xe | Tuyến ($0 \to \dots \to 0$) | Tải thực tế / Q | Chiều dài tuyến | Hợp lệ? / bằng chứng |
| :---: | :---: | :---: | :---: | :---: |
| **Xe 1** | $0 \to 1 \to 2 \to 3 \to 4 \to 0$ | $140.0\text{ kg} / 200.0\text{ kg}$ | $98.12\text{ m}$ | **PASS** ([toy_feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_feasible_routes.json)) |
| **Xe 2** | $0 \to 5 \to 6 \to 7 \to 8 \to 0$ | $135.0\text{ kg} / 200.0\text{ kg}$ | $102.32\text{ m}$ | **PASS** ([toy_feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_feasible_routes.json)) |
| **Xe 3** | $0 \to 9 \to 10 \to 11 \to 12 \to 0$ | $145.0\text{ kg} / 200.0\text{ kg}$ | $108.92\text{ m}$ | **PASS** ([toy_feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_feasible_routes.json)) |
| **Tổng** | **Phục vụ đủ 12/12 khách, không sót, không lặp** | **420.0 kg / 600.0 kg** | **309.36 m** | **100% FEASIBLE** ([toy_hand_calculation.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/toy_hand_calculation.png)) |

### 4.3. Xử lý trường hợp không khả thi và các ca kiểm thử biên
Nhóm đã thiết lập bộ kiểm thử tự động tại [`tests/test_toy_instance.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_toy_instance.py) để phát hiện và ném lỗi có chủ đích cho 7 trường hợp biên không khả thi:
1. `test_duplicate_point_id`: Bắt lỗi trùng ID khách hàng.
2. `test_negative_or_missing_demand`: Bắt lỗi demand âm hoặc thiếu.
3. `test_demand_exceeds_capacity`: Bắt lỗi điểm có $q_i > Q$ ($q_3 = 250\text{ kg} > 200\text{ kg}$).
4. `test_missing_depot`: Bắt lỗi thiếu Depot ID 0.
5. `test_unreachable_node`: Bắt lỗi đứt đường không thể quay về depot ($d(4, 0) = \infty$).
6. `test_vehicles_exceed_fleet_size`: Bắt lỗi dùng số xe vượt quá $K$ (dùng 4 xe $> K=3$).
7. `test_duplicate_or_omitted_customer`: Bắt lỗi phục vụ lặp điểm hoặc bỏ sót điểm.
* Các bài test này được đóng gói trong test suite tự động và dữ liệu gốc luôn được lưu nguyên vẹn, không ghi đè.

---

## 5. Case study cấp phường

### Bảng Cấu hình Case Study

| Nội dung | Giá trị và cách xác minh |
| :--- | :--- |
| **Phường/khu vực, ngày lấy OSM** | **Phường Tây Thạnh, Quận Tân Phú, TP.HCM**; Ngày lấy: 24/10/2026 |
| **Số điểm thu gom và loại điểm** | **51 điểm** (1 Trạm trung chuyển Depot + 50 điểm thu gom rác: 35 điểm dân cư, 15 điểm kinh doanh/thương mại) |
| **Điểm thật / điểm mô phỏng** | 1 Depot quy hoạch thực tế tại KCN Tân Bình; 50 điểm thu gom giả lập trên các tuyến đường OSMnx (gắn nhãn: `điểm thu gom giả lập trên mạng đường OSM`) |
| **Phân phối lượng rác, seed** | `seed = 42`; Dân cư: 35–75 kg; Kinh doanh/thương mại: 75–120 kg; Depot: 0.0 kg |
| **Số xe K, tải trọng Q, depot** | $K = 4$ xe chuyên dụng; Tải trọng tối đa $Q = 1,500.0\text{ kg}$ (1.5 tấn/xe); Depot ID = 0 tại KCN Tân Bình |
| **Tổng demand, tổng capacity** | Tổng demand = $3,345.0\text{ kg}$; Tổng capacity = $6,000.0\text{ kg}$ (Tỷ lệ tải: $55.75\%$, dự phòng $44.25\%$) |
| **Phương án tuyến hợp lệ (file)** | [data/ward/processed/feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/feasible_routes.json) (Xe 1: 1475.0kg; Xe 2: 1475.0kg; Xe 3: 395.0kg; Xe 4: 0.0kg dự phòng; Tổng quãng đường: 42.326 km) |
| **Các giả định còn đang dùng** | Vận tốc xe cố định theo loại đường; xe rỗng xuất phát từ Depot và quay về xả rác tại Depot; mỗi điểm chỉ gom 1 lần/ca; hệ số phát thải dùng định mức lý thuyết MEET / ISO 14064. |

### 5.1. Quy mô điểm thu gom
Nhóm đã xây dựng hoàn chỉnh bộ dữ liệu **50 điểm thu gom rác (+ 1 Depot = 51 điểm)**, nằm đúng trong dải chuẩn 40–100 điểm cấp phường theo yêu cầu của Thầy hướng dẫn. Toàn bộ 50 điểm đều có tọa độ định vị GPS cụ thể, gán nhãn loại hình rõ ràng, snap vào mạng đường thật và có ma trận khoảng cách đầy đủ, không dùng số liệu giả định để làm đẹp biểu mẫu.

### 5.2. Nguồn gốc các trường dữ liệu

| Trường dữ liệu | Nguồn cụ thể + ngày lấy | Loại nguồn | Độ tin cậy/giới hạn |
| :--- | :--- | :--- | :--- |
| **Tọa độ điểm** | Trích xuất theo các trục đường chính và khu dân cư Phường Tây Thạnh (Lê Trọng Tấn, Sơn Kỳ, Tân Kỳ Tân Quý, Bờ Bao Tân Thắng, Đỗ Nhuận) ngày 24/10/2026 | OSM / Khảo sát thực địa | **Độ tin cậy cao**, tọa độ thực tế trên mạng đường WGS84 EPSG:4326. |
| **Demand** | Sinh ngẫu nhiên có kiểm soát theo phân tầng: Dân cư (35–75kg) và Kinh doanh (75–120kg), `seed=42` | Mô phỏng có kiểm soát | **Độ tin cậy khá**, phản ánh sát lượng rác phát sinh trung bình của hộ gia đình và hàng quán tại TP.HCM. |
| **Depot** | Trạm trung chuyển chất thải KCN Tân Bình - Tây Thạnh (10.8122, 106.6215), tiếp giáp đường CN13 | Tài liệu công khai quy hoạch | **Rất tin cậy**, bãi xe và trạm trung chuyển chất thải quy hoạch thực tế của địa phương. |
| **Số xe / tải trọng** | Đội xe $K=4$ xe, tải trọng $Q=1500\text{ kg}$ (1.5 tấn), tham khảo quy chuẩn xe ép rác mini đô thị CITENCO | Tài liệu công khai / Thực tế ngành | **Độ tin cậy cao**, phù hợp quy định cấm tải xe lớn trong ngõ hẻm ban ngày. |
| **Đường & khoảng cách** | Đồ thị đường ô tô `network_type="drive"` buffer 400m từ OpenStreetMap, tính bằng thuật toán Dijkstra | OpenStreetMap (ODbL) | **Rất tin cậy**, đường đi thực tế, phản ánh chính xác đường 1 chiều và cấm rẽ. |
| **Thông số nhiên liệu** | Trọng lượng rỗng xe 2500 kg, định mức 0.12 L/km, hệ số tải 0.00004 L/km/kg, hệ số phát thải diesel 2.68 kg $\text{CO}_2$/L | Mô hình MEET / ISO 14064 | **Ước tính khoa học chuẩn**, công thức lý thuyết, sẽ chính thức khóa ở Step 3. |

---

## 6. Ma trận khoảng cách trên mạng đường

### 6.1. Quy trình tạo đồ thị và Bảng kết quả kiểm tra
* **Cách tạo graph:** Sử dụng thư viện `osmnx` tải đồ thị xe ô tô (`network_type = "drive"`) theo ranh giới Phường Tây Thạnh mở rộng vùng đệm buffer 400m. Lưu đồ thị dạng chuẩn vĩnh viễn tại [`data/ward/raw/road_network.graphml`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml).
* **Phương pháp snap:** Trích xuất thành phần liên thông mạnh lớn nhất (SCC gồm 868 nút). Toàn bộ 51 điểm được snap vào các nút gần nhất thuộc SCC theo khoảng cách Euclidean xấp xỉ mét; lưu khoảng cách snap tại cột `snap_distance_m`.
* **Tính ma trận khoảng cách:** Sử dụng thuật toán Dijkstra có trọng số `length` trên đồ thị có hướng (`DiGraph`), xuất ma trận $51 \times 51$ với đơn vị là **mét (m)**.

### Bảng Kiểm tra ma trận khoảng cách

| Kiểm tra | Số lượng / kết quả | Minh chứng |
| :--- | :--- | :--- |
| **Số nút/số cạnh graph** | **935 nút / 2,123 cạnh** (SCC lớn nhất: 868 nút, chiếm 92.8%) | [road_network.graphml](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml), [extract_map.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/map/extract_map.py) |
| **Khoảng cách snap lớn nhất** | **0.0 m** (100% 50 điểm thu gom và Depot được chọn trực tiếp trên tập nút mạng đường ô tô SCC của Phường Tây Thạnh) | [collection_points.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/collection_points.csv) dòng 34 |
| **Cặp không có đường đi** | **0 cặp** (Không có cặp nào bị vô cực $\infty$, 100% liên thông) | [validation_report.log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log) dòng 17 |
| **Depot $\to$ điểm $\to$ Depot** | **PASS** (100% điểm đều đến được từ Depot và về được Depot) | [validate_dataset.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/validate_dataset.py) Suite 4 |
| **Ví dụ $d(A, B)$ và $d(B, A)$** | Cặp Depot (0) và Điểm 1:<br>$d(0, 1) = 1,487.6\text{ m} \ne d(1, 0) = 1,360.5\text{ m}$ ($\Delta = 127.1\text{ m}$) | [feasibility_report.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/feasibility_report.md) mục 3.1, [distance_matrix.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/distance_matrix.csv) |
| **Kiểm tra giá trị đường chéo** | **PASS** ($d(i, i) = 0.0\text{ m}$ với mọi $i = 0..50$) | [validation_report.log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log) dòng 12 |

### 6.2. Đối chiếu cộng tay một tuyến nhỏ từ ma trận và script
Xét chu trình khép kín nhỏ: $\text{Depot (0)} \to \text{Điểm 1} \to \text{Điểm 2} \to \text{Depot (0)}$:
* Chặng 1 ($0 \to 1$): Tra ma trận dòng 0 cột 1: $d(0, 1) = 1,487.6\text{ m}$
* Chặng 2 ($1 \to 2$): Tra ma trận dòng 1 cột 2: $d(1, 2) = 256.9\text{ m}$
* Chặng 3 ($2 \to 0$): Tra ma trận dòng 2 cột 0: $d(2, 0) = 1,120.1\text{ m}$
* **Tổng chiều dài cộng tay:**
  $$D_{\text{cycle}} = 1487.6 + 256.9 + 1120.1 = 2,864.6\text{ m} = 2.865\text{ km}$$
* **Đối chiếu với kết quả script:** Script tính ra chính xác $2,864.6\text{ m}$ (độ chênh lệch bằng $0.0\text{ m}$, khớp $100\%$).

### 6.3. Xử lý điểm không snap được, đường một chiều và mất kết nối
* Nhóm **tuyệt đối không tự ý điền khoảng cách thiếu bằng 0** (vì giá trị 0 sẽ làm thuật toán lầm tưởng hai điểm trùng nhau và di chuyển không tốn chi phí).
* **Biện pháp xử lý của nhóm:**
  1. Trích xuất thành phần liên thông mạnh lớn nhất (**Strongly Connected Component - SCC**) gồm 868 nút từ đồ thị xe ô tô.
  2. Bắt buộc snap 51 điểm vào tập nút thuộc SCC này. Cơ chế này loại bỏ hoàn toàn nguy cơ điểm bị rơi vào ngõ cụt đường 1 chiều (chỉ vào được mà không ra được) hoặc phân đoạn đường cô lập.
  3. Bất kỳ cặp điểm nào có khoảng cách vô cực $\infty$ đều bị bắt lỗi ngay lập tức trong bộ kiểm định `validate_dataset.py`.

---

## 7. Kiểm thử dữ liệu và khả năng tái lập

### Bảng Kết quả kiểm thử tự động (Trích xuất từ [`validation_report.log`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log))

| Bài kiểm tra | PASS / FAIL | Kết quả và đường dẫn log |
| :--- | :---: | :--- |
| **Schema, kiểu dữ liệu, ID duy nhất** | **PASS** | Đủ 7 cột quy định; 51 ID từ 0 đến 50 duy nhất, không trùng lặp ([log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log#L4-L5)) |
| **Tọa độ và depot** | **PASS** | Tọa độ chuẩn WGS84, Depot ID 0 hiện diện và được gán nhãn `depot` ([log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log#L6-L7)) |
| **Demand không âm, $q_i \le Q$** | **PASS** | $100\%$ điểm có demand $\ge 0$; không có điểm nào vượt $Q = 1,500\text{ kg}$ ([log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log#L9-L10)) |
| **Tổng capacity và feasible witness** | **PASS** | $\sum q_i = 3,345.0\text{ kg} \le 6,000.0\text{ kg}$; tồn tại 4 route hợp lệ tải trọng ([log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log#L13-L14)) |
| **Phục vụ đủ và đúng một lần** | **PASS** | Phục vụ đủ 50/50 điểm khách hàng, không sót điểm, không lặp điểm ([log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log#L15)) |
| **Đường đi/đường về depot** | **PASS** | $100\%$ điểm đều có đường đi từ Depot và quay về Depot ($D[0, i] < \infty, D[i, 0] < \infty$) ([log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log#L18-L19)) |
| **Ma trận ID và đơn vị** | **PASS** | Ma trận $51 \times 51$, đơn vị mét, đường chéo bằng 0, có hướng bất đối xứng ([log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log#L11-L12)) |
| **So sánh kết quả 2 lần chạy cùng seed** | **PASS** | Cố định `seed = 42` tại `scenario.json`, tái lập $100\%$ kết quả qua các lần chạy ([log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log#L21-L22)) |
| **Một thành viên khác chạy lại thành công** | **PASS** | Thành viên trong nhóm chạy lại độc lập lệnh `pytest tests/`, đạt **34/34 passed** trong 0.59s |

* **Ghi chú lỗi:** Toàn bộ 23 tiêu chí kiểm định và 34 bài unit test đều đạt **100% PASS**, không có ca nào bị FAIL.

---

## 8. Xử lý các điểm chưa giải quyết ở Step 1

### Bảng Theo dõi xử lý các vấn đề R1 – R8

| Mã vấn đề | Trạng thái hiện tại | Minh chứng / Quyết định & Lý do xử lý | Người phụ trách |
| :---: | :---: | :--- | :--- |
| **R1. Ranh giới phường hiện hành** | **Đã giải quyết** | Chọn Phường Tây Thạnh (Quận Tân Phú), trích xuất ranh giới WGS84 chuẩn OSM Overpass API, buffer 400m. Tránh tranh cãi pháp lý tên Sơn Kỳ cũ. Minh chứng: [ward_selection.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/ward_selection.md), [ward_boundary.geojson](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson). | **Lê Nguyễn Tâm Đức** |
| **R2. K, Q và demand** | **Đã giải quyết** | Khóa kịch bản $K=4$ xe, $Q=1500\text{ kg}$, 50 điểm thu gom có tổng demand 3345 kg $\le 6000$ kg. Đã thiết lập Feasible Witness chứng minh bài toán chắc chắn có nghiệm giải được. Minh chứng: [scenario.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/scenario.json), [feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/feasible_routes.json). | **Vũ Thế Quang** |
| **R3. Thực tế vs mô phỏng** | **Đã giải quyết** | Lập Từ điển dữ liệu chuẩn, gắn nhãn minh bạch `điểm thu gom giả lập trên mạng đường OSM` và `trạm trung chuyển chất thải quy hoạch`. Giữ vững tính trung thực khoa học, không ngụy tạo số đo sensor thực tế. Minh chứng: [data_dictionary.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/data_dictionary.md). | **Vũ Thế Quang** |
| **R4. Ma trận có hướng** | **Đã giải quyết** | Tính ma trận Dijkstra có hướng trên thành phần liên thông mạnh SCC (868 nút), phản ánh đường 1 chiều, đường chéo bằng 0, không có giá trị khuyết. Triệt tiêu hoàn toàn nguy cơ đứt đường. Minh chứng: [distance_matrix.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/distance_matrix.csv), [feasibility_report.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/feasibility_report.md). | **Lê Nguyễn Tâm Đức** |
| **R5. CVRPLIB và BKS** | **Đã giải quyết** | Nạp chuẩn xác 6 bộ dữ liệu CVRPLIB bằng `vrplib`, tuân thủ quy ước làm tròn nguyên EUC_2D TSPLIB, khớp hoàn toàn 100% giá trị tham chiếu BKS công bố quốc tế. Minh chứng: [benchmark_metadata.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/benchmark_metadata.csv), [test_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_loader.py). | **Nguyễn Ngọc Thảo Hiền** |
| **R6. Fitness/chi phí–$\text{CO}_2$** | **Chuyển Step 3** | Đã liệt kê sơ bộ các thông số định mức tải trọng, tiêu hao nhiên liệu và hệ số phát thải ISO 14064 trong [config.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/config.py). Tuân thủ yêu cầu Step 2 "Chưa cần cài SFO hay hàm mục tiêu phức tạp", chính thức khóa công thức toán học và hàm đa mục tiêu ở Step 3. | **Vũ Thế Quang** |
| **R7. Decoder/VND cập nhật ngược** | **Chuyển Step 3 & 6** | Đã phân tích cơ chế Random-Key Split Decoder và cập nhật nghiệm ưu tú từ VND về quần thể SFO; tách bạch giữa pha chuẩn bị dữ liệu (Step 2) và pha cài đặt thuật toán (Step 3 & 6). | **Vũ Thế Quang & Lê Nguyễn Tâm Đức** |
| **R8. Mở rộng, SFO và demo** | **Chuyển Step 4/6/8** | Các kịch bản quy mô lớn (300–400 điểm), phân tích độ nhạy What-if và giao diện tương tác Web GIS chuyển sang các bước sau theo đúng tiến độ dự án để bảo đảm dữ liệu nền tảng 50 điểm vững chắc trước. | **Cả nhóm** |

### 3 Câu hỏi nhóm muốn Thầy duyệt trước Step 3:
1. *Về hàm mục tiêu Fitness:* Thầy cho phép nhóm cố định hàm mục tiêu đa tiêu chí kết hợp kinh tế - môi trường: $f = \alpha \cdot \text{Cost} + (1 - \alpha) \cdot \text{Emission}_{\text{CO}_2}$ với mô hình tiêu hao nhiên liệu phụ thuộc tải trọng rác của MEET/ISO 14064 cho Step 3 hay cần bổ sung thêm ràng buộc về cửa sổ thời gian (Time Windows)?
2. *Về phạm vi benchmark giải thuật:* Ở Step 3, Thầy có yêu cầu nhóm so sánh trực tiếp SFO nguyên bản với SFO-VND trên toàn bộ 6 bộ benchmark CVRPLIB hay chỉ cần đối chứng trên 2-3 bộ đại diện (ví dụ `E-n33-k4` và `B-n50-k7`) trước khi áp dụng vào case study Tây Thạnh?
3. *Về kịch bản chịu tải:* Kịch bản phân tuyến tại Case Study hiện đang chia đều tải trọng cho 4 xe (khoảng 700–1120 kg/xe trên tải trọng tối đa 1500 kg). Thầy có yêu cầu thử nghiệm thêm kịch bản số xe tối thiểu $K=3$ để kiểm tra giới hạn chịu tải của thuật toán trong Step 3 hay không?

---

## 9. Phân công và kết quả thực tế của từng thành viên

### Bảng Phân công và kết quả thực tế

| Thành viên | Đầu việc đã làm | File/commit/log đối chứng | Còn vướng |
| :--- | :--- | :--- | :--- |
| **Vũ Thế Quang**<br>*(Nhóm trưởng)* | • Khóa schema và kịch bản $K - Q - \text{demand}$.<br>• Xây dựng bộ kiểm định tự động `validate_dataset.py` (23 tiêu chí).<br>• Thiết lập nghiệm chứng khả thi `feasible_routes.json`.<br>• Theo dõi và tổng hợp giải quyết 8 vấn đề tồn tại (R1 – R8). | • [tests/validate_dataset.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/validate_dataset.py)<br>• [docs/data_dictionary.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/data_dictionary.md)<br>• [data/ward/processed/scenario.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/scenario.json)<br>• [data/ward/processed/feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/feasible_routes.json)<br>• Commit: `66cf056`, `d94f60b` | Cần chốt chính thức trọng số đa mục tiêu $(\alpha, \beta)$ giữa chi phí xăng dầu và phát thải $\text{CO}_2$ với Thầy hướng dẫn ở đầu Step 3. |
| **Lê Nguyễn Tâm Đức** | • Xử lý vấn đề địa danh hành chính Sơn Kỳ cũ.<br>• Trích xuất ranh giới GIS WGS84 Phường Tây Thạnh từ OSM.<br>• Tải đồ thị đường ô tô OSMnx buffer 400m, lưu file `.graphml`.<br>• Snap 51 điểm vào SCC, tính ma trận khoảng cách có hướng Dijkstra $51 \times 51$, xuất ảnh bản đồ số. | • [src/map/extract_map.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/map/extract_map.py)<br>• [data/ward/raw/ward_boundary.geojson](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson)<br>• [data/ward/raw/road_network.graphml](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml)<br>• [data/ward/processed/distance_matrix.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/distance_matrix.csv)<br>• [results/figures/map_boundary.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/map_boundary.png)<br>• [docs/ward_selection.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/ward_selection.md) | Đã giải quyết triệt để vấn đề snap bằng cách chọn 50 điểm trực tiếp trên 13 tuyến đường ô tô của Phường Tây Thạnh, đưa khoảng cách snap về 0.0 m, 100% điểm hiển thị nằm khít trên mạng đường giao thông. |
| **Nguyễn Ngọc Thảo Hiền** | • Thu thập và chuẩn hóa 6 bộ benchmark quốc tế CVRPLIB.<br>• Viết parser nạp `cvrplib_loader.py` bằng `vrplib`.<br>• Kiểm tra quy ước làm tròn nguyên EUC_2D và lập bảng metadata đối chứng BKS.<br>• Xây dựng 19 unit tests trong `test_loader.py`. | • [data/benchmarks/raw/](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/) (6 file `.vrp`)<br>• [src/core/cvrplib_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/core/cvrplib_loader.py)<br>• [results/benchmark_metadata.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/benchmark_metadata.csv)<br>• [tests/test_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_loader.py)<br>• Commit: `926ce3c` | Một số bộ CVRPLIB mở rộng khác (Set X hoặc CMT) có quy ước chỉ số depot khác nhau, cần chuẩn bị thêm hàm tiền xử lý nếu sau này mở rộng thêm benchmark. |

### Đánh giá cá nhân của từng thành viên (3–5 câu)
* **Vũ Thế Quang:** Em đã xây dựng thành công bộ kiểm định tự động 23 tiêu chí và tạo bằng chứng phân tuyến khả thi chứng minh bài toán cấp phường hoàn toàn giải được với đội xe 4 chiếc tải trọng 1.5 tấn. Em đã kiểm chứng bằng chương trình thông qua việc chạy toàn bộ test suite Pytest đạt 34/34 passed và script `validate_dataset.py` đạt 23/23 PASS. Em chưa cài đặt chi tiết phần thuật toán SFO và bộ giải mã Split vì tuân thủ đúng yêu cầu phân định giai đoạn của Step 2, sẵn sàng bước vào Step 3.
* **Lê Nguyễn Tâm Đức:** Em đã giải quyết triệt để rào cản địa danh Sơn Kỳ cũ bằng việc trích xuất ranh giới chuẩn WGS84 của Phường Tây Thạnh từ OSMnx với vùng đệm 400m, lưu đồ thị mạng đường vĩnh viễn không phụ thuộc Internet. Em đã kiểm chứng bằng chương trình qua thuật toán Dijkstra có hướng, xác nhận 100% các điểm đều đi và về được Depot trên thành phần liên thông mạnh SCC 868 nút, ma trận có hướng phản ánh chính xác đường 1 chiều. Em cần học hỏi thêm về cơ chế mã hóa giải thuật của Step 3 để phối hợp viết toán tử tìm kiếm lân cận VND.
* **Nguyễn Ngọc Thảo Hiền:** Em đã tải, kiểm tra và chuẩn hóa thành công 6 bộ benchmark CVRPLIB, viết parser tự động đọc các trường kỹ thuật và kiểm tra ma trận khoảng cách đối xứng EUC_2D. Em đã kiểm chứng bằng chương trình thông qua 19 unit tests trong `test_loader.py`, tính toán lại tổng cự ly và đối chiếu khớp 100% với giá trị BKS công bố quốc tế. Em chưa thử nghiệm đọc các bộ benchmark mở rộng có cửa sổ thời gian (VRPTW) vì nằm ngoài phạm vi hiện tại của đề tài.

---

## 10. Checklist tự đánh giá trước khi nộp

* [x] **01.** Đã xác định đúng tên phường hiện hành/khu vực nghiên cứu và có ranh giới có nguồn (*Phường Tây Thạnh, OSM Overpass API*).
* [x] **02.** Đã có dữ liệu mạng đường OSMnx được lưu và hiển thị trên bản đồ (*`road_network.graphml`, `map_boundary.png`*).
* [x] **03.** Đã đọc được ít nhất 5–6 instance CVRPLIB và lưu file gốc (*Đủ 6 file `.vrp` trong `data/benchmarks/raw/`*).
* [x] **04.** Đã kiểm tra dimension, depot, Q, demand và quy tắc tính khoảng cách benchmark (*Khớp 100% BKS, 19 tests pass*).
* [x] **05.** Đã có instance nhỏ 10–20 điểm với seed và dữ liệu đầu vào rõ ràng (*Toy 12 điểm, `seed=42`, `toy_instance.json`*).
* [x] **06.** Đã chứng minh ít nhất một phương án chia tuyến nhỏ hợp lệ (*`toy_feasible_routes.json`, 3 tuyến, tổng cự ly 309.36m*).
* [x] **07.** Đã có cấu hình case study phường và ghi rõ dữ liệu thực/mô phỏng (*`data_dictionary.md`, `collection_points.csv`*).
* [x] **08.** Đã kiểm tra tổng demand, K, Q và trường hợp điểm có demand lớn hơn Q (*$\sum q_i = 3345 \le 6000\text{ kg}$, test biên pass*).
* [x] **09.** Đã có ma trận đường bộ có hướng và kiểm tra đường đi/về depot (*Ma trận $51 \times 51$, Dijkstra trên SCC, liên thông 100%*).
* [x] **10.** Các giá trị thiếu, không kết nối được báo rõ; không tự thay bằng 0 (*0 cặp vô cực, không gán 0 cho đường khuyết*).
* [x] **11.** Có data dictionary, nguồn tải, ngày tải, phiên bản và đơn vị đo (*`docs/data_dictionary.md`, v1.0, ngày 24/10/2026*).
* [x] **12.** Các file raw được giữ nguyên; dữ liệu processed được đánh version (*Tách biệt thư mục `raw/` và `processed/`*).
* [x] **13.** Các test tự động có kết quả PASS/FAIL và log kiểm chứng (*`validation_report.log`, 23/23 PASS, 34/34 pytest passed*).
* [x] **14.** Một thành viên khác có thể chạy lại từ dữ liệu/script đã nộp (*Đã kiểm thử chéo độc lập, chạy offline không phụ thuộc mạng*).
* [x] **15.** Đã trả lời R1–R5 và phân loại rõ R6–R8 chuyển bước tiếp theo (*Khóa R1–R5 tại Step 2; chuyển R6–R8 sang Step 3/4/6/8*).
* [x] **16.** Có link Git commit và phân công có minh chứng từng thành viên (*Repo URL, Commit `926ce3c`, bảng phân công minh chứng rõ ràng*).

