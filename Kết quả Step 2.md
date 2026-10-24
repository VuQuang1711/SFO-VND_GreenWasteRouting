# 📊 TỔNG HỢP KẾT QUẢ THỰC NGHIỆM VÀ KIỂM ĐỊNH STEP 2

> **Đề tài:** Tối ưu hóa lộ trình thu gom rác đô thị bằng Sailfish Optimizer lai Variable Neighborhood Descent (SFO–VND)  
> **Nội dung:** Biên bản ghi nhận kết quả chạy thực tế của toàn bộ các script kiểm định, bộ test tự động và parser dữ liệu Step 2.  
> **Thời điểm thực thi:** 24/10/2026  
> **Môi trường:** Python 3.13.14 (Windows AMD64)  

---

## 📌 1. BẢNG KẾT QUẢ KIỂM ĐỊNH DỮ LIỆU (VALIDATION REPORT)

Lệnh thực thi:
```powershell
py tests/validate_dataset.py
```

### Kết quả chi tiết 7 Suite kiểm định chất lượng:

| STT | Hạng mục (Suite) | Nội dung kiểm tra | Kết quả | Ghi chú & Đánh giá |
| :---: | :--- | :--- | :---: | :--- |
| 1 | **1. Schema và Khóa** | Cột bắt buộc `collection_points.csv` | **PASS** | Đủ 7 cột: `point_id, latitude, longitude, demand_kg, point_type, source_type, snapped_node` |
| 2 | **1. Schema và Khóa** | `point_id` duy nhất | **PASS** | 51 điểm (1 depot + 50 khách), không có ID trùng |
| 3 | **1. Schema và Khóa** | Depot tồn tại trong points | **PASS** | Depot ID = 0 có mặt và được gán nhãn loại `depot` |
| 4 | **1. Schema và Khóa** | Cột bắt buộc `depot.csv` | **PASS** | Đầy đủ: `depot_id, latitude, longitude, source_type, snapped_node` |
| 5 | **1. Schema và Khóa** | Cột bắt buộc `vehicles.csv` | **PASS** | Đầy đủ: `vehicle_id, capacity_kg, available` |
| 6 | **2. Giá trị và Đơn vị** | Demand không âm | **PASS** | $100\%$ điểm thu gom có $\text{demand} \ge 0.0\text{ kg}$ |
| 7 | **2. Giá trị và Đơn vị** | Mọi $q_i \le Q$ | **PASS** | Không có điểm nào vượt tải trọng xe ($Q = 1500.0\text{ kg}$) |
| 8 | **2. Giá trị và Đơn vị** | Khoảng cách không âm | **PASS** | $100\%$ phần tử ma trận $D[i, j] \ge 0.0\text{ m}$ |
| 9 | **2. Giá trị và Đơn vị** | Đường chéo $d(i, i) = 0$ | **PASS** | Khoảng cách từ một điểm tới chính nó luôn bằng $0.0\text{ m}$ |
| 10 | **3. Tải trọng & Khả thi** | Điều kiện cần: $\sum q_i \le K \times Q$ | **PASS** | Tổng $\text{demand} = 3,329.0\text{ kg} \le \text{Tổng tải } 6,000.0\text{ kg}$ |
| 11 | **3. Tải trọng & Khả thi** | Tải trọng từng xe hợp lệ | **PASS** | Cả 4 xe trong `feasible_routes.json` đều $\le 1500.0\text{ kg}$ |
| 12 | **3. Tải trọng & Khả thi** | Phục vụ đủ 100% khách hàng | **PASS** | Đã phục vụ đủ 50/50 điểm thu gom, không sót điểm nào |
| 13 | **4. Mạng đường & Liên thông** | File `road_network.graphml` tồn tại | **PASS** | Đồ thị mạng đường trích xuất từ OSMnx lưu vĩnh viễn |
| 14 | **4. Mạng đường & Liên thông** | Mọi cặp điểm đều có đường đi | **PASS** | Không có cặp điểm nào bị vô cực (Dijkstra trên SCC) |
| 15 | **4. Mạng đường & Liên thông** | Có đường đi từ Depot đến mọi điểm | **PASS** | $100\%$ điểm khách hàng đều đến được từ Depot ($D[0, i] < \infty$) |
| 16 | **4. Mạng đường & Liên thông** | Có đường quay về Depot từ mọi điểm | **PASS** | $100\%$ điểm khách hàng đều quay về được Depot ($D[i, 0] < \infty$) |
| 17 | **4. Mạng đường & Liên thông** | Tính chất có hướng của mạng đường | **PASS** | $D[i, j] \ne D[j, i]$ phản ánh chính xác đường 1 chiều |
| 18 | **5. Tính tái lập** | Cố định Seed ngẫu nhiên (`seed=42`) | **PASS** | Khóa seed ngẫu nhiên tại 42 trong `scenario.json` |
| 19 | **5. Tính tái lập** | Quy tắc sinh dữ liệu & đơn vị đo rõ ràng | **PASS** | Đơn vị chuẩn: kg (khối lượng), mét (khoảng cách) |
| 20 | **6. Nguồn gốc dữ liệu** | Phân loại nguồn dữ liệu minh bạch | **PASS** | Gắn nhãn đúng `điểm thu gom giả lập trên mạng đường OSM` |
| 21 | **6. Nguồn gốc dữ liệu** | File ranh giới `ward_boundary.geojson` | **PASS** | Ranh giới hành chính chuẩn WGS84 EPSG:4326 |
| 22 | **7. Benchmark CVRPLIB** | Nạp thành công 6 bộ benchmark CVRPLIB | **PASS** | Đọc chuẩn xác cả 6 file `.vrp` chính thức |
| 23 | **7. Benchmark CVRPLIB** | Bảng metadata CVRPLIB tồn tại | **PASS** | File `results/benchmark_metadata.csv` đầy đủ trường |

