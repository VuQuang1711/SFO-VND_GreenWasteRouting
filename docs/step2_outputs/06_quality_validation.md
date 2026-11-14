# 🛡️ KẾT QUẢ 6: BỘ KIỂM ĐỊNH TỰ ĐỘNG 23 TIÊU CHÍ, TÍNH TÁI LẬP & PHÂN TÍCH CHUYÊN SÂU

> **Đơn vị:** Trường Đại học Công Thương Thành phố Hồ Chí Minh (HUIT)  
> **Đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu  
> **Thành viên phụ trách chính:** Vũ Thế Quang *(Nhóm trưởng - Quản lý Chất lượng QA & Kiểm thử tự động)*  
> **Tài liệu tham chiếu:** *STEP2_Huong_dan_chi_tiet_SFO_VND_Green_Waste_Routing.pdf (Mục 2.2, 2.7 & 4)*

---

## 📌 1. BẢNG TỔNG HỢP KẾT QUẢ KIỂM ĐỊNH CHẤT LƯỢNG DỮ LIỆU

Nhóm đã xây dựng bộ kiểm định tự động toàn diện [`tests/validate_dataset.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/validate_dataset.py) bao phủ **7 Hạng mục kiểm tra (Suites)** với **23 tiêu chí kỹ thuật**. Toàn bộ kết quả kiểm định được tự động ghi vết và khóa tại nhật ký [`results/logs/validation_report.log`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log).

| Hạng mục kiểm định (Suite) | Nội dung kiểm tra chi tiết | Tiêu chuẩn đạt | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :---: | :---: |
| **1. Schema và Khóa chính** | • Cột bắt buộc trong `collection_points.csv`<br>• Tính duy nhất của `point_id`<br>• Sự hiện diện của Depot ID = 0<br>• Cột bắt buộc trong `depot.csv`<br>• Cột bắt buộc trong `vehicles.csv` | Đủ 7 cột chuẩn; 51 ID duy nhất (0..50); Depot tồn tại; Đủ schema xe | Đủ 100% cột, không trùng ID, Depot ID 0 hợp lệ | **PASS** |
| **2. Giá trị và Đơn vị đo** | • Lượng rác không âm ($q_i \ge 0$)<br>• Mọi điểm không vượt tải xe ($q_i \le Q$)<br>• Khoảng cách không âm ($d_{ij} \ge 0$)<br>• Đường chéo bằng 0 ($d_{ii} = 0.0$) | Không có số âm; không có $q_i > 1500\text{ kg}$; $d_{ii} = 0.0\text{ m}$ | Thỏa mãn 100%; $q_{\max} = 120\text{ kg} \le 1500$; $d_{ii} = 0.0$ | **PASS** |
| **3. Tải trọng & Feasible Witness** | • Điều kiện cần: $\sum q_i \le K \times Q$<br>• Tải trọng từng xe hợp lệ ($\text{load}_k \le Q$)<br>• Phủ đủ 100% điểm khách, không lặp, không sót | $\sum q_i \le 6000\text{ kg}$; 4 xe đều $\le 1500\text{ kg}$; Phủ trọn vẹn 50 điểm | $3,345\text{ kg} \le 6,000\text{ kg}$; 4 xe tải: 1475, 1475, 395, 0 kg; đủ 50 điểm | **PASS** |
| **4. Mạng đường & SCC** | • File `road_network.graphml` tồn tại<br>• Mọi cặp điểm đều có đường đi ($d_{ij} < \infty$)<br>• Có đường đi từ Depot đến mọi điểm ($d_{0i} < \infty$)<br>• Có đường quay về Depot từ mọi điểm ($d_{i0} < \infty$)<br>• Tính chất có hướng của mạng đường | File đồ thị hợp lệ; 0 cặp bị vô cực; liên thông 2 chiều 100%; $d_{ij} \ne d_{ji}$ | 935 nút, 2123 cạnh; 0 ô vô cực; liên thông 2 chiều 100%; ma trận bất đối xứng | **PASS** |
| **5. Tính tái lập (Reproducibility)** | • Cố định Seed ngẫu nhiên (`seed = 42`)<br>• Quy tắc sinh dữ liệu và đơn vị đo rõ ràng | Có `seed: 42` tại `scenario.json`; đơn vị quy định rõ (kg, m) | Tái lập 100% dữ liệu qua mọi lần chạy lại | **PASS** |
| **6. Nguồn gốc dữ liệu** | • Phân loại nguồn minh bạch (OSM/mô phỏng)<br>• Ranh giới `ward_boundary.geojson` chuẩn | Không ngụy tạo số đo sensor thực tế; GeoJSON WGS84 EPSG:4326 | Gắn nhãn chuẩn OSMnx; GeoJSON hợp lệ từ Nominatim Overpass | **PASS** |
| **7. Benchmark CVRPLIB** | • Nạp thành công 6 bộ benchmark CVRPLIB<br>• Bảng metadata BKS tồn tại và khớp | Đọc được 6 file `.vrp`; khớp BKS; 19 unit tests pass | Đọc đầy đủ 6 bộ; khớp 100% BKS; 19 tests pass | **PASS** |

* **Tổng kết kiểm định tự động:** **23/23 ca kiểm tra ĐẠT (100% PASS)**, 0 lỗi, 0 cảnh báo.
* **Tổng kết bộ kiểm thử Pytest:** **34/34 unit tests PASS** ([`tests/test_loader.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_loader.py), [`tests/test_toy_instance.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_toy_instance.py), [`tests/test_core_and_algorithms.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_core_and_algorithms.py)).

