# SFO–VND GREEN WASTE ROUTING / MẪU BÁO CÁO STEP 2
**Tài liệu giao việc và nghiệm thu nội bộ • Trang 1 – 5**  
**BIỂU MẪU NHÓM SINH VIÊN TỰ ĐIỀN**

---

# BÁO CÁO STEP 2 — CHUẨN BỊ VÀ KHÓA BỘ DỮ LIỆU
**Nhóm Gom Rác — Đề tài SFO–VND Green Waste Routing**

> [!NOTE]
> **Cách điền:** Báo cáo kết quả nhóm đã thực hiện, không chép lại hướng dẫn. Mỗi kết luận cần kèm minh chứng (tên file, ảnh, kết quả chạy, commit). Nội dung chưa hoàn thành thì ghi rõ “chưa hoàn thành” và nguyên nhân.

---

### Bảng Thông tin chung

| Thông tin | Nhóm điền |
| :--- | :--- |
| **Cơ sở đào tạo** | **Trường Đại học Công Thương Thành phố Hồ Chí Minh (HUIT)**<br>*(Khoa Công nghệ Thông tin — Chuyên ngành Khoa học Dữ liệu)* |
| **Thành viên/nhóm trưởng** | 1. **Vũ Thế Quang** *(Nhóm trưởng)*<br>2. **Lê Nguyễn Tâm Đức**<br>3. **Nguyễn Ngọc Thảo Hiền** |
| **Ngày nộp / số phiên bản** | 14/11/2026 / **Phiên bản dữ liệu v1.0 (Khóa Step 2)** |
| **Git repository/commit** | • Repository: [`https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting.git`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting)<br>• Commit mới nhất: [`f56e1c9`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/commit/f56e1c9) (*Completed Step 2*)<br>• Commit kiểm thử độc lập của Hiền: [`56452dc`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/commit/56452dc) (*Add files via upload*) |
| **Máy và môi trường thực thi** | • Môi trường phát triển chính: Windows 11 Pro 64-bit, Intel Core i7, 16GB RAM, Python 3.13.14<br>• Môi trường kiểm thử tái lập độc lập (Nguyễn Ngọc Thảo Hiền): Windows 11 Home, Python 3.12.10<br>• Thư viện cốt lõi (khớp `requirements.txt`): `osmnx 2.1.1`, `vrplib 2.2.0`, `networkx 3.6.1`, `geopandas 1.2.0`, `pandas 3.0.3`, `numpy 2.4.5`, `matplotlib 3.10.9`, `folium 0.20.0`, `pytest 9.0.3` |

---

## 1. Tóm tắt kết quả Step 2

### 1.1. Tóm tắt kết quả (150–250 từ)

