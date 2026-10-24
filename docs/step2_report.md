# 📑 BÁO CÁO NGHIỆM THU NỘI BỘ STEP 2: CHUẨN BỊ VÀ KHÓA BỘ DỮ LIỆU

> **Tên đề tài:** Tối ưu lộ trình thu gom rác đô thị bằng Sailfish Optimizer lai Variable Neighborhood Descent (SFO–VND)  
> **Chương trình:** Nghiên cứu Khoa học Sinh viên  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu  
> **Thời điểm nghiệm thu:** 2026-10-24  
> **Nhóm sinh viên thực hiện:**  
> 1. **Vũ Thế Quang** *(Nhóm trưởng)*  
> 2. **Lê Nguyễn Tâm Đức**  
> 3. **Nguyễn Ngọc Thảo Hiền**  

---

## 🎯 1. Mục tiêu của Step 2 & Tuyên bố hoàn thành

Căn cứ theo tài liệu giao việc từ Thầy hướng dẫn:  
> *"Mục tiêu của bước này: Có bộ dữ liệu nhỏ chạy thử được, bộ benchmark đọc đúng và một case study cấp phường có nguồn gốc rõ ràng. Chưa cần cài SFO hay VND."*

Nhóm xin trân trọng báo cáo đã **hoàn thành 100% tất cả các đầu ra và minh chứng** theo đúng yêu cầu, không ghi đè dữ liệu gốc, phân định rõ ràng giữa file gốc (`raw`) và file xử lý (`processed`), đồng thời khóa phiên bản dữ liệu **v1.0** để làm tiền đề vững chắc bước sang **Step 3**.

---

## 👥 2. Phân công trách nhiệm và Bằng chứng nộp theo thành viên

Tuân thủ đúng bảng phân công tại Mục 3 của Hướng dẫn Step 2:

| Thành viên phụ trách | Nhiệm vụ chính trong Step 2 | Bằng chứng nộp cụ thể (Tệp đính kèm) | Trạng thái |
| :--- | :--- | :--- | :---: |
| **Vũ Thế Quang**<br>*(Nhóm trưởng)* | • Khóa schema và kịch bản $K - Q - \text{demand}$.<br>• Xây dựng bộ kiểm định tự động `validate_dataset.py`.<br>• Thiết lập minh chứng khả thi (`feasible_routes.json`).<br>• Theo dõi và tổng hợp giải quyết 8 vấn đề tồn tại (R1 – R8). | • [data_dictionary.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/data_dictionary.md)<br>• [scenario.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/scenario.json)<br>• [validate_dataset.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/validate_dataset.py)<br>• [feasibility_report.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/feasibility_report.md) | **HOÀN THÀNH (PASS)** |
| **Lê Nguyễn Tâm Đức** | • Xác định phường nghiên cứu, đối chiếu ranh giới GIS.<br>• Tải và làm sạch mạng đường ô tô có hướng qua OSMnx.<br>• Snap Depot và 50 điểm thu gom, tính ma trận khoảng cách có hướng Dijkstra. | • [ward_selection.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/ward_selection.md)<br>• [ward_boundary.geojson](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson)<br>• [road_network.graphml](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml)<br>• [extract_map.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/map/extract_map.py)<br>• [distance_matrix.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/distance_matrix.csv)<br>• [map_boundary.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/map_boundary.png) & [map.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/map.png) | **HOÀN THÀNH (PASS)** |
| **Nguyễn Ngọc Thảo Hiền** | • Tải và chuẩn hóa 6 bộ dữ liệu chuẩn quốc tế CVRPLIB.<br>• Viết parser `cvrplib_loader.py` dùng thư viện `vrplib`.<br>• Lập bảng metadata chuẩn và xây dựng bộ kiểm thử `test_loader.py`. | • 6 file `.vrp` trong [data/benchmarks/raw/](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/)<br>• [cvrplib_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/core/cvrplib_loader.py)<br>• [benchmark_metadata.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/benchmark_metadata.csv)<br>• [test_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_loader.py) | **HOÀN THÀNH (PASS)** |

---

## 📋 3. Bảng đối chiếu các Tiêu chí nghiệm thu (Mục 4)