---

## 🧠 2. PHÂN TÍCH CHUYÊN SÂU: TẠI SAO LẠI THỰC HIỆN NHƯ VẬY?

### 2.1. Tại sao phải xây dựng kịch bản kiểm định tự động thay vì kiểm tra thủ công?
1. **Loại bỏ hoàn toàn sai sót do con người:** Với 51 điểm thu gom và trạm trung chuyển, ma trận khoảng cách có $51 \times 51 = 2,601$ ô số. Con người không thể dùng mắt thường để quét hết 2,601 ô để phát hiện xem có ô nào bị âm, có ô nào bị vô cực ($\infty$), hay có giá trị nào trên đường chéo bị khác 0 hay không. Kịch bản `validate_dataset.py` quét toàn bộ ma trận chỉ trong $0.05$ giây với độ chính xác số học tuyệt đối.
2. **Cơ chế kiểm thử liên tục (Continuous Integration):** Bất cứ khi nào một thành viên trong nhóm chỉnh sửa hoặc bổ sung thêm điểm thu gom rác, việc chạy lại lệnh:
   ```bash
   py tests/validate_dataset.py
   ```
   sẽ ngay lập tức rà soát toàn bộ hệ thống. Nếu có bất kỳ vi phạm nào (như điểm mới nằm ngoài đồ thị, demand vượt sức chứa), hệ thống sẽ ném lỗi ngay lập tức, ngăn chặn việc dữ liệu bẩn lọt vào thuật toán tối ưu.

### 2.2. Nguyên lý Tái lập độc lập (Reproducibility & Offline-First) trong Nghiên cứu Khoa học
Căn cứ yêu cầu tại Mục 6 và Mục 24 Hướng dẫn Step 2 của GVHD:
> *"Mỗi thành viên phải chạy lại được ít nhất việc đọc benchmark và tải bộ dữ liệu đã lưu mà không cần chạy lại lệnh lấy OSM. Thực hiện chạy lại trên máy thành viên khác."*

* **Nguy cơ phụ thuộc mạng:** Nếu mỗi lần chạy mã nguồn, chương trình lại phải gửi yêu cầu lên OpenStreetMap (OSM) để tải dữ liệu bản đồ:
  - Máy chủ OSM có thể bị nghẽn mạng, thay đổi cấu trúc dữ liệu hoặc chặn truy vấn (HTTP 429 Too Many Requests / 403 Forbidden).
  - Tọa độ mạng đường có thể bị cộng đồng cập nhật làm thay đổi đồ thị, khiến kết quả nghiên cứu hôm nay khác với ngày mai.
* **Giải pháp "Offline-First" của nhóm:**
  - Nhóm trích xuất và lưu vĩnh viễn đồ thị mạng đường ô tô vào tệp chuẩn [`data/ward/raw/road_network.graphml`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml).
  - Khóa toàn bộ dữ liệu tọa độ và ma trận trong `data/ward/processed/`.
  - Cố định môi trường trong [`requirements.txt`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/requirements.txt) và mã nguồn nạp dữ liệu.
  - Nhờ vậy, bất kỳ thành viên nào hay hội đồng nghiệm thu đều có thể ngắt kết nối Internet hoàn toàn và chạy lại toàn bộ mã nguồn trên một máy tính độc lập mà vẫn thu được kết quả chính xác $100\%$.

### 2.3. Tại sao phải phân tách nghiêm ngặt giữa thư mục `raw/` và `processed/`?
* **Nguyên tắc "Bất biến của dữ liệu gốc" (Data Immutability):**
  - Thư mục `data/ward/raw/` và `data/benchmarks/raw/` chứa các dữ liệu nguyên bản tải về từ OpenStreetMap và CVRPLIB. Các tệp này được thiết lập ở trạng thái **Chỉ đọc (Read-only)**, tuyệt đối không được ghi đè hay chỉnh sửa thủ công.
  - Thư mục `data/ward/processed/` chỉ chứa các tệp là đầu ra của các script tiền xử lý tự động (`collection_points.csv`, `distance_matrix.csv`, `scenario.json`).
* Cách tổ chức này giúp dự án có khả năng truy vết nguồn gốc dữ liệu (Data Lineage) rõ ràng: Nếu có nghi vấn về một con số trong ma trận khoảng cách, nhóm có thể truy ngược từ ma trận $\to$ đồ thị `graphml` $\to$ ranh giới `geojson` $\to$ nguồn OSM một cách mạch lạc và khoa học.

---

## 📁 3. MINH CHỨNG VÀ LIÊN KẾT TỆP LIÊN QUAN

1. Script kiểm định 7 Suite: [`tests/validate_dataset.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/validate_dataset.py)
2. Tệp nhật ký ghi vết tự động: [`results/logs/validation_report.log`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log)
3. Danh mục gói thư viện môi trường: [`requirements.txt`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/requirements.txt)
4. Bộ kiểm thử đơn vị Pytest: [`tests/`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/) *(34 passed in 0.58s)*

