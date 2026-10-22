# BÁO CÁO TỔNG QUAN QUÁ TRÌNH PHÁT TRIỂN DỰ ÁN (DEMO 1)
### Đề tài: Tối ưu hóa Lộ trình Thu gom Rác thải Đô thị Xanh bằng Thuật toán Lai SFO-VND
---

## 1. CÂY THƯ MỤC BAN ĐẦU (INITIAL REPOSITORY SKELETON)

Trước khi triển khai, dự án chỉ có cấu trúc khung sườn (skeleton) với các thư mục rỗng và file `.gitkeep`:

```text
Source/
├── data/
│   ├── benchmarks/
│   │   └── .gitkeep
│   └── case_study/
├── docs/
│   └── .gitkeep
├── src/
│   ├── algorithms/
│   │   └── .gitkeep
│   ├── baselines/
│   │   └── .gitkeep
│   ├── core/
│   │   └── .gitkeep
│   ├── map/
│   │   └── .gitkeep
│   └── config.py
├── tests/
│   └── .gitkeep
├── web/
│   ├── static/
│   │   └── .gitkeep
│   └── templates/
│       └── .gitkeep
├── .gitignore
├── LICENSE
└── README.md
```

---

## 2. CÂY THƯ MỤC HOÀN CHỈNH HIỆN TẠI (CURRENT REPOSITORY TREE)

Toàn bộ các module thuật toán, dữ liệu, kiểm thử, bản đồ số GIS và ứng dụng web đã được hiện thực đầy đủ, đạt độ hoàn thiện cao:

```text
Source/
├── data/
│   ├── benchmarks/                         # 6 bộ dữ liệu chuẩn quốc tế CVRPLIB
│   │   ├── A-n53-k7.vrp
│   │   ├── A-n60-k9.vrp
│   │   ├── B-n50-k7.vrp
│   │   ├── E-n33-k4.vrp
│   │   ├── E-n51-k5.vrp
│   │   └── E-n76-k7.vrp
│   └── case_study/                         # Dữ liệu thực tế Phường Sơn Kỳ, Quận Tân Phú
│       ├── collection_points.csv           # 60 điểm gom rác sát vỉa hè 2 bên đường
│       └── distance_matrix.csv             # Ma trận khoảng cách thực tế giữa các điểm
├── docs/
│   └── .gitkeep
├── src/
│   ├── algorithms/                         # Lõi thuật toán tối ưu hóa thông minh
│   │   ├── __init__.py
│   │   ├── sfo.py                          # Thuật toán Bầy cá buồm (Sailfish Optimizer)
│   │   ├── vnd.py                          # Tìm kiếm lân cận biến đổi (Variable Neighborhood Descent)
│   │   └── hybrid_sfo_vnd.py               # Thuật toán lai ghép toàn diện SFO-VND
│   ├── baselines/                          # Thuật toán đối chứng truyền thống
│   │   ├── __init__.py
│   │   └── greedy.py                       # Tham lam chọn láng giềng gần nhất (Nearest Neighbor)
│   ├── core/                               # Các module cốt lõi của bài toán định tuyến
│   │   ├── __init__.py
│   │   ├── data_loader.py                  # Bộ nạp dữ liệu CVRPLIB (.vrp) & CSV Case Study
│   │   ├── decoder.py                      # Bộ giải mã Random Key & Split Decoder theo tải trọng
│   │   ├── evaluator.py                    # Đánh giá đa mục tiêu: Quãng đường, Nhiên liệu MEET, CO2 ISO 14064, Chi phí
│   │   └── validator.py                    # Kiểm tra 4 ràng buộc cứng của bài toán CVRP
│   ├── map/                                # Xử lý bản đồ số GIS và đồ thị đường giao thông
│   │   ├── __init__.py
│   │   ├── extract_map.py                  # Tải mạng đường bộ từ OpenStreetMap qua OSMnx
│   │   └── route_mapper.py                 # Xuất bản đồ Google Maps, định tuyến OSRM theo đường nhựa
│   └── config.py                           # Cấu hình tham số toàn cục (SFO, VND, MEET, ISO 14064)
├── tests/
│   ├── .gitkeep
│   └── test_core_and_algorithms.py         # Bộ 7 bài kiểm thử tự động (Unit & Integration Tests)
├── web/
│   ├── static/
│   │   └── .gitkeep
│   ├── templates/
│   │   └── .gitkeep
│   └── app.py                              # Ứng dụng Web Dashboard phân tích tối ưu hóa (Streamlit)
├── .gitignore                              # Cấu hình bỏ qua các file tạm/cache
├── Demo1.md                                # Báo cáo tổng hợp tiến độ và kiến trúc dự án
├── green_waste_routing_map.html            # Bản đồ tương tác hoàn chỉnh xuất từ thuật toán
├── LICENSE
├── main.py                                 # Điểm khởi chạy chương trình dòng lệnh (CLI Pipeline)
├── README.md
└── requirements.txt                        # Danh mục thư viện phụ thuộc của dự án
```

