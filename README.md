# 🚛 GreenWaste Route : Urban Waste Collection Routing Optimization Using Hybrid SFO-VND

> **Đề tài Nghiên cứu Khoa học Sinh viên**  
> **Tên đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị nhằm giảm chi phí và phát thải carbon bằng thuật toán Sailfish Optimizer lai Variable Neighborhood Descent.  
> **Phạm vi ứng dụng:** Case study tại một phường tại Thành phố Hồ Chí Minh (Phường Sơn Kỳ, Quận Tân Phú cũ).

---
## 👤 THÀNH VIÊN THỰC HIỆN
**Vũ Thế Quang**


**Nguyễn Ngọc Thảo Hiền**


**Lê Nguyễn Tâm Đức**


---
## 📌 1. Giới thiệu tổng quan (Overview)

Thu gom rác thải sinh hoạt đô thị là bài toán thực tiễn quan trọng diễn ra hằng ngày. Việc quy hoạch lộ trình xe thu gom chưa tối ưu dẫn đến quãng đường di chuyển kéo dài, gia tăng chi phí nhiên liệu và phát thải khí nhà kính ($\text{CO}_2$).

Dự án này nghiên cứu và phát triển mô hình định tuyến phương tiện có ràng buộc tải trọng xanh (**Green Capacitated Vehicle Routing Problem - GCVRP**), kết hợp:
* **Thuật toán tối ưu toàn cục:** **Sailfish Optimizer (SFO)** trên không gian số thực liên tục.
* **Cơ chế mã hóa/giải mã:** **Random-Key Encoding + Split Decoder** có xét tải trọng động.
* **Thuật toán tìm kiếm cục bộ:** **Variable Neighborhood Descent (VND)** với 3 cấu trúc lân cận: **2-opt**, **Relocate** và **Swap**.
* **Mô hình môi trường:** Ước tính lượng phát thải $\text{CO}_2$ theo tải trọng rác tích lũy trên từng cung đường (dựa trên mô hình tiêu thụ nhiên liệu MEET / chuẩn ISO 14064).
* **Ứng dụng Web:** Trực quan hóa lộ trình trên mạng đường thực tế từ **OpenStreetMap (OSMnx)** và đối chứng Before/After minh bạch.

---

## 🌟 2. Các tính năng cốt lõi (Key Features)

- [x] **Trích xuất mạng đường thực tế:** Tích hợp thư viện `OSMnx` & `NetworkX` để lập bản đồ giao thông thực tế cấp phường, tính ma trận khoảng cách đường bộ chính xác (không dùng đường chim bay).
- [x] **Lõi thuật toán lai SFO-VND:**
  - SFO khám phá đa dạng các vùng nghiệm trên miền liên tục.
  - Bộ giải mã Random-Key + Split đảm bảo nghiệm sinh ra luôn hợp lệ về tải trọng ($Q_{\max}$) và số xe ($K$).
  - VND khai thác sâu để gỡ đường cắt chéo (2-opt), chuyển điểm (Relocate) và tráo đổi điểm giữa các xe (Swap).
- [x] **Đánh giá môi trường động:** Tính toán chi phí và lượng $\text{CO}_2$ dựa trên tải trọng xe tăng dần sau mỗi điểm thu gom.
- [x] **Thực nghiệm Benchmark CVRPLIB chuẩn quốc tế:** Đối chiếu chất lượng với Best Known Solutions (BKS), Google OR-Tools, GA và mô hình quy hoạch nguyên MILP trên các bộ chuẩn: `E-n33-k4`, `B-n50-k7`, `E-n51-k5`, `A-n53-k7`, `A-n60-k9`, `E-n76-k7`.
- [x] **GreenWaste Route Dashboard:** Giao diện Web hiển thị bản đồ đa màu cho từng xe, bảng kê chi tiết lộ trình, phân tích kịch bản phát sinh (**What-if**) và biểu đồ hội tụ trực quan (**Live Convergence Curve**).

---

## 🔄 3. Quy trình xử lý của hệ thống (Pipeline)

```text
[Dữ liệu OSMnx & Collection Points] 
           │
           ▼
[Tính Ma trận khoảng cách đường bộ] 
           │
           ▼
[Quần thể SFO (Vector số thực liên tục)] 
           │
           ▼
[Bộ giải mã Random-Key + Split Decoder] ──► Tuyến xe hợp lệ (Feasible Routes)
           │
           ▼
[Hàm đánh giá Fitness: Chi phí + CO2 động + Phạt]
           │
           ▼
[Tinh chỉnh cục bộ VND (2-opt ➔ Relocate ➔ Swap)] ──► Cập nhật nghiệm ưu tú
           │
           ▼
[Kiểm tra điều kiện dừng (Max Iterations / Time)]
           │
           ▼
[Giao diện Web: Bản đồ đường thực + Dashboard Before/After]
```

---

## 📂 4. Cấu trúc thư mục chuẩn hóa (Standardized Repository Structure)

Dự án được chuẩn hóa cấu trúc theo Quy chuẩn Step 2 (phân định minh bạch giữa dữ liệu gốc `raw` và dữ liệu xử lý `processed`):