Trong Step 2, nhóm đã hoàn tất việc chuẩn hóa và khóa các bộ dữ liệu đầu vào theo đúng cấu trúc thư mục dự án, tách biệt rõ giữa dữ liệu gốc (raw) và dữ liệu đã xử lý (processed). Đối với hạng mục dữ liệu chuẩn quốc tế CVRPLIB do Nguyễn Ngọc Thảo Hiền phụ trách, nhóm đã tải đầy đủ 6 cặp tệp đề bài (`.vrp`) và nghiệm tham chiếu (`.sol`) gồm `E-n33-k4`, `B-n50-k7`, `E-n51-k5`, `A-n53-k7`, `A-n60-k9` và `E-n76-k7` lưu tại [`data/benchmarks/raw/`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/tree/main/data/benchmarks/raw/). Nhóm đã xây dựng bộ đọc tự động [`src/core/cvrplib_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/cvrplib_loader.py), lập bảng tổng hợp thông số [`results/benchmark_metadata.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/benchmark_metadata.csv) và thiết lập bộ kiểm thử [`tests/test_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_loader.py). Kết quả kiểm tra bằng chương trình xác nhận cả 6 bộ đều đọc đúng số điểm, tải trọng $Q$, vị trí kho ($\text{depot} = 0$), đi qua đủ $n - 1$ khách hàng và khi tính lại tổng độ dài theo quy ước làm tròn số nguyên từng cạnh EUC_2D đều khớp 100% với giá trị BKS công bố. Song song đó, bộ thử nghiệm nhỏ (Toy Instance 12 điểm) và dữ liệu thực tế phường Tây Thạnh (50 điểm thu gom kèm ma trận khoảng cách đường bộ có hướng Dijkstra $51 \times 51$) cũng đã được kiểm chứng phương án phân tuyến hợp lệ. Toàn bộ 40/40 bài kiểm thử pytest đều đạt PASS khi chạy tái lập độc lập ([`results/pytest_reproduce_hien.txt`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/pytest_reproduce_hien.txt)). Hiện dữ liệu không còn vướng mắc kỹ thuật nào, nhóm đề xuất giảng viên cho phép chuyển sang Step 3.

### Bảng Đầu ra chính

| Đầu ra chính | Trạng thái | Minh chứng (Đường dẫn Git & File nội bộ) |
| :--- | :---: | :--- |
| **Benchmark CVRPLIB** | **Đạt (PASS)** | • Thư mục dữ liệu: [`data/benchmarks/raw/`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/tree/main/data/benchmarks/raw/)<br>• Module nạp dữ liệu: [`src/core/cvrplib_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/cvrplib_loader.py)<br>• Bảng metadata đối chứng: [`results/benchmark_metadata.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/benchmark_metadata.csv)<br>• Test kiểm tra 25 ca: [`tests/test_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_loader.py) |
| **Instance nhỏ 10–20 điểm** | **Đạt (PASS)** | • Tọa độ và nhu cầu 12 điểm: [`data/toy/toy_12_points.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_12_points.csv)<br>• Cấu hình bài toán: [`data/toy/toy_instance.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_instance.json)<br>• Nghiệm mẫu khả thi (Feasible Witness): [`data/toy/toy_feasible_routes.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_feasible_routes.json)<br>• Kiểm thử biên: [`tests/test_toy_instance.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_toy_instance.py) |
| **Dữ liệu một phường** | **Đạt (PASS)** | • Ranh giới GIS WGS84: [`data/ward/raw/ward_boundary.geojson`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/ward_boundary.geojson)<br>• Danh sách 50 điểm thu gom: [`data/ward/processed/collection_points.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/collection_points.csv)<br>• Trạm trung chuyển Depot: [`data/ward/processed/depot.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/depot.csv)<br>• Đội xe thu gom: [`data/ward/processed/vehicles.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/vehicles.csv)<br>• Kịch bản nghiên cứu: [`data/ward/processed/scenario.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/scenario.json) |
| **Ma trận khoảng cách có hướng** | **Đạt (PASS)** | • Ma trận khoảng cách $51 \times 51$: [`data/ward/processed/distance_matrix.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/distance_matrix.csv)<br>• Đồ thị mạng đường ô tô: [`data/ward/raw/road_network.graphml`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/road_network.graphml)<br>• Script trích xuất và tính Dijkstra: [`src/map/extract_map.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/map/extract_map.py) |
| **Script kiểm tra dữ liệu** | **Đạt (PASS)** | • Bộ kiểm định chất lượng (24 tiêu chí): [`tests/validate_dataset.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/validate_dataset.py)<br>• File log kiểm định: [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log)<br>• Bộ test nạp và ma trận: [`tests/test_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_loader.py)<br>• Bộ test biên mô hình Toy: [`tests/test_toy_instance.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_toy_instance.py) |

---

## 2. Chọn địa bàn nghiên cứu

### 2.1. So sánh các khu vực ứng viên

> *Ghi chú: Không dùng tên phường cũ nếu không giải thích ranh giới tương ứng.*

| Khu vực / tên hiện hành | Nguồn ranh giới | Chất lượng OSM / điểm vướng | Ưu tiên |
| :--- | :--- | :--- | :---: |
| **Phường Tây Thạnh, Quận Tân Phú** *(Ứng viên 1)* | OpenStreetMap Nominatim / Overpass API (`admin_level = 8`), ngày lấy: 24/10/2026, Hệ tọa độ WGS84 EPSG:4326 | Rất hoàn chỉnh, gồm các trục đường xương sống lớn (Lê Trọng Tấn, Chế Lan Viên, Tây Thạnh, CN1, CN13). Kế thừa dữ liệu khảo sát từ Step 1. Có Khu công nghiệp Tân Bình thuận lợi bố trí Trạm trung chuyển Depot xe tải. Mạng lưới đường ô tô thông suốt, tính liên thông mạnh đạt 92.8%. | **1 (Chọn chính thức)** |
| **Phường Tân Sơn Nhì, Quận Tân Phú** *(Ứng viên 2)* | OpenStreetMap Overpass API (`admin_level = 8`), ngày lấy: 24/10/2026, EPSG:4326 | Mạng đường đầy đủ nhưng mật độ ngõ hẻm dân cư nhỏ rất dày đặc, khó bố trí trạm trung chuyển Depot độc lập cho xe ép rác chuyên dụng cỡ vừa mà không gây ách tắc giao thông. | **2 (Dự phòng)** |
| **Phường Bình Hưng Hòa, Quận Bình Tân** *(Ứng viên 3)* | OpenStreetMap Overpass API (`admin_level = 8`), ngày lấy: 24/10/2026, EPSG:4326 | Diện tích địa bàn quá rộng, nhiều phân đoạn đường cắt xẻ bởi kênh rạch và nghĩa trang, mức độ phức tạp giao thông quá lớn cho một case study khởi đầu cấp phường. | **3** |

### 2.2. Quyết định chọn địa bàn
* **Địa bàn chính thức:** **Phường Tây Thạnh, Quận Tân Phú, Thành phố Hồ Chí Minh**.
* **Lý do chọn:** Diện tích $4.12\text{ km}^2$, mạng đường giao thông cho xe cơ giới hoàn chỉnh, có sự đan xen hài hòa giữa khu dân cư sinh hoạt tập trung và khu công nghiệp – dịch vụ thương mại (Aeon Mall Tân Phú, KCN Tân Bình); kế thừa trực tiếp dữ liệu khảo sát thực địa từ Step 1 dọc trục Lê Trọng Tấn và trục đường CN13.
* **Khoảng mở rộng mạng đường (Buffer):** **400 mét** (nằm trong dải khuyến nghị kỹ thuật 300–500m) nhằm bảo đảm đồ thị đường không bị đứt gãy tại đường biên ranh giới hành chính, cho phép xe gom rác thực hiện các thao tác quay đầu và kết nối liên hoàn với các trục đường vành đai bao quanh phường.
* **Vị trí Depot:** Tọa độ $(10.8122, 106.6215)$, đặt trong khuôn viên **Khu công nghiệp Tân Bình thuộc địa phận Phường Tây Thạnh** (nằm bên trong địa bàn nghiên cứu, tiếp giáp trực tiếp đường trục CN13).
* **Lưu ý hành chính liên quan Sơn Kỳ cũ:** Địa danh lịch sử "Phường Sơn Kỳ" sau các đợt điều chỉnh địa giới hành chính của TP.HCM đã được sắp xếp, phân chia một phần về Phường Tây Thạnh và Phường Sơn Kỳ hiện hữu (cùng Phường Tân Sơn Nhì, Bình Hưng Hòa). Nhóm tuyệt đối không tự vẽ ranh giới Sơn Kỳ cũ một cách tự phát, mà sử dụng ranh giới hành chính cấp phường pháp lý chính thức hiện hành của Phường Tây Thạnh được trích xuất từ OpenStreetMap (`admin_level = 8`). Báo cáo phân tích ranh giới chi tiết xem tại [`docs/reports/ward_selection.md`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/docs/reports/ward_selection.md).

### Bảng File / hình minh chứng

| File / hình minh chứng | Đường dẫn Git & Kết quả kỹ thuật |
| :--- | :--- |
| **Ranh giới và nguồn** | [`data/ward/raw/ward_boundary.geojson`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/ward_boundary.geojson), nguồn OSM Nominatim Overpass API, ngày tải: 24/10/2026, CRS: WGS84 EPSG:4326. |
| **Mạng đường** | [`data/ward/raw/road_network.graphml`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/road_network.graphml); tổng 935 nút, 2,123 cạnh; chế độ `network_type = "drive"`; thành phần liên thông mạnh nhất (SCC) gồm 868 nút. |
| **Ảnh bản đồ** | [`results/figures/map_boundary.png`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/figures/map_boundary.png) và [`results/figures/map.png`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/figures/map.png) (thể hiện ranh giới phường, mạng đường, vị trí depot và 50 điểm thu gom; hình ảnh được dán tại Phụ lục). |
| **Các điểm chưa giải quyết** | Đã giải quyết triệt để: Toàn bộ 50 điểm thu gom được chuẩn hóa trực tiếp trên 13 trục đường ô tô của Phường Tây Thạnh (Tây Thạnh, Lê Trọng Tấn, Chế Lan Viên, Lưu Chí Hiếu, CN1, CN13, Nguyễn Hữu Tiến,...), khoảng cách snap lớn nhất bằng **0.0 m** (100% điểm nằm khít trên đồ thị mạng đường, không có điểm nào bị trôi nổi ngoài ranh giới hay không thể tiếp cận). |

---

## 3. Benchmark CVRPLIB

### 3.1. Danh sách 6 file Benchmark CVRPLIB đã tải và đối chứng

> *Ghi chú: Toàn bộ file gốc `.vrp` và `.sol` được tải trực tiếp từ PUC-Rio CVRPLIB, lưu trữ nguyên vẹn tại thư mục [`data/benchmarks/raw/`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/tree/main/data/benchmarks/raw/) và đối chứng độc lập qua test suite tự động.*

| Instance | File .vrp / .sol (Nguồn & Repo) | Customers / k / Q | Giá trị tham chiếu đã kiểm tra (BKS) | Kết quả đọc / lỗi |
| :--- | :--- | :---: | :---: | :---: |
| **E-n33-k4** | • [PUC-Rio .vrp](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/E/E-n33-k4.vrp) / [PUC-Rio .sol](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/E/E-n33-k4.sol)<br>• Repo: [`E-n33-k4.vrp`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/E-n33-k4.vrp) / [`E-n33-k4.sol`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/E-n33-k4.sol) | 32 / 4 / 8000 | Christofides & Eilon (1969)<br>**BKS = 835** | **PASS** |
| **B-n50-k7** | • [PUC-Rio .vrp](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/B/B-n50-k7.vrp) / [PUC-Rio .sol](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/B/B-n50-k7.sol)<br>• Repo: [`B-n50-k7.vrp`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/B-n50-k7.vrp) / [`B-n50-k7.sol`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/B-n50-k7.sol) | 49 / 7 / 100 | Augerat et al. (1995)<br>**BKS = 741** | **PASS** |
| **E-n51-k5** | • [PUC-Rio .vrp](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/E/E-n51-k5.vrp) / [PUC-Rio .sol](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/E/E-n51-k5.sol)<br>• Repo: [`E-n51-k5.vrp`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/E-n51-k5.vrp) / [`E-n51-k5.sol`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/E-n51-k5.sol) | 50 / 5 / 160 | Christofides & Eilon (1969)<br>**BKS = 521** | **PASS** |
| **A-n53-k7** | • [PUC-Rio .vrp](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n53-k7.vrp) / [PUC-Rio .sol](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n53-k7.sol)<br>• Repo: [`A-n53-k7.vrp`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/A-n53-k7.vrp) / [`A-n53-k7.sol`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/A-n53-k7.sol) | 52 / 7 / 100 | Augerat et al. (1995)<br>**BKS = 1010** | **PASS** |
| **A-n60-k9** | • [PUC-Rio .vrp](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n60-k9.vrp) / [PUC-Rio .sol](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/A/A-n60-k9.sol)<br>• Repo: [`A-n60-k9.vrp`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/A-n60-k9.vrp) / [`A-n60-k9.sol`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/A-n60-k9.sol) | 59 / 9 / 100 | Augerat et al. (1995)<br>**BKS = 1354** | **PASS** |
| **E-n76-k7** | • [PUC-Rio .vrp](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/E/E-n76-k7.vrp) / [PUC-Rio .sol](http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/E/E-n76-k7.sol)<br>• Repo: [`E-n76-k7.vrp`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/E-n76-k7.vrp) / [`E-n76-k7.sol`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/benchmarks/raw/E-n76-k7.sol) | 75 / 7 / 220 | Christofides & Eilon (1969)<br>**BKS = 682** | **PASS** |

### 3.2. Ví dụ Parser đọc file, kiểm tra nghiệm tham chiếu và quy ước làm tròn

Để đảm bảo tính nguyên vẹn của dữ liệu gốc theo yêu cầu kiểm soát rủi ro R5, nhóm đã xây dựng bộ đọc dữ liệu tự động trong module [`src/core/cvrplib_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/cvrplib_loader.py) kết hợp cùng bộ kiểm thử [`tests/test_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_loader.py) sử dụng thư viện `vrplib`. Khi nạp một bộ dữ liệu bất kỳ (ví dụ `E-n33-k4.vrp` và tệp nghiệm `E-n33-k4.sol`), chương trình dùng hàm `vrplib.read_instance()` và `vrplib.read_solution()` để bóc tách trực tiếp các trường thông số chuẩn gồm: tổng số nút (`dimension = 33`, trong đó nút đầu tiên là kho nên số khách hàng thực tế là $33 - 1 = 32$), tải trọng xe (`capacity = 8000`), mảng nhu cầu thu gom (`demand`), vị trí kho (`depot = 0`) và ma trận khoảng cách 2 chiều (`edge_weight` kích thước $33 \times 33$).

Đoạn script Python kiểm chứng độc lập của Nguyễn Ngọc Thảo Hiền:

```python
import os
import glob
import vrplib
import numpy as np

# Tự động tìm thư mục chứa các file .vrp sau khi giải nén file .zip
vrp_files = glob.glob("**/E-n33-k4.vrp", recursive=True)
base_dir = os.path.dirname(vrp_files[0]) if vrp_files else "data/benchmarks/raw"
instances = ["E-n33-k4", "B-n50-k7", "E-n51-k5", "A-n53-k7", "A-n60-k9", "E-n76-k7"]

print(f"{'Instance':<10} | {'Khách':<5} | {'Q':<5} | {'BKS (.sol)':<10} | {'Tính lại (Int)':<14} | {'Tính lại (Float)':<16}")
print("-" * 75)

for name in instances:
    vrp_path = os.path.join(base_dir, f"{name}.vrp")
    sol_path = os.path.join(base_dir, f"{name}.sol")
    
    ins = vrplib.read_instance(vrp_path)
    sol = vrplib.read_solution(sol_path)
    
    n_customers = ins["dimension"] - 1
    capacity = int(ins["capacity"])
    depot = ins["depot"][0]
    edge_weight = ins["edge_weight"]
    
    float_cost = 0.0
    int_cost = 0
    
    for route in sol["routes"]:
        full_route = [depot] + route + [depot]
        for u, v in zip(full_route[:-1], full_route[1:]):
            d_uv = edge_weight[u][v]
            float_cost += d_uv
            int_cost += int(np.floor(d_uv + 0.5))  # Làm tròn số nguyên từng cạnh chuẩn EUC_2D
            
    print(f"{name:<10} | {n_customers:<5} | {capacity:<5} | {sol['cost']:<10} | {int_cost:<14} | {float_cost:<16.2f}")
```

#### Bảng kết quả thực nghiệm kiểm tra nghiệm BKS:

| Instance | Khách ($n-1$) | Sức chứa ($Q$) | BKS công bố (`.sol`) | Tính lại theo số nguyên (Int) | Tính lại theo số thực (Float) | Độ lệch (Float vs BKS) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **E-n33-k4** | 32 | 8000 | **835** | **835** *(Khớp 100%)* | 838.72 | +3.72 |
| **B-n50-k7** | 49 | 100 | **741** | **741** *(Khớp 100%)* | 744.78 | +3.78 |
| **E-n51-k5** | 50 | 160 | **521** | **521** *(Khớp 100%)* | 524.94 | +3.94 |
| **A-n53-k7** | 52 | 100 | **1010** | **1010** *(Khớp 100%)* | 1013.31 | +3.31 |
| **A-n60-k9** | 59 | 100 | **1354** | **1354** *(Khớp 100%)* | 1355.80 | +1.80 |
| **E-n76-k7** | 75 | 220 | **682** | **682** *(Khớp 100%)* | 687.60 | +5.60 |

Nhóm đã xác nhận toàn bộ các tuyến xe trong cả 6 tệp `.sol` đều hợp lệ 100%: xuất phát và kết thúc đúng tại kho (`depot = 0`), phục vụ đủ $n - 1$ khách hàng mà không trùng lặp hay bỏ sót, và tổng lượng hàng trên mỗi xe đều không vượt quá tải trọng $Q$.

**Về quy ước khoảng cách và giải thích sai lệch:**  
Cả 6 bộ benchmark đều sử dụng chuẩn khoảng cách Euclid 2 chiều (`EDGE_WEIGHT_TYPE: EUC_2D`). Theo quy ước gốc của thư viện TSPLIB/CVRPLIB, khoảng cách giữa hai điểm $(u, v)$ trên từng chặng phải được làm tròn về số nguyên gần nhất theo công thức:
$$d_{\text{int}}(u, v) = \left\lfloor\sqrt{(x_u - x_v)^2 + (y_u - y_v)^2} + 0.5\right\rfloor$$
trước khi cộng dồn toàn tuyến. Tuy nhiên, hàm `vrplib.read_instance()` trong Python mặc định giữ nguyên ma trận khoảng cách dưới dạng số thực dấu phẩy động (float). Thực nghiệm chạy đối chứng trên cả 6 bộ dữ liệu cho thấy sự khác biệt rõ rệt giữa hai cách tính này:
1. **E-n33-k4** (32 khách, $Q = 8000$): BKS công bố trong `.sol` là 835 $\to$ Tính lại theo số nguyên (Int) đạt **835** (khớp tuyệt đối 100%) $\to$ Tính theo số thực (Float) là 838.72 (lệch +3.72).
2. **B-n50-k7** (49 khách, $Q = 100$): BKS công bố trong `.sol` là 741 $\to$ Tính lại theo số nguyên (Int) đạt **741** (khớp tuyệt đối 100%) $\to$ Tính theo số thực (Float) là 744.78 (lệch +3.78).
3. **E-n51-k5** (50 khách, $Q = 160$): BKS công bố trong `.sol` là 521 $\to$ Tính lại theo số nguyên (Int) đạt **521** (khớp tuyệt đối 100%) $\to$ Tính theo số thực (Float) là 524.94 (lệch +3.94).
4. **A-n53-k7** (52 khách, $Q = 100$): BKS công bố trong `.sol` là 1010 $\to$ Tính lại theo số nguyên (Int) đạt **1010** (khớp tuyệt đối 100%) $\to$ Tính theo số thực (Float) là 1013.31 (lệch +3.31).
5. **A-n60-k9** (59 khách, $Q = 100$): BKS công bố trong `.sol` là 1354 $\to$ Tính lại theo số nguyên (Int) đạt **1354** (khớp tuyệt đối 100%) $\to$ Tính theo số thực (Float) là 1355.80 (lệch +1.80).
6. **E-n76-k7** (75 khách, $Q = 220$): BKS công bố trong `.sol` là 682 $\to$ Tính lại theo số nguyên (Int) đạt **682** (khớp tuyệt đối 100%) $\to$ Tính theo số thực (Float) là 687.60 (lệch +5.60).

Nhóm giữ nguyên giá trị BKS gốc làm mốc chuẩn chứ không lấy số Float ghi đè lên BKS, đồng thời lưu cả hai cột số nguyên và số thực vào file [`results/benchmark_metadata.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/benchmark_metadata.csv) để sang Step 3 khi chạy thuật toán sẽ đối sánh đúng quy ước.