---

## 3. CHI TIẾT TẤT CẢ CÁC NỘI DUNG ĐÃ THỰC HIỆN

### 3.1. Thiết kế Kiến trúc 3 Lớp & Các Module Cốt Lõi (`src/core/`)
* **`config.py`**: Thiết lập toàn bộ hằng số toán học và thông số vật lý chuẩn quốc tế:
  - Thông số SFO: $N_{SF}=15$ (cá buồm), $N_S=45$ (cá mòi), $A=4.0$, $\epsilon=0.001$, $PP=0.1$.
  - Ràng buộc xe rác: Sức chứa tối đa $Q_{\max} = 1,500\text{ kg}$, Depot tại điểm `0`.
  - Mô hình tiêu thụ nhiên liệu MEET: Trọng lượng xe không tải $2,500\text{ kg}$, hệ số tiêu hao cơ sở $0.12\text{ L/km}$, hệ số tải trọng $\alpha = 0.00004\text{ L/km/kg}$.
  - Tiêu chuẩn ISO 14064-1:2018: Hệ số phát thải $2.68\text{ kg } CO_2\text{/L dầu Diesel}$, giá dầu $22,500\text{ VNĐ/L}$.
* **`data_loader.py`**: Tải và tiền xử lý dữ liệu chuẩn CVRPLIB (`.vrp`) và dữ liệu thực nghiệm địa bàn Phường Sơn Kỳ. Xử lý phòng thủ dữ liệu khuyết thiếu (NaN), trùng lặp tọa độ và tự động chuẩn hóa ID điểm bắt đầu từ Depot 0.
* **`decoder.py`**: 
  - Giải mã Random Key (`np.argsort`) chuyển vector số thực liên tục trong không gian tìm kiếm $[0, 1]^D$ thành hoán vị các điểm dừng.
  - Bộ giải mã cắt tuyến (`split_decoder`): Cắt chuỗi tour thành các chu trình con cho từng xe đảm bảo không bao giờ vượt quá sức chứa $Q_{\max}$, mỗi tuyến đều khép kín `[0, pt1, pt2, ..., 0]`.
  - Tái mã hóa (`tour_to_random_key`): Chuyển ngược tour rời rạc sau khi tối ưu VND về lại không gian liên tục để đồng bộ hóa cho bầy cá buồm SFO.
* **`evaluator.py`**: Tính toán đồng thời 4 chỉ số kinh tế - môi trường:
  $$\text{Tổng quãng đường } (km), \quad \text{Nhiên liệu tiêu thụ động theo tải rác } (Lít), \quad \text{Phát thải } CO_2\text{ } (kg), \quad \text{Chi phí vận hành } (VNĐ)$$
* **`validator.py`**: Xác thực tự động 4 ràng buộc cứng (Hard Constraints):
  1. Phục vụ đủ 100% các điểm rác, không bỏ sót bất kỳ điểm nào.
  2. Mỗi điểm rác chỉ được một xe ghé duy nhất một lần.
  3. Mọi tuyến xe đều bắt buộc xuất phát từ Depot và kết thúc tại Depot.
  4. Tổng lượng rác trên từng xe không vượt quá tải trọng $Q_{\max} = 1,500\text{ kg}$.

