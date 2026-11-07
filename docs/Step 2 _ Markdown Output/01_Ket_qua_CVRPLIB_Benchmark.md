# 🏆 KẾT QUẢ 1: BỘ BENCHMARK CVRPLIB CHUẨN QUỐC TẾ & PHÂN TÍCH CHUYÊN SÂU

> **Đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu  
> **Thành viên phụ trách chính:** Nguyễn Ngọc Thảo Hiền *(Data & Benchmark Specialist)*  
> **Tài liệu tham chiếu:** *STEP2_Huong_dan_chi_tiet_SFO_VND_Green_Waste_Routing.pdf (Mục 2.3 & 3)*

---

## 📌 1. BẢNG TỔNG HỢP KẾT QUẢ ĐẦU RA BỘ BENCHMARK

Nhóm đã tải lại, giải mã và thẩm định độc lập **6 bộ dữ liệu chuẩn quốc tế CVRPLIB** (Capacitated Vehicle Routing Problem Library) từ các tác giả kinh điển (Christofides & Eilon 1969, Augerat et al. 1995). Toàn bộ 6 file gốc được giữ nguyên vẹn trong thư mục [`data/benchmarks/raw/`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/).

| Tên Instance | Tệp dữ liệu gốc (.vrp/.sol) | Số điểm $N$ (gồm Depot) | Số khách $n$ | Đội xe $K$ | Sức chứa $Q$ | Kiểu khoảng cách | BKS Tham chiếu (Công bố) | Kết quả Parser nhóm tính lại | Trạng thái đối chứng |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E-n33-k4** | [E-n33-k4.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/E-n33-k4.vrp) / [.sol](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/E-n33-k4.sol) | 33 | 32 | 4 | 8,000 | `EUC_2D` | **835** | **835** | **KHỚP 100% (PASS)** |
| **B-n50-k7** | [B-n50-k7.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/B-n50-k7.vrp) / [.sol](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/B-n50-k7.sol) | 50 | 49 | 7 | 100 | `EUC_2D` | **741** | **741** | **KHỚP 100% (PASS)** |
| **E-n51-k5** | [E-n51-k5.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/E-n51-k5.vrp) / [.sol](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/E-n51-k5.sol) | 51 | 50 | 5 | 160 | `EUC_2D` | **521** | **521** | **KHỚP 100% (PASS)** |
| **A-n53-k7** | [A-n53-k7.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/A-n53-k7.vrp) / [.sol](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/A-n53-k7.sol) | 53 | 52 | 7 | 100 | `EUC_2D` | **1,010** | **1,010** | **KHỚP 100% (PASS)** |
| **A-n60-k9** | [A-n60-k9.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/A-n60-k9.vrp) / [.sol](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/A-n60-k9.sol) | 60 | 59 | 9 | 100 | `EUC_2D` | **1,354** | **1,354** | **KHỚP 100% (PASS)** |
| **E-n76-k7** | [E-n76-k7.vrp](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/E-n76-k7.vrp) / [.sol](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/E-n76-k7.sol) | 76 | 75 | 7 | 220 | `EUC_2D` | **682** | **682** | **KHỚP 100% (PASS)** |

* Toàn bộ siêu dữ liệu đã được xuất tự động tại [`results/benchmark_metadata.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/benchmark_metadata.csv).
* Kiểm thử tự động đạt kết quả **25/25 unit tests PASS** tại [`tests/test_loader.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_loader.py) (bao gồm 6 ca đối chứng khớp 100% với file `.sol`).

---

## 🧠 2. PHÂN TÍCH CHUYÊN SÂU: TẠI SAO LẠI THỰC HIỆN NHƯ VẬY?

### 2.1. Tại sao đề tài nghiên cứu phải sử dụng bộ dữ liệu CVRPLIB?
1. **Tiêu chuẩn học thuật quốc tế:** CVRPLIB là bộ chuẩn mực vàng (Gold Standard) được toàn bộ cộng đồng nghiên cứu VRP thế giới sử dụng từ năm 1969 đến nay. Khi nghiên cứu một thuật toán mới như **Sailfish Optimizer lai Variable Neighborhood Descent (Hybrid SFO-VND)**, muốn chứng minh thuật toán có tính đột phá thì phải đối chứng trên cùng một "sân chơi" tiêu chuẩn với các thuật toán nổi tiếng như GA, PSO, ALNS.
2. **Loại trừ sai số chủ quan từ dữ liệu:** Nếu chỉ thử nghiệm trên dữ liệu tự sinh tại Phường Tây Thạnh, hội đồng khoa học sẽ đặt câu hỏi: *"Liệu thuật toán chạy tốt là do thuật toán thông minh hay do dữ liệu tự tạo quá dễ giải?"*. Việc vượt qua 6 bộ benchmark CVRPLIB chứng minh độ tin cậy toán học tuyệt đối của thuật toán trước khi áp dụng vào thực tiễn.