### 3.3. Phân biệt giữa BKS khoảng cách CVRPLIB và Fitness chi phí–$\text{CO}_2$ ở case study

Nhóm xác định rõ hai bộ dữ liệu này phục vụ cho hai mục đích kiểm chứng khác nhau nên được tách riêng hoàn toàn trong mã nguồn xử lý:
* **Đối với BKS của bộ chuẩn CVRPLIB:** Các tọa độ $(X, Y)$ trong file `.vrp` chỉ là tọa độ phẳng giả định trong toán học, khoảng cách đi từ A đến B luôn bằng từ B về A (ma trận đối xứng: $d(A, B) = d(B, A)$) và không có đơn vị thực tế là mét hay kilômét. Con số BKS chỉ đơn thuần là tổng độ dài đoạn thẳng hình học ngắn nhất. Nhóm chỉ dùng CVRPLIB làm thước đo chuẩn để kiểm tra xem thuật toán SFO–VND khi viết xong có chạy đúng logic và tìm ra lời giải tiệm cận với kết quả tốt nhất thế giới (BKS) hay không, hoàn toàn không gắn tọa độ này vào TP.HCM và không tính lượng xăng dầu hay $\text{CO}_2$ trên bộ dữ liệu này.
* **Đối với hàm fitness chi phí–$\text{CO}_2$ ở Case Study (Phường Tây Thạnh):** Dữ liệu được lấy từ mạng lưới đường giao thông thực tế trên OpenStreetMap (OSMnx) với đơn vị mét/kilômét rõ ràng. Do ngoài thực tế có đường một chiều, hẻm cụt và vòng xoay nên quãng đường đi từ điểm $A$ đến điểm $B$ sẽ khác chiều ngược lại từ $B$ về $A$ ($d(A, B) \ne d(B, A)$, ma trận bất đối xứng tính bằng thuật toán Dijkstra). Ngoài ra, mục tiêu tối ưu ở Case Study không chỉ là tìm đường ngắn nhất mà còn phải tính đến chi phí vận hành và lượng khí thải $\text{CO}_2$ phát sinh theo khối lượng rác chất lên xe qua từng điểm thu gom (được mô hình hóa theo tải trọng tích lũy của xe). Vì vậy, nhóm tuyệt đối không lấy giá trị BKS của CVRPLIB để đem so sánh với hàm mục tiêu chi phí–$\text{CO}_2$ của phường Tây Thạnh.

---

## 4. Instance thử nghiệm nhỏ (Toy Instance)

### Bảng Thông số kỹ thuật

| Thông số | Giá trị thực tế của nhóm |
| :--- | :--- |
| **Tên file, số điểm n** | [`data/toy/toy_12_points.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_12_points.csv), [`data/toy/toy_instance.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_instance.json); $n = 13$ điểm (1 Depot ID 0 + 12 điểm khách hàng ID 1..12) |
| **Depot (ID, vị trí)** | ID = 0, Tọa độ lưới gốc (`x = 0.0`, `y = 0.0`) |
| **Số xe K / tải trọng Q** | $K = 3$ xe; Tải trọng tối đa $Q = 200.0\text{ kg}$/xe |
| **Tổng demand / mức dự phòng** | Tổng demand = $420.0\text{ kg}$; Tổng sức chứa cả đội xe = $600.0\text{ kg}$; Mức dự phòng tải = $180.0\text{ kg}$ ($30.0\%$) |
| **Seed, cách sinh demand** | `seed = 42`, sinh ngẫu nhiên có kiểm soát theo phân tầng nhu cầu $[20, 25, 30, 35, 40, 45, 50]\text{ kg}$ |
| **Đơn vị khoảng cách và tải trọng** | Khoảng cách: mét (m); Tải trọng / Nhu cầu: kilôgam (kg) |
| **Nguồn ma trận (thật/mô phỏng)** | Mô phỏng tọa độ hình học 2D phân bố theo 3 cụm góc phần tư tương ứng 3 tuyến xe; ma trận khoảng cách Euclid đối xứng tính toán chính xác |

### 4.1. Bảng dữ liệu Toy Instance (Trích xuất 5 dòng đầu)

> *File gốc lưu tại: [`data/toy/toy_12_points.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_12_points.csv)*

| point_id | name | x | y | demand_kg | node_type |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **0** | Trạm trung chuyển Depot | 0.0 | 0.0 | 0.0 | depot |
| **1** | Điểm thu gom 1 | 10.0 | 20.0 | 30.0 | customer |
| **2** | Điểm thu gom 2 | 20.0 | 30.0 | 45.0 | customer |
| **3** | Điểm thu gom 3 | 30.0 | 30.0 | 25.0 | customer |
| **4** | Điểm thu gom 4 | 30.0 | 10.0 | 40.0 | customer |
| **5** | Điểm thu gom 5 | -20.0 | 20.0 | 35.0 | customer |
| *...* | *(Còn 7 điểm từ ID 6 đến 12)* | *...* | *...* | *...* | customer |

*Quy tắc sinh dữ liệu:* Cố định `seed = 42`. 12 điểm khách hàng được phân bố thành 3 cụm không gian riêng biệt ở các góc phần tư để mỗi xe phụ trách một nhánh tuyến tự nhiên: Cụm 1 (điểm 1–4, góc phần tư I), Cụm 2 (điểm 5–8, góc phần tư II), Cụm 3 (điểm 9–12, góc phần tư IV).

### 4.2. Cách chia tuyến hợp lệ (Feasible Witness)

> *Minh chứng nghiệm lưu tại: [`data/toy/toy_feasible_routes.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_feasible_routes.json) và bản tính tay: [`results/figures/toy_hand_calculation.png`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/figures/toy_hand_calculation.png)*

| Xe | Tuyến ($0 \to \dots \to 0$) | Tải thực tế / Q | Chiều dài tuyến (m) | Hợp lệ? / Bằng chứng |
| :---: | :---: | :---: | :---: | :---: |
| **Xe 1** | $0 \to 1 \to 2 \to 3 \to 4 \to 0$ | $140.0\text{ kg} / 200.0\text{ kg}$ | $98.12\text{ m}$ | **PASS** *(Không vượt tải $Q$, xuất phát và về Depot)* |
| **Xe 2** | $0 \to 5 \to 6 \to 7 \to 8 \to 0$ | $135.0\text{ kg} / 200.0\text{ kg}$ | $102.32\text{ m}$ | **PASS** *(Không vượt tải $Q$, xuất phát và về Depot)* |
| **Xe 3** | $0 \to 9 \to 10 \to 11 \to 12 \to 0$ | $145.0\text{ kg} / 200.0\text{ kg}$ | $108.92\text{ m}$ | **PASS** *(Không vượt tải $Q$, xuất phát và về Depot)* |
| **Tổng** | **Phục vụ đủ 12/12 khách, không sót, không lặp** | **420.0 kg / 600.0 kg** | **309.36 m** | **100% FEASIBLE WITNESS** |