---

### 3.2. Lõi Thuật toán Tối ưu hóa Thông minh (`src/algorithms/` & `src/baselines/`)
* **`sfo.py` (Sailfish Optimizer)**: Cài đặt nguyên bản 13 phương trình toán học từ nghiên cứu gốc của Shadravan et al. (2019):
  - Mô phỏng cơ chế săn mồi tập thể của bầy cá buồm tấn công đàn cá mòi.
  - Cập nhật vị trí cá buồm theo tâm điểm giữa cá buồm đầu đàn ($X_{elite}$) và cá mòi bị thương nặng nhất ($X_{injured}$).
  - Tính toán lực tấn công suy giảm thích ứng $AP = A \times (1 - 2t / t_{\max})$ để cân bằng giữa khả năng khám phá (exploration) và khai thác (exploitation).
* **`vnd.py` (Variable Neighborhood Descent)**: Tìm kiếm lân cận biến đổi với 3 toán tử cục bộ:
  1. **2-opt**: Đảo ngược đoạn con trong hành trình để tháo gỡ các đoạn đường chéo giao cắt nhau.
  2. **Relocate**: Di chuyển 1 điểm gom rác từ vị trí kém sang vị trí tối ưu hơn trên cùng tuyến hoặc khác tuyến.
  3. **Swap**: Hoán đổi vị trí của 2 điểm dừng giữa hai xe để cân bằng tải trọng và rút ngắn khoảng cách.
  - *Cơ chế phòng thủ:* Khóa chặt hai đầu bến Depot `0`, không cho phép toán tử làm thay đổi điểm xuất phát/kết thúc.
* **`hybrid_sfo_vnd.py` (Hybrid SFO-VND)**: Kiến trúc lai ghép hoàn chỉnh:
  - SFO đóng vai trò tìm kiếm toàn cục trên diện rộng.
  - Định kỳ mỗi $K$ thế hệ, thuật toán kích hoạt VND để đào sâu tối ưu hóa cục bộ trên cá thể cá buồm xuất sắc nhất ($X_{elite}$).
  - Sau khi VND cải thiện nghiệm, giải thuật lập tức tái mã hóa (re-encoding) để đưa kết quả tối ưu vào lại không gian bầy đàn.
* **`greedy.py` (Greedy Nearest Neighbor)**: Cài đặt giải thuật láng giềng gần nhất làm phương pháp đối chứng truyền thống ("Before") để đo lường mức độ cải thiện của giải thuật đề xuất.

---

### 3.3. Dữ liệu Case Study Thực tế Phường Sơn Kỳ, Quận Tân Phú (`data/case_study/`)
* Khảo sát và xây dựng bộ dữ liệu gồm **60 điểm thu gom rác** (1 Depot trung tâm + 59 điểm rác).
* Các điểm được định vị chính xác nằm dọc theo **6 trục đường chính**: *Lê Trọng Tấn, đường Sơn Kỳ, Tân Kỳ Tân Quý, Bờ Bao Tân Thắng, đường Đỗ Nhuận, và hệ thống đường DC (DC1 đến DC13 quanh Chợ Sơn Kỳ)*.
* **Đặc điểm thực tế cao:** Các điểm rác được đặt so le hai bên lề đường (lề trái / lề phải), cách tim đường ~11 mét (tương ứng vị trí vỉa hè trước cửa từng số nhà dân, cổng chợ, trường học, khu chung cư Celadon City), khối lượng rác biến thiên từ 40 kg đến 240 kg.

---