### 2.2. Tại sao phải sử dụng thư viện chuyên dụng `vrplib` thay vì tự viết parser bằng regex hay chuỗi?
* Cấu trúc file `.vrp` chuẩn TSPLIB/CVRPLIB chứa nhiều phần phức tạp (`NODE_COORD_SECTION`, `DEMAND_SECTION`, `DEPOT_SECTION`, `EOF`). Nhiều instance có số lượng khoảng trắng, định dạng xuống dòng và quy ước chỉ số Depot khác nhau (1-based index).
* Việc tự bóc tách bằng regex thủ công dễ dẫn tới:
  - Bỏ sót dòng Depot hoặc nhầm lẫn giữa ID khách hàng $1..N$ với chỉ số mảng $0..N-1$.
  - Nhầm lẫn số chiều `DIMENSION`: Trong CVRPLIB, `DIMENSION = 33` nghĩa là gồm **1 Depot + 32 Khách hàng**. Nếu parser tự viết không trừ 1 sẽ gây sai lệch kích thước bài toán.
* Do đó, nhóm sử dụng thư viện tiêu chuẩn `vrplib.read_instance()` trong [`src/core/cvrplib_loader.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/core/cvrplib_loader.py) để đảm bảo tuân thủ 100% chuẩn định dạng quốc tế.

### 2.3. Tại sao bắt buộc phải làm tròn nguyên từng cạnh theo quy tắc TSPLIB `nint`?
Đây là một "bẫy" kỹ thuật rất phổ biến trong nghiên cứu VRP:
* Trong các bài toán CVRPLIB có `EDGE_WEIGHT_TYPE: EUC_2D`, quy ước TSPLIB quốc tế bắt buộc khoảng cách giữa hai tọa độ $(x_i, y_i)$ và $(x_j, y_j)$ phải được tính và **làm tròn thành số nguyên gần nhất ngay trên từng cạnh**:
  $$d(i, j) = \text{round}\left(\sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}\right)$$
* **Hậu quả nếu làm sai:** Nếu giữ nguyên số thực dấu phẩy động (`float`), cộng dồn toàn bộ hành trình rồi mới làm tròn ở kết quả cuối cùng, tổng quãng đường sẽ bị lệch từ $1 - 4$ đơn vị so với BKS (Best Known Solution) đã công bố. Khi đó, bài báo hoặc báo cáo khoa học sẽ bị coi là sai quy ước kỹ thuật.
* Nhóm đã lập trình chính xác quy tắc này trong hàm `compute_distance_matrix(instance, round_euclidean=True)`.

### 2.4. Tại sao tuyệt đối KHÔNG ĐƯỢC gộp BKS khoảng cách CVRPLIB với hàm Fitness xanh ở Case Study?
Căn cứ lưu ý nghiêm ngặt của GVHD tại trang 3 tài liệu hướng dẫn:
> *"CVRPLIB phục vụ đánh giá CVRP theo chi phí khoảng cách gốc. Không mặc nhiên xem tọa độ benchmark là vị trí địa lý tại TP.HCM, không đổi đơn vị benchmark sang km/CO₂ và không so BKS khoảng cách với fitness chi phí–phát thải của case study."*

* **Bản chất của BKS CVRPLIB:** Mục tiêu đơn nhất là cực tiểu hóa tổng chiều dài hình học vô hướng trên mặt phẳng Euclid ($\min \sum d_{ij}$).
* **Bản chất của Green Case Study:** Là bài toán thực tế đa mục tiêu, cự ly là đường bộ thực tế có hướng qua OSMnx, mức tiêu hao nhiên liệu và phát thải $\text{CO}_2$ phụ thuộc vào **tải trọng rác tích lũy biến thiên** trên xe:
  $$\text{Fuel} = d_{uv} \times \left( f_{\text{empty}} + \alpha_{\text{load}} \cdot w_{uv} \right)$$
  Một lộ trình ngắn nhất về khoảng cách chưa chắc đã tiết kiệm nhiên liệu nhất nếu nó bắt xe chở tải nặng đi qua các cung đường tắc nghẽn hoặc đường dốc.
* Việc tách bạch rạch ròi 2 mục tiêu này giúp đề tài giữ vững tính liêm chính học thuật và chuẩn mực khoa học.

---

## 📁 3. MINH CHỨNG VÀ LIÊN KẾT TỆP LIÊN QUAN

1. Tệp siêu dữ liệu: [`results/benchmark_metadata.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/benchmark_metadata.csv)
2. Bộ kiểm thử tự động: [`tests/test_loader.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_loader.py)
3. Module xử lý: [`src/core/cvrplib_loader.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/core/cvrplib_loader.py)
4. Thư mục chứa 6 file .vrp gốc: [`data/benchmarks/raw/`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/)