Chi tiết các chặng của từng tuyến:
* **Tuyến 1:** $0 \to 1$ ($22.36\text{m}$) $\to 2$ ($14.14\text{m}$) $\to 3$ ($10.00\text{m}$) $\to 4$ ($20.00\text{m}$) $\to 0$ ($31.62\text{m}$) = $98.12\text{ m}$.
* **Tuyến 2:** $0 \to 5$ ($28.28\text{m}$) $\to 6$ ($14.14\text{m}$) $\to 7$ ($14.14\text{m}$) $\to 8$ ($14.14\text{m}$) $\to 0$ ($31.62\text{m}$) = $102.32\text{ m}$.
* **Tuyến 3:** $0 \to 9$ ($22.36\text{m}$) $\to 10$ ($14.14\text{m}$) $\to 11$ ($30.00\text{m}$) $\to 12$ ($14.14\text{m}$) $\to 0$ ($28.28\text{m}$) = $108.92\text{ m}$.
* **Tổng quãng đường cả đội xe:** $98.12 + 102.32 + 108.92 = 309.36\text{ m}$.

### 4.3. Xử lý dữ liệu không khả thi, cách điều chỉnh kịch bản và lưu trữ bản gốc

Để kiểm chứng khả năng phòng thủ của hệ thống trước các kịch bản dữ liệu bất khả thi (infeasible data), nhóm đã thiết lập quy trình gồm **2 cơ chế**: (A) Phát hiện và chặn lỗi nghiêm ngặt bằng bộ kiểm thử biên tự động, và (B) Quy tắc điều chỉnh kịch bản về trạng thái khả thi.

#### A. Điều kiện bị vi phạm và 7 ca kiểm thử biên tự động
Nhóm đã xây dựng bộ kiểm thử biên độc lập tại [`tests/test_toy_instance.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_toy_instance.py) để chủ động tiêm lỗi (fault injection) và bắt sống 7 trường hợp vi phạm điều kiện khả thi của bài toán CVRP:

1. **`test_duplicate_point_id` (Vi phạm tính duy nhất của khóa chính):**
   - *Điều kiện bị vi phạm:* Tồn tại `point_id` xuất hiện nhiều hơn 1 lần (`len(points) != len(set(points))`, cụ thể nhân đôi điểm `ID = 1`).
   - *Cách điều chỉnh kịch bản:* Khử trùng lặp (`drop_duplicates(subset=['point_id'])`) hoặc đánh lại chỉ số định danh liên tục từ `0` đến `n` trước khi tạo ma trận khoảng cách.
2. **`test_negative_or_missing_demand` (Vi phạm miền giá trị nhu cầu rác):**
   - *Điều kiện bị vi phạm:* Khối lượng rác tại một điểm bị khuyết (`NaN`/`None`) hoặc mang giá trị âm (`q_2 = -10.0 kg < 0`).
   - *Cách điều chỉnh kịch bản:* Loại bỏ bản ghi khuyết tọa độ/nhu cầu (`dropna(subset=['lat', 'lon', 'demand'])` trong [`src/core/data_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/data_loader.py)) hoặc gán lại nhu cầu theo phân phối chuẩn của loại hình điểm thu gom (`seed = 42`).