| Mốc kiểm tra | Tiêu chuẩn đạt | Kết quả thực tế của nhóm | Đánh giá |
| :--- | :--- | :--- | :---: |
| **Dữ liệu benchmark** | • 5–6 instance đọc được.<br>• Parser kiểm tra trường cơ bản.<br>• Ghi nguồn và đối chứng tham chiếu. | • Đọc đầy đủ **6/6 instance**: `E-n33-k4`, `B-n50-k7`, `E-n51-k5`, `A-n53-k7`, `A-n60-k9`, `E-n76-k7`.<br>• Sử dụng `vrplib.read_instance`, kiểm tra dimension, capacity, demand, depot, EUC_2D.<br>• Bảng metadata chi tiết tại [benchmark_metadata.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/benchmark_metadata.csv).<br>• 19 unit tests đạt 100% tại `test_loader.py`. | **ĐẠT (PASS)** |
| **Dữ liệu nhỏ (Toy)** | • 10–20 điểm.<br>• Dữ liệu hợp lệ.<br>• Có ít nhất 1 phương án tuyến xác nhận tính khả thi. | • Xây dựng bộ dữ liệu **12 điểm khách + 1 depot** ($K=3, Q=200$ kg).<br>• Tổng demand = 420 kg $\le 600$ kg.<br>• Phương án khả thi 3 tuyến (Tải: 140kg, 135kg, 145kg; Tổng quãng đường: 309.36m).<br>• Vượt qua 8 unit test kiểm thử biên tại `test_toy_instance.py`.<br>• Minh chứng tại [toy_hand_calculation.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/toy_hand_calculation.png). | **ĐẠT (PASS)** |
| **Case study cấp phường** | • Có ranh giới kiểm chứng và mạng đường.<br>• Có bộ dữ liệu xử lý ban đầu.<br>• Có khả năng đi/về depot. | • Ranh giới GeoJSON EPSG:4326 của **Phường Tây Thạnh (Quận Tân Phú)** từ OpenStreetMap.<br>• Đồ thị xe ô tô buffer 400m với 935 nút, 2123 cạnh (SCC 868 nút).<br>• Đặt 1 Depot tại KCN Tân Bình và 50 điểm thu gom (35 dân cư, 15 kinh doanh).<br>• $100\%$ các điểm đều liên thông 2 chiều với Depot. | **ĐẠT (PASS)** |
| **Ma trận đường bộ** | • Đúng ID, đơn vị, có hướng.<br>• Không có giá trị thiếu bị thay bằng 0. | • Ma trận $51 \times 51$, đơn vị mét, Dijkstra có hướng.<br>• Đường chéo bằng 0.0, không có cặp vô cực.<br>• Tính bất đối xứng phản ánh đường 1 chiều ($d(i,j) \ne d(j,i)$).<br>• Đã đối chiếu thủ công 3 cặp điểm và 1 vòng khép kín tại `feasibility_report.md`. | **ĐẠT (PASS)** |
| **Minh bạch & Tái lập** | • Script + seed + metadata + file gốc + phiên bản thư viện đủ để chạy lại. | • Cố định `seed = 42` tại `scenario.json`.<br>• Thư mục chuẩn hóa: `raw` tách biệt hoàn toàn `processed`.<br>• Bộ thư viện thực tế được ghi nhận chính xác tại [requirements.txt](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/requirements.txt): Python 3.13.14, `vrplib 2.2.0`, `osmnx 2.1.1`, `geopandas 1.2.0`, `networkx 3.6.1`. | **ĐẠT (PASS)** |
| **Vấn đề Step 1 (R1–R8)** | • R1–R5 có kết quả/biện pháp.<br>• R6–R8 ghi rõ chuyển sang bước sau. | • R1–R5 đã giải quyết triệt để và khóa tại Step 2.<br>• R6 (MEET/ISO 14064): Liệt kê thông số, chuyển khóa ở Step 3.<br>• R7 (Split/VND cập nhật ngược): Chuyển thiết kế vào Step 3 & 6.<br>• R8 (Quy mô lớn 300–400 điểm, What-if): Chuyển sang Step 4/6/8. | **ĐẠT (PASS)** |

---

## 🛠️ 4. Báo cáo Kết quả Kiểm định Chất lượng (Quality Assurance)

Nhóm đã thực thi toàn bộ các bài kiểm thử tự động với kết quả tuyệt đối:
* **Bộ kiểm tra nạp Benchmark CVRPLIB:** `19/19 passed` ([test_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_loader.py))
* **Bộ kiểm tra Toy Instance 8 ca biên:** `8/8 passed` ([test_toy_instance.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_toy_instance.py))
* **Bộ kiểm định toàn diện 7 Suite dữ liệu:** `23/23 passed` ([validate_dataset.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/validate_dataset.py))
* **Bộ kiểm tra tích hợp giải thuật nền:** `7/7 passed` ([test_core_and_algorithms.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_core_and_algorithms.py))
* **Tổng số ca kiểm thử tự động:** **57/57 tests PASS (100%)**.

Toàn bộ nhật ký kiểm thử chi tiết được tự động lưu vết tại:
👉 [results/logs/validation_report.log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log)

---

## 🚀 5. Kiến nghị & Kế hoạch chuyển sang Step 3

Dựa trên các tiêu chí nghiệm thu nghiêm ngặt của Thầy hướng dẫn:
1. **Dữ liệu đáng tin cậy:** Đã có nguồn ranh giới GIS kiểm chứng, đồ thị đường bộ OSMnx được lưu vĩnh viễn dưới dạng `road_network.graphml` (chạy lại offline không cần gọi lại OSM), ma trận khoảng cách có hướng chính xác, không còn giá trị ảo.
2. **Minh chứng khả thi:** Đã chứng minh cả trên instance nhỏ (12 điểm) và instance cấp phường (50 điểm) đều tồn tại các nghiệm khả thi, không bị vượt tải.

Nhóm kính đề xuất Thầy hướng dẫn **chính thức nghiệm thu Step 2 và phê duyệt cho nhóm chuyển sang Step 3**:
* Triển khai chi tiết thuật toán Sailfish Optimizer (SFO).
* Thiết kế bộ giải mã Random-Key + Split tối ưu hóa tải trọng rác tích lũy.
* Tích hợp hàm mục tiêu Fitness đa tiêu chí: Chi phí vận hành kinh tế + Phát thải $\text{CO}_2$ theo mô hình MEET / ISO 14064.