### 3.4. Bản đồ số GIS & Công nghệ Định tuyến Đường nhựa Thực tế (`src/map/`)
Đã giải quyết triệt để vấn đề "đường chim bay đâm xuyên tòa nhà/trường học":
* **Nền bản đồ thực tế Google Maps:** Tích hợp lớp bản đồ Google Maps Đường phố và Google Maps Ảnh Vệ Tinh (Satellite Hybrid), tải tức thì tại Việt Nam, hiển thị rõ từng con đường, mái nhà, công viên và khu dân cư.
* **Định tuyến bám sát mặt đường (Turn-by-turn Road Routing via OSRM):**
  - Tích hợp công nghệ OSRM truy vấn mạng giao thông thực tế.
  - Tuyến xe chạy uốn lượn chính xác theo tim đường giao thông, ôm cua tại các ngã ba, ngã tư, đi đúng chiều đường nhựa.
  - Loại bỏ hoàn toàn đường thẳng chim bay và các dấu mũi tên tam giác gây rối mắt; thay bằng **dải màu nét liền liên tục, sắc nét và trơn mượt**.
* **Biểu diễn điểm dừng dạng hình tròn mang màu sắc của xe:**
  - Mỗi điểm dừng là một hình tròn có màu sắc tương ứng với xe phụ trách (Đỏ, Xanh dương, Xanh ngọc, Cam đất).
  - Viền trắng 2px sắc nét, **bên trong hiển thị số thứ tự ghé thăm (1, 2, 3...) được căn chính giữa tâm**.
* **Bộ điều khiển hiển thị đa chế độ (Layer Control & Filter Buttons):**
  - Cho phép người dùng bật/tắt để **xem riêng từng tuyến xe** (`[Chỉ Xe #1]`, `[Chỉ Xe #2]`, `[Chỉ Xe #3]`, `[Chỉ Xe #4]`) hoặc **xem toàn bộ đội xe** (`[Hiện tất cả]`).
  - Khi xem riêng từng xe, bản đồ hiển thị rõ ràng duy nhất **1 chu trình khép kín hoàn chỉnh**: Xuất phát từ Depot 0 $\to$ Thu gom lần lượt các điểm $\to$ Quay về Depot 0 xả rác hoàn tất.

---

### 3.5. Chương trình Dòng lệnh CLI (`main.py`) & Web App (`web/app.py`)
* **`main.py`**:
  - Hỗ trợ tham số linh hoạt (`--dataset`, `--iter`, `--sardines`, `--interval`, `--web`).
  - Xuất bảng Báo cáo Kết quả Đối chứng (Green Impact Report) so sánh Before vs After: Giảm ~20% quãng đường, tiết kiệm ~23% nhiên liệu và lượng phát thải $CO_2$.
  - Xuất sơ đồ hành trình chi tiết từng xe kèm tên địa chỉ thực tế, tải trọng thu gom và tỷ lệ lấp đầy xe.
* **`web/app.py`**: Giao diện trực quan hóa trên nền tảng Streamlit với 4 tab:
  - *Tab 1: Tổng quan dự án* (Mục tiêu, thông số xe, cấu hình mô hình).
  - *Tab 2: Bản đồ số lộ trình* (Nhúng trực tiếp bản đồ Folium/Google Maps tương tác).
  - *Tab 3: Green Impact Dashboard* (Bảng so sánh Before vs After, biểu đồ tiết kiệm nhiên liệu/CO2).
  - *Tab 4: XAI Inspector* (Giải thích cơ chế mô hình toán học và công thức MEET).

---

### 3.6. Hệ thống Kiểm thử Tự động (`tests/`)
* Đã xây dựng bộ kiểm thử tự động tại [test_core_and_algorithms.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_core_and_algorithms.py).
* Kiểm thử toàn diện 7 khía cạnh: Đọc file CVRPLIB, Kiểm tra 4 ràng buộc cứng, Mô hình tính phát thải $CO_2$, Tái mã hóa Random Key, Thuật toán SFO thuần túy, Toán tử lân cận VND, và Thuật toán lai ghép Hybrid SFO-VND.
* **Kết quả:** 100% Passed (7/7 tests) trong thời gian 0.1s.

---

<br>

<div align="right">
  <b>Author: Vũ Quang</b>
</div>