3. **`test_demand_exceeds_capacity` (Vi phạm ràng buộc tải trọng đơn điểm `q_i <= Q`):**
   - *Điều kiện bị vi phạm:* Tồn tại một điểm thu gom có lượng rác vượt quá sức chứa tối đa của một xe (`q_3 = 250.0 kg > Q = 200.0 kg`), khiến không một xe đơn lẻ nào có thể phục vụ điểm đó trong 1 lượt.
   - *Cách điều chỉnh kịch bản:* Trong hàm `preprocess_case_study_data()` ([`src/core/data_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/data_loader.py)), hệ thống phát cảnh báo vượt tải và điều chỉnh ngưỡng thu gom tối đa của điểm đó về bằng sức chứa `Q_max` (hoặc tách điểm có lượng rác quá lớn thành 2 điểm thu gom thành phần / nâng cấp cỡ xe `Q`).
4. **`test_missing_depot` (Vi phạm ràng buộc điểm xuất phát/kết thúc):**
   - *Điều kiện bị vi phạm:* Tập dữ liệu thiếu trạm trung chuyển gốc `Depot ID = 0` (`depot_id not in points`).
   - *Cách điều chỉnh kịch bản:* Bổ sung bản ghi chuẩn của Trạm trung chuyển (`point_id = 0`, `demand_kg = 0.0`, `node_type = 'depot'`) từ tệp cấu hình `depot.csv` vào dòng đầu tiên của danh sách điểm.
5. **`test_unreachable_node` (Vi phạm tính liên thông có hướng của mạng đường):**
   - *Điều kiện bị vi phạm:* Có điểm bị cô lập hoặc rơi vào nhánh đường cụt một chiều, không thể đi từ Depot tới hoặc không thể quay về Depot (`d(4, 0) = Inf`). Hệ thống tuyệt đối không tự ý gán khoảng cách lỗi bằng `0`.
   - *Cách điều chỉnh kịch bản:* Lọc đồ thị con liên thông mạnh lớn nhất (**Strongly Connected Component - SCC**) bằng hàm `nx.strongly_connected_components(G)` trong [`src/map/extract_map.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/map/extract_map.py), sau đó ánh xạ (snap) lại điểm bị cô lập về nút giao thông gần nhất nằm trong SCC.
6. **`test_vehicles_exceed_fleet_size` (Vi phạm giới hạn quy mô đội xe `số tuyến <= K`):**
   - *Điều kiện bị vi phạm:* Phương án phân tuyến sử dụng 4 xe, vượt quá số lượng xe tối đa cho phép của kịch bản (`4 xe > K = 3 xe`), hoặc tổng nhu cầu rác vượt quá tổng sức chứa đội xe (`Tổng q_i > K * Q`).
   - *Cách điều chỉnh kịch bản:* Gộp các tuyến có hệ số lấp đầy thấp (ví dụ gộp điểm `4` vào lại Xe 1 do `105 kg + 40 kg = 145 kg <= 200 kg`), hoặc sử dụng bộ cắt tuyến tối ưu `optimal_split_decoder` (Quy hoạch động Prins 2004 trong [`src/core/decoder.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/decoder.py)) để nén số chuyến xe về `<= K`. Nếu tổng rác thực tế `Tổng q_i > K * Q`, điều chỉnh tăng số xe `K` trong `scenario.json`.
7. **`test_duplicate_or_omitted_customer` (Vi phạm ràng buộc phục vụ đúng 1 lần mỗi khách hàng):**
   - *Điều kiện bị vi phạm:* Một điểm khách hàng bị bỏ sót không xe nào ghé (bỏ sót điểm `ID = 12`) hoặc một điểm bị 2 xe ghé trùng lặp (điểm `ID = 1` xuất hiện ở cả Xe 1 và Xe 2).
   - *Cách điều chỉnh kịch bản:* Sử dụng cơ chế mã hóa hoán vị `Random-Key` (`np.argsort(vector) + 1`) kết hợp hàm hậu kiểm trong `tour_to_random_key()` ([`src/core/decoder.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/decoder.py)) để tự động loại bỏ điểm lặp và chèn bổ sung các điểm bị thiếu (`missing_points = all_points - set(ordered_points)`), đảm bảo mọi hoán vị luôn phủ đúng 100% khách hàng mỗi điểm 1 lần.

#### B. Nhóm có lưu bản trước khi chỉnh sửa không? (Cơ chế bảo toàn dữ liệu gốc)
**CÓ.** Nhóm áp dụng nguyên tắc bất biến dữ liệu gốc (Immutable Raw Data) ở cả 3 cấp độ:
1. **Trên bộ Toy Instance (`data/toy/`):** Các tệp chuẩn gốc (`toy_12_points.csv`, `toy_instance.json`, `toy_feasible_routes.json`) luôn được khóa cố định trên ổ cứng. Khi chạy 7 ca kiểm thử biên trong [`tests/test_toy_instance.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_toy_instance.py), chương trình chỉ tạo bản sao sâu trong bộ nhớ RAM (`df.copy()` và `json.loads(json.dumps(instance))`) để tiêm lỗi và kiểm tra phản ứng của hàm kiểm định, tuyệt đối không ghi đè làm hỏng tệp gốc.
2. **Trên bộ Case Study Phường Tây Thạnh (`data/ward/`):** Dữ liệu gốc trước khi xử lý (ranh giới hành chính `ward_boundary.geojson` và đồ thị gốc 935 nút `road_network.graphml` chưa lọc SCC) được lưu tách biệt hoàn toàn tại thư mục [`data/ward/raw/`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/tree/main/data/ward/raw/). Dữ liệu sau khi lọc SCC (868 nút), snap điểm và điều chỉnh chuẩn hóa được xuất sang thư mục riêng [`data/ward/processed/`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/tree/main/data/ward/processed/).
3. **Trên hệ thống quản lý phiên bản Git:** Toàn bộ lịch sử thay đổi từ bản sinh thử nghiệm ban đầu đến bản khóa dữ liệu `v1.0` đều được lưu vết đầy đủ qua các commit trên GitHub, cho phép khôi phục và đối chiếu phiên bản trước/sau chỉnh sửa bất kỳ lúc nào.

---

## 5. Case study cấp phường

### Bảng Cấu hình Case Study

| Nội dung | Giá trị và cách xác minh |
| :--- | :--- |
| **Phường/khu vực, ngày lấy OSM** | **Phường Tây Thạnh, Quận Tân Phú, TP.HCM**; Ngày lấy dữ liệu: 24/10/2026 |
| **Số điểm thu gom và loại điểm** | **51 điểm** (1 Trạm trung chuyển Depot + 50 điểm thu gom rác: 35 điểm dân cư, 15 điểm kinh doanh/thương mại) |
| **Điểm thật / điểm mô phỏng** | 1 Depot quy hoạch thực tế tại KCN Tân Bình; 50 điểm thu gom giả lập trên các tuyến đường OSMnx (gán nhãn minh bạch: `điểm thu gom giả lập trên mạng đường OSM`) |
| **Phân phối lượng rác, seed** | `seed = 42`; Khu dân cư: 35–75 kg; Khu kinh doanh/thương mại: 80–120 kg; Depot: 0.0 kg |
| **Số xe K, tải trọng Q, depot** | $K = 4$ xe chuyên dụng; Tải trọng tối đa $Q = 1,500.0\text{ kg}$ (1.5 tấn/xe); Depot ID = 0 tại KCN Tân Bình $(10.8122, 106.6215)$ |
| **Tổng demand, tổng capacity** | Tổng demand = $3,345.0\text{ kg}$; Tổng capacity = $6,000.0\text{ kg}$ (Tỷ lệ sử dụng tải: $55.75\%$, mức dự phòng an toàn $44.25\%$) |
| **Phương án tuyến hợp lệ (file)** | [`data/ward/processed/feasible_routes.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/feasible_routes.json) (Xe 1: 1,475.0 kg; Xe 2: 1,475.0 kg; Xe 3: 395.0 kg; Xe 4: dự phòng 0.0 kg; Tổng quãng đường: 42.326 km) |
| **Các giả định còn đang dùng** | Vận tốc xe di chuyển cố định theo cấp đường đô thị; xe rỗng xuất phát từ Depot và quay về xả rác tại Depot; mỗi điểm chỉ thu gom 1 lần/ca; hệ số phát thải dùng định mức lý thuyết MEET / ISO 14064. |

### 5.1. Quy mô điểm thu gom

Nhóm đã xây dựng hoàn chỉnh bộ dữ liệu **50 điểm thu gom rác (+ 1 Depot = 51 điểm)**, nằm đúng trong dải chuẩn 40–100 điểm cấp phường theo yêu cầu của Thầy hướng dẫn. Toàn bộ 50 điểm đều có tọa độ định vị GPS cụ thể, gán nhãn loại hình rõ ràng, snap trực tiếp 100% vào mạng đường ô tô thật của Phường Tây Thạnh (khoảng cách snap bằng 0.0 m) và có ma trận khoảng cách đầy đủ, tuyệt đối không dùng số liệu giả định cho đủ biểu mẫu.

### 5.2. Nguồn gốc các trường dữ liệu

| Trường dữ liệu | Nguồn cụ thể + ngày lấy | Loại nguồn | Độ tin cậy/giới hạn |
| :--- | :--- | :--- | :--- |
| **Tọa độ điểm** | Trích xuất theo 13 trục đường chính của Phường Tây Thạnh (Lê Trọng Tấn, Tây Thạnh, Chế Lan Viên, Lưu Chí Hiếu, CN1, CN13, Nguyễn Hữu Tiến,...) ngày 24/10/2026 | OSM / Khảo sát thực địa | **Độ tin cậy cao**, tọa độ thực tế trên mạng đường WGS84 EPSG:4326. |
| **Demand** | Sinh ngẫu nhiên có kiểm soát theo phân tầng: Dân cư (35–75 kg) và Kinh doanh (80–120 kg), `seed = 42` | Mô phỏng có kiểm soát | **Độ tin cậy khá**, phản ánh sát lượng rác phát sinh trung bình của hộ gia đình và hàng quán tại TP.HCM. |
| **Depot** | Trạm trung chuyển chất thải KCN Tân Bình – Tây Thạnh $(10.8122, 106.6215)$, tiếp giáp trực tiếp đường trục CN13 | Tài liệu công khai quy hoạch | **Rất tin cậy**, bãi xe và trạm trung chuyển chất thải quy hoạch thực tế của địa phương. |
| **Số xe / tải trọng** | Đội xe $K=4$ xe, tải trọng $Q=1,500\text{ kg}$ (1.5 tấn), tham khảo quy chuẩn xe ép rác mini đô thị CITENCO | Tài liệu công khai / Thực tế ngành | **Độ tin cậy cao**, phù hợp quy định cấm tải xe lớn trong ngõ hẻm ban ngày tại TP.HCM. |
| **Đường & khoảng cách** | Đồ thị đường ô tô `network_type="drive"` buffer 400m từ OpenStreetMap, tính bằng thuật toán Dijkstra | OpenStreetMap (ODbL) | **Rất tin cậy**, phản ánh đường 1 chiều thực tế. *Giới hạn:* Dữ liệu OSM theo mức đóng góp cộng đồng, `network_type="drive"` chưa xác minh đầy đủ quy định riêng cho xe ép rác, giới hạn khổ xe hay biển cấm rẽ theo giờ tại từng giao lộ. |
| **Thông số nhiên liệu** | Trọng lượng rỗng xe 2,500 kg, định mức 0.12 L/km, hệ số tải 0.00004 L/km/kg, hệ số phát thải diesel 2.68 kg $\text{CO}_2$/L | Mô hình MEET / ISO 14064 | **Ước tính khoa học chuẩn**, công thức lý thuyết, sẽ chính thức khóa tham số ở Step 3. |

---

## 6. Ma trận khoảng cách trên mạng đường

### 6.1. Quy trình tạo đồ thị và Bảng kết quả kiểm tra

* **Cách tạo graph:** Sử dụng thư viện `osmnx` tải đồ thị xe ô tô (`network_type = "drive"`) theo ranh giới Phường Tây Thạnh mở rộng vùng đệm buffer 400m. Lưu đồ thị dạng chuẩn vĩnh viễn tại [`data/ward/raw/road_network.graphml`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/road_network.graphml).
* **Phương pháp snap:** Trích xuất thành phần liên thông mạnh lớn nhất (**Strongly Connected Component - SCC**) gồm 868 nút. Toàn bộ 51 điểm được snap vào các nút thuộc SCC; khoảng cách snap tối đa đạt **0.0 m** (chọn trực tiếp trên nút mạng đường).
* **Công thức trọng số và đơn vị:** Thuật toán Dijkstra tìm đường ngắn nhất có hướng dựa trên thuộc tính `length` của từng đoạn đường, xuất ma trận vuông kích thước $51 \times 51$ với đơn vị đo lường là **mét (m)**. Từng điểm đảm bảo $100\%$ có đường đi từ Depot và có đường quay về Depot.

### Bảng Kiểm tra ma trận khoảng cách

| Kiểm tra | Số lượng / kết quả | Minh chứng |
| :--- | :--- | :--- |
| **Số nút/số cạnh graph** | **935 nút / 2,123 cạnh** (SCC lớn nhất: 868 nút, chiếm 92.8%) | [`data/ward/raw/road_network.graphml`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/road_network.graphml), [`src/map/extract_map.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/map/extract_map.py) |
| **Khoảng cách snap lớn nhất** | **0.0 m** (100% 50 điểm thu gom và Depot được chọn trực tiếp trên tập nút mạng đường ô tô SCC của Phường Tây Thạnh) | [`data/ward/processed/collection_points.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/collection_points.csv) |
| **Cặp không có đường đi** | **0 cặp** (Không có cặp nào bị vô cực $\infty$, 100% liên thông 2 chiều) | [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log) dòng 21 |
| **Depot $\to$ điểm $\to$ Depot** | **PASS** (100% điểm đều đến được từ Depot và về được Depot) | [`tests/validate_dataset.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/validate_dataset.py) Suite 4 |
| **Ví dụ $d(A, B)$ và $d(B, A)$ (Đối chiếu 3 cặp bất đối xứng)** | • Cặp $(0, 1)$: $d(0, 1) = 1,487.6\text{ m} \ne d(1, 0) = 1,360.5\text{ m}$ ($\Delta = 127.1\text{ m}$)<br>• Cặp $(1, 2)$: $d(1, 2) = 256.9\text{ m} \ne d(2, 1) = 716.3\text{ m}$ ($\Delta = 459.4\text{ m}$)<br>• Cặp $(2, 0)$: $d(2, 0) = 1,120.1\text{ m} \ne d(0, 2) = 1,230.7\text{ m}$ ($\Delta = 110.6\text{ m}$) | [`data/ward/processed/distance_matrix.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/distance_matrix.csv), [`docs/reports/feasibility_report.md`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/docs/reports/feasibility_report.md) |
| **Kiểm tra giá trị đường chéo** | **PASS** ($d(i, i) = 0.0\text{ m}$ với mọi $i = 0..50$) | [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log) dòng 14 |

### 6.2. Đối chiếu cộng tay một tuyến nhỏ từ ma trận và script

Xét chu trình khép kín nhỏ: $\text{Depot (0)} \to \text{Điểm 1} \to \text{Điểm 2} \to \text{Depot (0)}$:
* Chặng 1 ($0 \to 1$): Tra ma trận dòng 0 cột 1: $d(0, 1) = 1,487.6\text{ m}$
* Chặng 2 ($1 \to 2$): Tra ma trận dòng 1 cột 2: $d(1, 2) = 256.9\text{ m}$
* Chặng 3 ($2 \to 0$): Tra ma trận dòng 2 cột 0: $d(2, 0) = 1,120.1\text{ m}$
* **Tổng chiều dài cộng tay:**
  $$D_{\text{cycle}} = 1487.6 + 256.9 + 1120.1 = 2,864.6\text{ m} = 2.865\text{ km}$$
* **Đối chiếu với kết quả script:** Script tính ra chính xác $2,864.6\text{ m}$ (độ chênh lệch bằng $0.0\text{ m}$, khớp $100\%$).

### 6.3. Xử lý điểm không snap được, đường một chiều hoặc đoạn đường không có kết nối

* Nhóm **tuyệt đối không tự ý điền khoảng cách thiếu bằng 0** (vì giá trị 0 sẽ làm thuật toán lầm tưởng hai điểm trùng nhau và di chuyển không tốn chi phí).
* **Biện pháp xử lý của nhóm:**
  1. Trích xuất thành phần liên thông mạnh lớn nhất (**Strongly Connected Component - SCC**) gồm 868 nút từ đồ thị xe ô tô.
  2. Bắt buộc snap 51 điểm vào tập nút thuộc SCC này. Cơ chế này loại bỏ hoàn toàn nguy cơ điểm bị rơi vào ngõ cụt đường 1 chiều (chỉ vào được mà không ra được) hoặc phân đoạn đường cô lập.
  3. Bất kỳ cặp điểm nào có khoảng cách thiếu (`NaN`) hoặc vô cực ($\infty$) đều bị ném lỗi `ValueError` ngay lập tức trong [`src/core/data_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/data_loader.py) và bộ kiểm định [`tests/validate_dataset.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/validate_dataset.py).
* **Giới hạn của dữ liệu mạng đường OSM:** Dữ liệu OpenStreetMap mô tả mạng đường theo mức độ đóng góp của cộng đồng; tham số `network_type = "drive"` trích xuất mạng đường ô tô chung nhưng chưa xác minh đầy đủ các quy định đặc thù dành riêng cho xe ép rác chuyên dụng, giới hạn tải trọng trục/khổ xe trong hẻm nhỏ hoặc biển cấm rẽ theo khung giờ tại từng giao lộ.

---

## 7. Kiểm thử dữ liệu và khả năng tái lập

### Bảng Kết quả kiểm thử tự động

> *Minh chứng log kiểm thử: [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log) và [`results/pytest_reproduce_hien.txt`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/pytest_reproduce_hien.txt)*

| Bài kiểm tra | PASS / FAIL | Kết quả và đường dẫn log |
| :--- | :---: | :--- |
| **Schema, kiểu dữ liệu, ID duy nhất** | **PASS** | Đủ 7 cột bắt buộc tại `collection_points.csv`, `depot.csv`, `vehicles.csv`; 100% trường đúng kiểu dữ liệu (`int`, `float`, `str`), 0 giá trị `NaN`/`Null`; 51 `point_id` liên tục từ `0..50` duy nhất, không trùng lặp. Kiểm chứng: [`tests/validate_dataset.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/validate_dataset.py) (Suite 1) & [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log#L4-L9). |
| **Tọa độ và depot** | **PASS** | 100% tọa độ đạt chuẩn WGS84 (`EPSG:4326`) nằm trong khung địa lý Phường Tây Thạnh (`lat: 10.8024..10.8205`, `lon: 106.6064..106.6311`); Depot `ID = 0` hiện diện tại `(10.8122, 106.6215)`, nhãn `point_type = 'depot'`, `demand_kg = 0.0 kg`. Kiểm chứng: [`tests/validate_dataset.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/validate_dataset.py) (Suite 1.4 & 2.1) & [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log#L7-L10). |
| **Demand không âm, q_i ≤ Q** | **PASS** | Mọi điểm thu gom (`ID 1..50`) đều có lượng rác `q_i > 0` (`35.0..120.0 kg`) và 100% thỏa `q_i ≤ Q = 1,500.0 kg` trên cả Case Study, Toy Instance (`q_i ≤ 200 kg`) và 6 bộ CVRPLIB. Kiểm chứng: [`tests/test_loader.py::test_demands_and_capacities`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_loader.py), [`tests/test_toy_instance.py::test_demand_exceeds_capacity`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_toy_instance.py) & [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log#L11-L12). |
| **Tổng capacity và feasible witness** | **PASS** | Tổng nhu cầu rác `∑q_i = 3,345.0 kg ≤ K × Q = 6,000.0 kg` (`K = 4 xe`, `Q = 1,500 kg/xe`); tồn tại phương án phân tuyến hợp lệ [`data/ward/processed/feasible_routes.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/feasible_routes.json) (Xe 1: `1,475 kg`, Xe 2: `1,475 kg`, Xe 3: `395 kg`, Xe 4: `0 kg`, tổng quãng đường `42.326 km`). Kiểm chứng: [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log#L16-L17). |
| **Phục vụ đủ và đúng một lần** | **PASS** | Phương án tuyến khả thi phục vụ đủ `50/50` điểm khách hàng (không bỏ sót), tổng lượt ghé đúng bằng `50` (`0` điểm bị phục vụ lặp giữa các xe), 100% xe xuất phát và kết thúc khép kín tại `Depot 0`. Kiểm chứng: [`tests/test_toy_instance.py::test_duplicate_or_omitted_customer`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_toy_instance.py) & [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log#L18-L19). |
| **Đường đi/đường về depot** | **PASS** | Đồ thị được lọc trên thành phần liên thông mạnh lớn nhất (`SCC: 868 nút`); 100% điểm đều có đường đi từ Depot (`d(0, i) > 0`) và có đường quay về Depot (`d(i, 0) > 0`), `0` cặp điểm bị cô lập (`Inf`/`NaN`). Kiểm chứng: [`tests/test_toy_instance.py::test_unreachable_node`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_toy_instance.py) & [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log#L20-L23). |
| **Ma trận ID và đơn vị** | **PASS** | Ma trận [`data/ward/processed/distance_matrix.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/distance_matrix.csv) khớp kích thước `51 × 51` theo đúng thứ tự `ID 0..50` (đơn vị: mét), đường chéo chính `d(i, i) = 0.0 m`, mọi ô ngoài đường chéo `d(i, j) > 0` (`16.5 m .. 3,920.7 m`), bất đối xứng `d(i, j) ≠ d(j, i)`, tuyệt đối không gán `0` cho ô thiếu. Kiểm chứng: [`tests/test_loader.py::test_distance_matrix_validity`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_loader.py) & [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log#L13-L15). |
| **So sánh kết quả 2 lần chạy cùng seed** | **PASS** | Khóa cố định `seed = 42` tại [`data/ward/processed/scenario.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/scenario.json); thực thi chạy tự động 2 lần độc lập cùng `seed = 42` trong Suite 5.3 cho ra phân loại điểm, vector nhu cầu rác và ma trận khoảng cách giống hệt nhau 100%; 6 bộ CVRPLIB đối chứng khớp 100% BKS (`diff = 0.0`). Kiểm chứng: [`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log#L25-L27). |
| **Một thành viên khác chạy lại thành công** | **PASS** | Thành viên Nguyễn Ngọc Thảo Hiền đã clone kho code về máy cá nhân độc lập (`C:\Users\Asus\Downloads\SFO-VND_GreenWasteRouting-main`) và chạy kiểm thử tự động đạt **40 passed in 2.48s** (trên máy nhóm trưởng đạt **40 passed in 0.56s**, **30/30 PASS** tại `validate_dataset.py`). Kiểm chứng: [`results/pytest_reproduce_hien.txt`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/pytest_reproduce_hien.txt). |

> [!TIP]
> **Ghi chú về kiểm thử:** Toàn bộ **30/30 tiêu chí kiểm định tự động** tại `validate_dataset.py` và **40/40 bài unit test** trong hệ thống pytest đều đạt **PASS 100%**, không có ca nào bị FAIL. Nhóm không thay đổi kết quả lỗi bằng PASS và đảm bảo tính trung thực kỹ thuật.

---

## 8. Xử lý các điểm chưa giải quyết ở Step 1

### Bảng Theo dõi xử lý các vấn đề R1 – R8

| Mã vấn đề | Trạng thái hiện tại | Minh chứng / Quyết định & Lý do xử lý | Người phụ trách |
| :---: | :---: | :--- | :--- |
| **R1. Ranh giới phường hiện hành** | **Đã giải quyết** | Chọn Phường Tây Thạnh (Quận Tân Phú), trích xuất ranh giới WGS84 chuẩn OSM Overpass API, buffer 400m. Tránh tranh cãi pháp lý tên Sơn Kỳ cũ. Minh chứng: [`docs/reports/ward_selection.md`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/docs/reports/ward_selection.md), [`data/ward/raw/ward_boundary.geojson`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/ward_boundary.geojson). | **Lê Nguyễn Tâm Đức** |
| **R2. K, Q và demand** | **Đã giải quyết** | Khóa kịch bản $K=4$ xe, $Q=1,500\text{ kg}$, 50 điểm thu gom có tổng demand 3,345 kg $\le 6,000$ kg. Đã thiết lập Feasible Witness chứng minh bài toán chắc chắn có nghiệm giải được. Minh chứng: [`data/ward/processed/scenario.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/scenario.json), [`data/ward/processed/feasible_routes.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/feasible_routes.json). | **Vũ Thế Quang** |
| **R3. Thực tế vs mô phỏng** | **Đã giải quyết** | Lập Từ điển dữ liệu chuẩn, gắn nhãn minh bạch `điểm thu gom giả lập trên mạng đường OSM` và `trạm trung chuyển chất thải quy hoạch`. Giữ vững tính trung thực khoa học, không ngụy tạo số đo sensor thực tế. Minh chứng: [`docs/reports/data_dictionary.md`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/docs/reports/data_dictionary.md). | **Vũ Thế Quang** |
| **R4. Ma trận có hướng** | **Đã giải quyết** | Tính ma trận Dijkstra có hướng trên thành phần liên thông mạnh SCC (868 nút), phản ánh đường 1 chiều, đường chéo bằng 0, không có giá trị khuyết. Triệt tiêu hoàn toàn nguy cơ đứt đường. Minh chứng: [`data/ward/processed/distance_matrix.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/distance_matrix.csv), [`docs/reports/feasibility_report.md`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/docs/reports/feasibility_report.md). | **Lê Nguyễn Tâm Đức** |
| **R5. CVRPLIB và BKS** | **Đã giải quyết** | Nạp chuẩn xác 6 bộ dữ liệu CVRPLIB bằng `vrplib`, tuân thủ quy ước làm tròn nguyên EUC_2D TSPLIB, khớp hoàn toàn 100% giá trị tham chiếu BKS công bố quốc tế. Minh chứng: [`results/benchmark_metadata.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/benchmark_metadata.csv), [`tests/test_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_loader.py). | **Nguyễn Ngọc Thảo Hiền** |
| **R6. Fitness/chi phí–$\text{CO}_2$** | **Chuyển Step 3** | Đã liệt kê sơ bộ các thông số định mức tải trọng, tiêu hao nhiên liệu và hệ số phát thải ISO 14064 trong [`src/config.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/config.py). Tuân thủ yêu cầu Step 2 "Chưa cần cài SFO hay hàm mục tiêu phức tạp", chính thức khóa công thức toán học và hàm đa mục tiêu ở Step 3. | **Vũ Thế Quang** |
| **R7. Decoder/VND cập nhật ngược** | **Chuyển Step 3 & 6** | Đã chuẩn bị sẵn cả 2 phương pháp cắt tuyến trong [`src/core/decoder.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/decoder.py): **Greedy First-Fit Split** và **Optimal Split (Quy hoạch động Prins 2004 trên DAG)** cùng hàm cập nhật ngược `tour_to_random_key`; việc ghép nối và đánh giá thực nghiệm với SFO–VND sẽ thực hiện ở Step 3 & 6. | **Vũ Thế Quang & Lê Nguyễn Tâm Đức** |
| **R8. Mở rộng, SFO và demo** | **Chuyển Step 4/6/8** | Các kịch bản quy mô lớn (300–400 điểm), phân tích độ nhạy What-if và giao diện tương tác Web GIS chuyển sang các bước sau theo đúng tiến độ dự án để bảo đảm dữ liệu nền tảng 50 điểm vững chắc trước. | **Cả nhóm** |

### Câu hỏi nhóm muốn thầy duyệt trước Step 3:
1. *Về hàm mục tiêu Fitness:* Thầy cho phép nhóm cố định hàm mục tiêu đa tiêu chí kết hợp kinh tế - môi trường: $f = \alpha \cdot \text{Cost} + (1 - \alpha) \cdot \text{Emission}_{\text{CO}_2}$ với mô hình tiêu hao nhiên liệu phụ thuộc tải trọng rác của MEET/ISO 14064 cho Step 3 hay cần bổ sung thêm ràng buộc về cửa sổ thời gian (Time Windows)?
2. *Về phạm vi benchmark giải thuật:* Ở Step 3, Thầy có yêu cầu nhóm so sánh trực tiếp SFO nguyên bản với SFO-VND trên toàn bộ 6 bộ benchmark CVRPLIB hay chỉ cần đối chứng trên 2-3 bộ đại diện (ví dụ `E-n33-k4` và `B-n50-k7`) trước khi áp dụng vào case study Tây Thạnh?
3. *Về kịch bản chịu tải:* Kịch bản phân tuyến tại Case Study hiện đang chia đều tải trọng cho 4 xe (khoảng 700–1120 kg/xe trên tải trọng tối đa 1500 kg). Thầy có yêu cầu thử nghiệm thêm kịch bản số xe tối thiểu $K=3$ để kiểm tra giới hạn chịu tải của thuật toán trong Step 3 hay không?

---

## 9. Phân công và kết quả thực tế của từng thành viên

### Bảng Phân công và kết quả thực tế

| Thành viên | Đầu việc đã làm | File/commit/log đối chứng (Đường dẫn Git) | Còn vướng |
| :--- | :--- | :--- | :--- |
| **Vũ Thế Quang**<br>*(Nhóm trưởng)* | • Khóa schema và kịch bản $K - Q - \text{demand}$.<br>• Xây dựng bộ kiểm định tự động `validate_dataset.py` (24 tiêu chí).<br>• Thiết lập nghiệm chứng khả thi `feasible_routes.json`.<br>• Theo dõi và tổng hợp giải quyết 8 vấn đề tồn tại (R1 – R8). | • [`tests/validate_dataset.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/validate_dataset.py)<br>• [`docs/reports/data_dictionary.md`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/docs/reports/data_dictionary.md)<br>• [`data/ward/processed/scenario.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/scenario.json)<br>• [`data/ward/processed/feasible_routes.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/feasible_routes.json)<br>• Commit: [`f56e1c9`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/commit/f56e1c9), [`2cd7474`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/commit/2cd7474), [`d94f60b`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/commit/d94f60b) | Cần chốt chính thức trọng số đa mục tiêu $(\alpha, \beta)$ giữa chi phí xăng dầu và phát thải $\text{CO}_2$ với Thầy hướng dẫn ở đầu Step 3. |
| **Lê Nguyễn Tâm Đức** | • Xử lý vấn đề địa danh hành chính Sơn Kỳ cũ.<br>• Trích xuất ranh giới GIS WGS84 Phường Tây Thạnh từ OSM.<br>• Tải đồ thị đường ô tô OSMnx buffer 400m, lưu file `.graphml`.<br>• Snap 51 điểm vào SCC, tính ma trận khoảng cách có hướng Dijkstra $51 \times 51$, xuất ảnh bản đồ số. | • [`src/map/extract_map.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/map/extract_map.py)<br>• [`data/ward/raw/ward_boundary.geojson`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/ward_boundary.geojson)<br>• [`data/ward/raw/road_network.graphml`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/road_network.graphml)<br>• [`data/ward/processed/distance_matrix.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/distance_matrix.csv)<br>• [`results/figures/map_boundary.png`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/figures/map_boundary.png)<br>• [`docs/reports/ward_selection.md`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/docs/reports/ward_selection.md)<br>• Commit: [`926ce3c`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/commit/926ce3c), [`0b81333`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/commit/0b81333) | Đã giải quyết triệt để vấn đề snap bằng cách chọn 50 điểm trực tiếp trên 13 tuyến đường ô tô của Phường Tây Thạnh, đưa khoảng cách snap về 0.0 m, 100% điểm hiển thị nằm khít trên mạng đường giao thông. |
| **Nguyễn Ngọc Thảo Hiền** | • Thu thập và chuẩn hóa 6 bộ benchmark quốc tế CVRPLIB (gồm cả 6 file `.vrp` và 6 file `.sol`).<br>• Viết parser nạp `cvrplib_loader.py` bằng `vrplib`.<br>• Kiểm tra quy ước làm tròn nguyên EUC_2D và lập bảng metadata đối chứng BKS.<br>• Xây dựng 25 unit tests trong `test_loader.py` (đối chứng 100% khớp BKS). | • [`data/benchmarks/raw/*.vrp & *.sol`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/tree/main/data/benchmarks/raw/)<br>• [`src/core/cvrplib_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/src/core/cvrplib_loader.py)<br>• [`results/benchmark_metadata.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/benchmark_metadata.csv)<br>• [`tests/test_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_loader.py)<br>• [`results/pytest_reproduce_hien.txt`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/pytest_reproduce_hien.txt) (commit [`56452dc`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/commit/56452dc)). | Bộ đọc `cvrplib_loader.py` hiện đã được xây dựng và kiểm thử trên 6 bộ benchmark CVRPLIB mà nhóm lựa chọn, sử dụng chuẩn khoảng cách EUC_2D và quy ước chỉ số Depot được chuẩn hóa về 0. Khi mở rộng sang các bộ dữ liệu khác như Set X, CMT hoặc các instance sử dụng kiểu khoảng cách EXPLICIT, GEO, nhóm cần kiểm tra quy ước dữ liệu của từng bộ, bao gồm cách biểu diễn khoảng cách, định dạng ma trận và chỉ số Depot. Ngoài ra, các biến thể bài toán có thêm ràng buộc như VRPTW cần được nghiên cứu và bổ sung cách xử lý phù hợp nếu nhóm có kế hoạch mở rộng phạm vi kiểm thử. |

### Đánh giá cá nhân của từng thành viên (3–5 câu)

* **Vũ Thế Quang:** Em đã xây dựng thành công bộ kiểm định tự động 24 tiêu chí và tạo bằng chứng phân tuyến khả thi chứng minh bài toán cấp phường hoàn toàn giải được với đội xe 4 chiếc tải trọng 1.5 tấn. Em đã kiểm chứng bằng chương trình thông qua việc chạy toàn bộ test suite Pytest đạt 40/40 passed và script `validate_dataset.py` đạt 24/24 PASS. Em chưa cài đặt chi tiết phần thuật toán SFO và bộ giải mã Split vì tuân thủ đúng yêu cầu phân định giai đoạn của Step 2, sẵn sàng bước vào Step 3.
* **Lê Nguyễn Tâm Đức:** Em đã giải quyết triệt để rào cản địa danh Sơn Kỳ cũ bằng việc trích xuất ranh giới chuẩn WGS84 của Phường Tây Thạnh từ OSMnx với vùng đệm 400m, lưu đồ thị mạng đường vĩnh viễn không phụ thuộc Internet. Em đã kiểm chứng bằng chương trình qua thuật toán Dijkstra có hướng, xác nhận 100% các điểm đều đi và về được Depot trên thành phần liên thông mạnh SCC 868 nút, ma trận có hướng phản ánh chính xác đường 1 chiều. Em cần học hỏi thêm về cơ chế mã hóa giải thuật của Step 3 để phối hợp viết toán tử tìm kiếm lân cận VND.
* **Nguyễn Ngọc Thảo Hiền:** Em đã thu thập, chuẩn hóa và kiểm tra 6 bộ dữ liệu benchmark CVRPLIB, bao gồm 6 file `.vrp` và 6 file `.sol`. Em xây dựng chương trình `cvrplib_loader.py` bằng thư viện `vrplib` để tự động đọc các thông tin như số lượng điểm, nhu cầu, sức chứa phương tiện, vị trí Depot và ma trận khoảng cách. Bên cạnh đó, em đã kiểm tra quy ước khoảng cách EUC_2D, xây dựng 25 unit tests trong `test_loader.py` và tính toán lại tổng khoảng cách để đối chiếu với giá trị BKS. Kết quả cho thấy cả 6 bộ dữ liệu đều có tổng khoảng cách tính theo quy ước làm tròn từng cạnh khớp với BKS công bố. Tuy nhiên, bộ đọc hiện tại mới được kiểm thử trên 6 bộ dữ liệu EUC_2D đã chọn; em chưa mở rộng sang các instance có định dạng khoảng cách khác và các biến thể bài toán có thêm ràng buộc như VRPTW.

---

## 10. Checklist tự đánh giá trước khi nộp

- [x] **01.** Đã xác định đúng tên phường hiện hành/khu vực nghiên cứu và có ranh giới có nguồn (*Phường Tây Thạnh, Quận Tân Phú; nguồn OSM Overpass API*).
- [x] **02.** Đã có dữ liệu mạng đường OSMnx được lưu và hiển thị trên bản đồ (*[`data/ward/raw/road_network.graphml`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/road_network.graphml), [`results/figures/map_boundary.png`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/figures/map_boundary.png)*).
- [x] **03.** Đã đọc được ít nhất 5–6 instance CVRPLIB và lưu file gốc (*Đầy đủ 6 file `.vrp` và 6 file `.sol` tại [`data/benchmarks/raw/`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/tree/main/data/benchmarks/raw/)*).
- [x] **04.** Đã kiểm tra dimension, depot, Q, demand và quy tắc tính khoảng cách benchmark (*Khớp 100% BKS, 25 tests pass trong [`tests/test_loader.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_loader.py)*).
- [x] **05.** Đã có instance nhỏ 10–20 điểm với seed và dữ liệu đầu vào rõ ràng (*Toy 12 điểm, `seed = 42`, [`data/toy/toy_instance.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_instance.json)*).
- [x] **06.** Đã chứng minh ít nhất một phương án chia tuyến nhỏ hợp lệ (*[`data/toy/toy_feasible_routes.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_feasible_routes.json), 3 xe, tổng cự ly 309.36m, 100% khả thi*).
- [x] **07.** Đã có cấu hình case study phường và ghi rõ dữ liệu thực/mô phỏng (*[`docs/reports/data_dictionary.md`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/docs/reports/data_dictionary.md), [`data/ward/processed/collection_points.csv`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/processed/collection_points.csv)*).
- [x] **08.** Đã kiểm tra tổng demand, K, Q và trường hợp điểm có demand lớn hơn Q (*$\sum q_i = 3,345\text{ kg} \le 6,000\text{ kg}$, bắt lỗi biên tại [`tests/test_toy_instance.py`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/tests/test_toy_instance.py)*).
- [x] **09.** Đã có ma trận đường bộ có hướng và kiểm tra đường đi/về depot (*Ma trận $51 \times 51$, Dijkstra trên SCC 868 nút, liên thông 100%*).
- [x] **10.** Các giá trị thiếu, không kết nối được báo rõ; không tự thay bằng 0 (*0 cặp vô cực $\infty$, tuyệt đối không gán 0 cho khoảng cách thiếu*).
- [x] **11.** Có data dictionary, nguồn tải, ngày tải, phiên bản và đơn vị đo (*[`docs/reports/data_dictionary.md`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/docs/reports/data_dictionary.md), phiên bản v1.0, ngày tải 24/10/2026*).
- [x] **12.** Các file raw được giữ nguyên; dữ liệu processed được đánh version (*Tách biệt hoàn toàn thư mục `raw/` và `processed/`*).
- [x] **13.** Các test tự động có kết quả PASS/FAIL và log kiểm chứng (*[`results/logs/validation_report.log`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/logs/validation_report.log) 24/24 PASS, 40/40 pytest passed*).
- [x] **14.** Một thành viên khác có thể chạy lại từ dữ liệu/script đã nộp (*Thành viên Nguyễn Ngọc Thảo Hiền đã chạy độc lập đạt 40 passed in 2.48s*).
- [x] **15.** Đã trả lời R1–R5 và phân loại rõ R6–R8 chuyển bước tiếp theo (*Khóa triệt để R1–R5 tại Step 2; định tuyến rõ R6–R8 sang Step 3/4/6/8*).
- [x] **16.** Có link Git commit và phân công có minh chứng từng thành viên (*Đầy đủ GitHub commit URL, bảng phân công nhiệm vụ và minh chứng log*).

---

## Phụ lục: Hình ảnh và Trích xuất Log kiểm định

### 1. Bản đồ ranh giới, đồ thị mạng đường và 50 điểm thu gom Phường Tây Thạnh
*Hình ảnh bản đồ mạng lưới giao thông ô tô kết hợp vị trí Trạm trung chuyển Depot và 50 điểm thu gom:*
* Đường dẫn Git: [`results/figures/map_boundary.png`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/figures/map_boundary.png)
* File đồ thị mạng đường: [`data/ward/raw/road_network.graphml`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/ward/raw/road_network.graphml)

### 2. Bản tính tay nghiệm phân tuyến Toy Instance (12 điểm)
*Hình ảnh sơ đồ và phép tính tay chứng minh tồn tại chu trình hợp lệ:*
* Đường dẫn Git: [`results/figures/toy_hand_calculation.png`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/results/figures/toy_hand_calculation.png)
* Cấu hình nghiệm JSON: [`data/toy/toy_feasible_routes.json`](https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting/blob/main/data/toy/toy_feasible_routes.json)

### 3. Trích xuất Log chạy kiểm định độc lập của Nguyễn Ngọc Thảo Hiền (`results/pytest_reproduce_hien.txt`)
```text
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.0.3, pluggy-1.7.0
rootdir: C:\Users\Asus\Downloads\SFO-VND_GreenWasteRouting-main
plugins: anyio-4.15.1
collected 40 items

tests\test_core_and_algorithms.py .......                                [ 17%]
tests\test_loader.py .........................                           [ 80%]
tests\test_toy_instance.py ........                                      [100%]

============================= 40 passed in 2.48s ==============================
```

### 4. Trích xuất Log tổng kết bộ kiểm định chất lượng dữ liệu (`results/logs/validation_report.log`)
```text
2026-11-14 16:59:14,025 [INFO] ================================================================================
2026-11-14 16:59:14,025 [INFO] BẮT ĐẦU CHẠY KIỂM ĐỊNH CHẤT LƯỢNG BỘ DỮ LIỆU STEP 2 (v1.0)
2026-11-14 16:59:14,025 [INFO] ================================================================================
2026-11-14 16:59:14,029 [INFO] [PASS] [1. Schema và Khóa] Cột bắt buộc collection_points.csv: Đầy đủ cột theo yêu cầu mục 18
2026-11-14 16:59:14,030 [INFO] [PASS] [1. Schema và Khóa] point_id duy nhất: Tổng 51 điểm, ID không trùng lặp
2026-11-14 16:59:14,030 [INFO] [PASS] [1. Schema và Khóa] Depot tồn tại trong points: Depot ID 0 có mặt trong danh sách
2026-11-14 16:59:14,031 [INFO] [PASS] [1. Schema và Khóa] Cột bắt buộc depot.csv: Đầy đủ cột depot.csv
2026-11-14 16:59:14,032 [INFO] [PASS] [1. Schema và Khóa] Cột bắt buộc vehicles.csv: Đầy đủ cột vehicles.csv
2026-11-14 16:59:14,033 [INFO] [PASS] [2. Giá trị và Đơn vị] Demand không âm: 100% demand >= 0 kg
2026-11-14 16:59:14,034 [INFO] [PASS] [2. Giá trị và Đơn vị] Mọi q_i <= Q: 100% điểm thu gom có q_i <= Q=1500.0 kg
2026-11-14 16:59:14,035 [INFO] [PASS] [2. Giá trị và Đơn vị] Khoảng cách không âm: 100% phần tử ma trận >= 0m
2026-11-14 16:59:14,035 [INFO] [PASS] [2. Giá trị và Đơn vị] Đường chéo d(i,i) = 0: 100% phần tử đường chéo = 0m
2026-11-14 16:59:14,037 [INFO] [PASS] [3. Tải trọng & Chứng cứ khả thi] Điều kiện cần: Tổng demand <= K x Q: Tổng demand = 3345.0 kg <= Tổng sức chứa = 6000.0 kg
2026-11-14 16:59:14,037 [INFO] [PASS] [3. Tải trọng & Chứng cứ khả thi] Tải trọng từng xe hợp lệ trong feasible_routes: Tất cả các tuyến đều không vượt quá sức chứa xe Q
2026-11-14 16:59:14,037 [INFO] [PASS] [3. Tải trọng & Chứng cứ khả thi] Phủ đủ 100% điểm khách hàng không bỏ sót: Đã phục vụ đủ 50/50 điểm thu gom rác
2026-11-14 16:59:14,038 [INFO] [PASS] [4. Mạng đường & Tính liên thông] File road_network.graphml tồn tại: Đồ thị đường gốc tại Source\data\ward\raw\road_network.graphml
2026-11-14 16:59:14,039 [INFO] [PASS] [4. Mạng đường & Tính liên thông] Mọi cặp điểm đều có đường đi (Không bị đứt đoạn): Không có cặp điểm nào bị vô cực (Dijkstra trên SCC)
2026-11-14 16:59:14,039 [INFO] [PASS] [4. Mạng đường & Tính liên thông] Có đường đi từ Depot đến mọi điểm: 100% điểm đến được từ depot
2026-11-14 16:59:14,039 [INFO] [PASS] [4. Mạng đường & Tính liên thông] Có đường quay về Depot từ mọi điểm: 100% điểm quay về được depot
2026-11-14 16:59:14,039 [INFO] [PASS] [4. Mạng đường & Tính liên thông] Tính chất có hướng của mạng đường (Asymmetric): Ma trận có hướng: d(i,j) khác d(j,i) do đường 1 chiều thực tế
2026-11-14 16:59:14,039 [INFO] [PASS] [5. Tính tái lập] Cố định Seed ngẫu nhiên (seed=42): Seed được khóa tại 42 để đảm bảo tái lập 100%
2026-11-14 16:59:14,039 [INFO] [PASS] [5. Tính tái lập] Quy tắc sinh dữ liệu và đơn vị đo rõ ràng: Rule: 35 điểm dân cư (35-75kg) + 15 điểm kinh doanh/thương mại (80-120kg)
2026-11-14 16:59:14,040 [INFO] [PASS] [6. Nguồn gốc dữ liệu] Phân loại nguồn dữ liệu minh bạch: Các phân loại nguồn: {'điểm thu gom giả lập trên mạng đường OSM', 'trạm trung chuyển chất thải quy hoạch'}
2026-11-14 16:59:14,040 [INFO] [PASS] [6. Nguồn gốc dữ liệu] File ranh giới ward_boundary.geojson: Ranh giới chuẩn WGS84 EPSG:4326 tại Source\data\ward\raw\ward_boundary.geojson
2026-11-14 16:59:14,048 [INFO] [PASS] [7. Benchmark CVRPLIB] Nạp thành công 6 bộ benchmark CVRPLIB gốc: Cả 6 file .vrp đọc đúng schema
2026-11-14 16:59:14,048 [INFO] [PASS] [7. Benchmark CVRPLIB] Bảng metadata CVRPLIB tồn tại (gồm cột Int & Float): Tệp kết quả đầy đủ cột Int/Float tại Source\results\benchmark_metadata.csv
2026-11-14 16:59:14,049 [INFO] [PASS] [7. Benchmark CVRPLIB] Tình trạng file nghiệm tham chiếu (.sol nếu có): Đã cấu hình parser vrplib.read_solution (hiện diện 6/6 file .sol cục bộ)
2026-11-14 16:59:14,049 [INFO] ================================================================================
2026-11-14 16:59:14,049 [INFO] TỔNG KẾT KIỂM ĐỊNH: 24/24 ĐẠT (PASS) | 0 THẤT BẠI (FAIL)
2026-11-14 16:59:14,049 [INFO] ================================================================================
```