```text
SFO-VND_GreenWasteRouting/
├── data/
│   ├── benchmarks/
│   │   └── raw/               # 6 bộ dữ liệu chuẩn CVRPLIB (.vrp, .sol)
│   ├── toy/                   # Instance kiểm thử nhỏ 12 điểm (tính tay & test biên)
│   │   ├── toy_12_points.csv
│   │   ├── toy_instance.json
│   │   └── toy_feasible_routes.json
│   └── ward/
│       ├── raw/               # Ranh giới GIS WGS84, mạng đường gốc road_network.graphml
│       └── processed/         # 50 điểm thu gom, depot, vehicles, ma trận Dijkstra, scenario, feasible witness
├── src/
│   ├── algorithms/
│   │   ├── sfo.py             # Lõi thuật toán Sailfish Optimizer
│   │   ├── vnd.py             # 3 toán tử: 2-opt, Relocate, Swap
│   │   └── hybrid_sfo_vnd.py  # Thuật toán lai hoàn chỉnh SFO-VND
│   ├── core/
│   │   ├── cvrplib_loader.py  # Bộ nạp CVRPLIB chuẩn quốc tế dùng vrplib
│   │   ├── data_loader.py     # Bộ nạp dữ liệu định tuyến phòng thủ
│   │   ├── decoder.py         # Bộ giải mã Random-Key + Split Decoder
│   │   ├── evaluator.py       # Hàm tính Fitness, Nhiên liệu & Phát thải CO2 (MEET/ISO 14064)
│   │   └── validator.py       # Kiểm tra 4 điều kiện cứng của nghiệm
│   ├── map/
│   │   ├── extract_map.py     # Trích xuất ranh giới, đồ thị có hướng, snap và Dijkstra
│   │   └── route_mapper.py    # Ánh xạ tọa độ và vẽ tuyến lên Folium/Leaflet
│   └── baselines/
│       ├── greedy_baseline.py # Phương án Before (Nearest Neighbor)
│       └── ga_baseline.py     # Giải thuật Di truyền (GA) đối chứng
├── web/                       # Ứng dụng Web Demo
│   ├── static/                # CSS, JS, Icon
│   └── templates/             # Giao diện HTML bản đồ
├── tests/                     # Bộ kiểm thử tự động (57/57 tests PASS)
│   ├── test_loader.py         # Kiểm tra nạp 6 bộ benchmark CVRPLIB
│   ├── test_toy_instance.py   # Kiểm tra 8 ca biên cho instance nhỏ
│   ├── validate_dataset.py    # Kiểm định 7 Suite chất lượng dữ liệu
│   └── test_core_and_algorithms.py
├── docs/                      # Tài liệu và báo cáo theo dõi
│   ├── ward_selection.md      # So sánh khu vực nghiên cứu & ranh giới OSM
│   ├── data_dictionary.md     # Từ điển dữ liệu chi tiết nguồn gốc & đơn vị
│   ├── feasibility_report.md  # Báo cáo khả thi & theo dõi các vấn đề Step 1 (R1-R8)
│   └── step2_report.md        # Báo cáo tổng thể nghiệm thu Step 2
├── results/                   # Bằng chứng kết quả & kiểm tra
│   ├── figures/               # map_boundary.png, map.png, toy_hand_calculation.png
│   ├── logs/                  # validation_report.log
│   └── benchmark_metadata.csv # Bảng metadata 6 bộ CVRPLIB
├── requirements.txt           # Danh sách thư viện Python thực tế
├── .gitignore
└── README.md
```

---

## 👥 5. Thành viên nhóm nghiên cứu (Team Members)

| STT | Họ và tên | Ngành | Vai trò & Trách nhiệm chính trong Step 2 |
| :---: | :--- | :---: | :--- |
| 1 | **Vũ Thế Quang** *(Nhóm trưởng)* | Khoa Học Dữ Liệu | Khóa schema, kịch bản $K-Q-\text{demand}$; tạo validator tự động, feasible witness; theo dõi R1–R8. |
| 2 | **Lê Nguyễn Tâm Đức** | Khoa Học Dữ Liệu | Xác định phường nghiên cứu, trích xuất ranh giới GIS OSMnx, xử lý đồ thị có hướng và tính ma trận khoảng cách Dijkstra. |
| 3 | **Nguyễn Ngọc Thảo Hiền** | Khoa Học Dữ Liệu | Tải và kiểm tra 6 bộ benchmark CVRPLIB, lập bảng metadata và xây dựng bộ kiểm thử nạp benchmark `test_loader.py`. |

---

## 🛠️ 6. Cài đặt và Chạy kiểm thử Step 2 (Quickstart)

```bash
# 1. Kích hoạt môi trường Python (Python 3.13)
# Trên Windows PowerShell / Command Prompt:
.venv\Scripts\activate

# 2. Cài đặt các thư viện phụ thuộc đã khóa phiên bản
pip install -r requirements.txt

# 3. Chạy bộ kiểm định chất lượng dữ liệu 7 Suite (Công việc 2.7)
python tests/validate_dataset.py

# 4. Chạy toàn bộ các bài kiểm thử tự động (57/57 tests PASS)
python -m pytest tests/

# 5. Kiểm tra đọc bộ dữ liệu Benchmark CVRPLIB (Công việc 2.3)
python src/core/cvrplib_loader.py
```
