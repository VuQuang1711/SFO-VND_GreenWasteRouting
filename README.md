# 🚛 GreenWaste Route AI: Urban Waste Collection Routing Optimization Using Hybrid SFO-VND

> **Đề tài Nghiên cứu Khoa học Sinh viên**  
> **Tên đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị nhằm giảm chi phí và phát thải carbon bằng thuật toán Sailfish Optimizer lai Variable Neighborhood Descent.  
> **Phạm vi ứng dụng:** Case study tại một phường tại Thành phố Hồ Chí Minh (Phường Sơn Kỳ, Quận Tân Phú cũ).

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

## 📂 4. Cấu trúc thư mục dự án giả định trên module của Quang (Repository Structure)

```text
SFO-VND-Green-Waste-Routing/
├── data/
│   ├── benchmarks/            # 6 bộ dữ liệu chuẩn CVRPLIB (.vrp, .sol)
│   ├── collection_points.csv  # Danh sách điểm thu gom (ID, Lat, Lon, Demand)
│   └── distance_matrix.csv    # Ma trận khoảng cách mạng đường thực tế
├── src/
│   ├── algorithms/
│   │   ├── sfo.py             # Lõi thuật toán Sailfish Optimizer
│   │   ├── vnd.py             # 3 toán tử: 2-opt, Relocate, Swap
│   │   └── hybrid_sfo_vnd.py  # Thuật toán lai hoàn chỉnh SFO-VND
│   ├── core/
│   │   ├── decoder.py         # Bộ giải mã Random-Key + Split Decoder
│   │   ├── evaluator.py       # Hàm tính Fitness, Nhiên liệu & Phát thải CO2
│   │   └── validator.py       # Hàm kiểm tra 4 điều kiện cứng của nghiệm
│   ├── map/
│   │   ├── extract_map.py     # Trích xuất đồ thị đường phố qua OSMnx
│   │   └── route_mapper.py    # Ánh xạ tọa độ và vẽ tuyến lên Folium/Leaflet
│   └── baselines/
│       ├── greedy_baseline.py # Phương án Before (Nearest Neighbor)
│       └── ga_baseline.py     # Giải thuật Di truyền (GA) đối chứng
├── web/                       # Ứng dụng Web Demo
│   ├── static/                # CSS, JS, Icon
│   └── templates/             # Giao diện HTML bản đồ
├── tests/                     # Unit test kiểm tra bộ giải mã và hàm mục tiêu
├── docs/                      # Báo cáo Step 1, Step 2 và mô hình toán học
├── requirements.txt           # Danh sách thư viện Python cần cài đặt
├── .gitignore
└── README.md
```

---

## 👥 5. Thành viên nhóm nghiên cứu (Team Members)

| STT | Họ và tên | MSSV / Lớp | Vai trò & Trách nhiệm chính |
| :---: | :--- | :---: | :--- |
| 1 | **Vũ Thế Quang** *(Nhóm trưởng)* | 15DHKHDL03 | Phụ trách mô hình toán học, thuật toán lõi SFO, bộ giải mã Random-Key + Split Decoder và hàm đánh giá phát thải $\text{CO}_2$. |
| 2 | **Lê Nguyễn Tâm Đức** | 15DHKHDL04 | Phụ trách mạng đường thực tế (OSMnx/NetworkX), xử lý dữ liệu bản đồ Case Study cấp phường và xây dựng giao diện hiển thị tuyến đường. |
| 3 | **Nguyễn Ngọc Thảo Hiền** | 15DHKHDL06 | Phụ trách bộ dữ liệu Benchmark CVRPLIB, thuật toán Baseline đối chứng (Tham lam, GA) và thống kê kết quả thực nghiệm. |

---

## 🛠️ 6. Cài đặt và Bắt đầu nhanh (Quickstart)

```bash
# 1. Clone kho lưu trữ về máy
git clone https://github.com/VuQuang1711/SFO-VND_GreenWasteRouting.git
cd SFO-VND-Green-Waste-Routing

# 2. Tạo môi trường ảo Python
python -m venv .venv
# Kích hoạt trên Windows:
.venv\Scripts\activate

# 3. Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt
```