* **Tổng số ca kiểm tra:** **23/23 ĐẠT (100% PASS)**  
* **Đường dẫn file nhật ký (Log):** [results/logs/validation_report.log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log)

---

## 🧪 2. KẾT QUẢ CHẠY BỘ KIỂM THỬ TỰ ĐỘNG (PYTEST)

Lệnh thực thi:
```powershell
py -m pytest tests/
```

### Nhật ký kiểm thử:
```text
============================== test session starts ===============================
platform win32 -- Python 3.13.14, pytest-9.0.3, pluggy-1.6.0
rootdir: E:\15DHKHDL03\2026-2027\HKI_26_27\SFO_VND\Source
plugins: anyio-4.14.2, platformdirs-4.12.2
collected 34 items

tests\test_core_and_algorithms.py .......                                   [ 20%]
tests\test_loader.py ...................                                    [ 76%]
tests\test_toy_instance.py ........                                         [100%]

=============================== 34 passed in 0.59s ===============================
```

### Phân rã 34 bài kiểm thử:
1. **`tests/test_core_and_algorithms.py` (7 tests):** Kiểm tra nạp dữ liệu, bộ giải mã Split Decoder, tính phát thải $CO_2$ theo MEET/ISO 14064, thuật toán SFO và toán tử VND.
2. **`tests/test_loader.py` (19 tests):** Kiểm tra cấu trúc metadata, số lượng khách hàng, sức chứa, ma trận khoảng cách đối xứng EUC_2D và không vượt tải cho cả 6 bộ benchmark CVRPLIB.
3. **`tests/test_toy_instance.py` (8 tests):** Kiểm tra trường hợp chuẩn khả thi và 7 ca lỗi biên nghiêm ngặt (ID trùng, demand âm/thiếu, $q_i > Q$, thiếu depot, đứt đường đến/về depot, số xe vượt $K$, phục vụ lặp điểm hoặc bỏ sót điểm).

---

## 📚 3. KẾT QUẢ ĐỌC VÀ ĐỐI CHỨNG 6 BỘ BENCHMARK CVRPLIB

Lệnh thực thi:
```powershell
py src/core/cvrplib_loader.py
```

### Thông số kỹ thuật chi tiết của 6 bộ dữ liệu chuẩn:

```text
======================================================================
BÁO CÁO THÔNG SỐ INSTANCE: E-n33-k4
======================================================================
Các trường đọc được : ['capacity', 'comment', 'demand', 'depot', 'dimension', 'edge_weight', 'edge_weight_type', 'name', 'node_coord', 'type']
Tên instance         : E-n33-k4
Dimension            : 33 (Khách hàng: 32, Depot: 1)
Sức chứa xe Q        : 8,000.0 đơn vị
Vị trí Depot         : Node index 0
Kiểu khoảng cách     : EUC_2D (Euclid 2 chiều)
Ma trận khoảng cách  : Kích thước (33, 33), Kiểu: float64
Tổng nhu cầu rác     : 29,370.0 đơn vị
Giá trị tối ưu BKS   : 835
Ghi chú nguồn        : (Christophides and Eilon, Min no of trucks: 4, Optimal value: 835)
======================================================================

======================================================================
BÁO CÁO THÔNG SỐ INSTANCE: B-n50-k7
======================================================================
Các trường đọc được : ['capacity', 'comment', 'demand', 'depot', 'dimension', 'edge_weight', 'edge_weight_type', 'name', 'node_coord', 'type']
Tên instance         : B-n50-k7
Dimension            : 50 (Khách hàng: 49, Depot: 1)
Sức chứa xe Q        : 100.0 đơn vị
Vị trí Depot         : Node index 0
Kiểu khoảng cách     : EUC_2D (Euclid 2 chiều)
Ma trận khoảng cách  : Kích thước (50, 50), Kiểu: float64
Tổng nhu cầu rác     : 609.0 đơn vị
Giá trị tối ưu BKS   : 741
Ghi chú nguồn        : (Augerat et al, No of trucks: 7, Optimal value: 741)
======================================================================

======================================================================
BÁO CÁO THÔNG SỐ INSTANCE: E-n51-k5
======================================================================
Các trường đọc được : ['capacity', 'comment', 'demand', 'depot', 'dimension', 'edge_weight', 'edge_weight_type', 'name', 'node_coord', 'type']
Tên instance         : E-n51-k5
Dimension            : 51 (Khách hàng: 50, Depot: 1)
Sức chứa xe Q        : 160.0 đơn vị
Vị trí Depot         : Node index 0
Kiểu khoảng cách     : EUC_2D (Euclid 2 chiều)
Ma trận khoảng cách  : Kích thước (51, 51), Kiểu: float64
Tổng nhu cầu rác     : 777.0 đơn vị
Giá trị tối ưu BKS   : 521
Ghi chú nguồn        : (Christophides and Eilon, Min no of trucks: 5, Optimal value: 521)
======================================================================

======================================================================
BÁO CÁO THÔNG SỐ INSTANCE: A-n53-k7
======================================================================
Các trường đọc được : ['capacity', 'comment', 'demand', 'depot', 'dimension', 'edge_weight', 'edge_weight_type', 'name', 'node_coord', 'type']
Tên instance         : A-n53-k7
Dimension            : 53 (Khách hàng: 52, Depot: 1)
Sức chứa xe Q        : 100.0 đơn vị
Vị trí Depot         : Node index 0
Kiểu khoảng cách     : EUC_2D (Euclid 2 chiều)
Ma trận khoảng cách  : Kích thước (53, 53), Kiểu: float64
Tổng nhu cầu rác     : 664.0 đơn vị
Giá trị tối ưu BKS   : 1,010
Ghi chú nguồn        : (Augerat et al, No of trucks: 7, Optimal value: 1010)
======================================================================

======================================================================
BÁO CÁO THÔNG SỐ INSTANCE: A-n60-k9
======================================================================
Các trường đọc được : ['capacity', 'comment', 'demand', 'depot', 'dimension', 'edge_weight', 'edge_weight_type', 'name', 'node_coord', 'type']
Tên instance         : A-n60-k9
Dimension            : 60 (Khách hàng: 59, Depot: 1)
Sức chứa xe Q        : 100.0 đơn vị
Vị trí Depot         : Node index 0
Kiểu khoảng cách     : EUC_2D (Euclid 2 chiều)
Ma trận khoảng cách  : Kích thước (60, 60), Kiểu: float64
Tổng nhu cầu rác     : 829.0 đơn vị
Giá trị tối ưu BKS   : 1,354
Ghi chú nguồn        : (Augerat et al, No of trucks: 9, Optimal value: 1354)
======================================================================

======================================================================
BÁO CÁO THÔNG SỐ INSTANCE: E-n76-k7
======================================================================
Các trường đọc được : ['capacity', 'comment', 'demand', 'depot', 'dimension', 'edge_weight', 'edge_weight_type', 'name', 'node_coord', 'type']
Tên instance         : E-n76-k7
Dimension            : 76 (Khách hàng: 75, Depot: 1)
Sức chứa xe Q        : 220.0 đơn vị
Vị trí Depot         : Node index 0
Kiểu khoảng cách     : EUC_2D (Euclid 2 chiều)
Ma trận khoảng cách  : Kích thước (76, 76), Kiểu: float64
Tổng nhu cầu rác     : 1,364.0 đơn vị
Giá trị tối ưu BKS   : 682
Ghi chú nguồn        : (Christophides and Eilon, Min no of trucks: 7, Optimal value: 682)
======================================================================
```

---

## 🏆 4. KẾT LUẬN NGHIỆM THU STEP 2

Căn cứ vào kết quả thực nghiệm trên máy tính và toàn bộ mã nguồn:
1. **Dữ liệu chuẩn CVRPLIB:** Đọc đúng định dạng 6/6 bộ, đối chiếu khớp giá trị tham chiếu BKS công bố quốc tế.
2. **Bộ dữ liệu nhỏ Toy Instance:** 12 điểm hợp lệ, có phương án phân tuyến chứng minh tính khả thi, vượt qua 8/8 bài kiểm tra biên.
3. **Bộ dữ liệu Case Study Cấp Phường (Tây Thạnh):** Ranh giới WGS84 kiểm chứng từ OpenStreetMap, mạng đường ô tô có hướng liên thông 100%, 50 điểm thu gom có tọa độ và khoảng cách snap rõ ràng, tồn tại phương án phân tuyến 4 xe hợp lệ về tải trọng.
4. **Chất lượng kiểm định:** Đạt **100% PASS** trên cả 23 tiêu chuẩn kiểm định dữ liệu và 34 bài unit test.

Bộ dữ liệu Step 2 đã sẵn sàng chuyển giao làm đầu vào cho **Step 3 (Thiết kế và cài đặt thuật toán SFO-VND)**.
