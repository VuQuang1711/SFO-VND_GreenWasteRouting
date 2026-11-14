# 📘 HƯỚNG DẪN TOÀN DIỆN VỀ STEP 2: NHỮNG GÌ ĐÃ LÀM VÀ TẠI SAO LẠI LÀM NHƯ VẬY?

> **Đơn vị đào tạo:** Trường Đại học Công Thương Thành phố Hồ Chí Minh (HUIT)  
> **Tên tài liệu:** Cẩm nang Học thuật & Kỹ thuật Nghiệm thu Step 2 — Chuẩn bị và Khóa Bộ Dữ liệu  
> **Đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai Sailfish Optimizer kết hợp Variable Neighborhood Descent (Hybrid SFO–VND)  
> **Nhóm thực hiện:** Vũ Thế Quang *(Nhóm trưởng)*, Lê Nguyễn Tâm Đức, Nguyễn Ngọc Thảo Hiền  
> **Mục tiêu của tài liệu:** Giúp từng thành viên nắm vững **từng việc nhóm đã làm**, **bản chất lý do khoa học tại sao phải làm như vậy**, từ đó tự tin thuyết trình, đối thoại và bảo vệ xuất sắc trước Giảng viên hướng dẫn (GVHD) và Hội đồng chấm điểm.

---

## 🎯 TỔNG QUAN: VỊ TRÍ CỦA STEP 2 TRONG TOÀN BỘ ĐỀ TÀI

### 1. Step 2 là gì?
Căn cứ theo đề cương của GVHD:  
> *"Mục tiêu của bước này: Có bộ dữ liệu nhỏ chạy thử được, bộ benchmark đọc đúng và một case study cấp phường có nguồn gốc rõ ràng. Chưa cần cài SFO hay VND."*

Step 2 là giai đoạn **Chuẩn bị, Làm sạch, Kiểm định và Khóa cứng Bộ Dữ liệu Đầu vào (Data Freezing)**.

### 2. Triết lý khoa học: Tại sao phải làm Step 2 cẩn thận mà chưa vội cài SFO hay VND?
Trong Khoa học Dữ liệu và Trí tuệ Nhân tạo, có một nguyên lý bất biến: **"Garbage In, Garbage Out"** *(Dữ liệu rác thì đầu ra luôn là rác)*:
* Nếu ma trận khoảng cách bị đứt đường, có cung vô cực ($\infty$), thuật toán tối ưu sẽ bị sập (`crash`).
* Nếu tổng lượng rác của các điểm vượt quá tổng sức chứa của đội xe ($Q_{\text{total}} < \sum q_i$), thì dù thuật toán có chạy $100,000$ thế hệ cũng chỉ sinh ra các nghiệm vi phạm bị phạt nặng, không bao giờ tìm được nghiệm khả thi.
* Nếu không có dữ liệu benchmark chuẩn quốc tế, nhóm sẽ không thể chứng minh được thuật toán tự viết là đúng hay sai so với thế giới.
* Do đó, **Step 2 chính là việc đổ móng xây nhà**. Móng có vững thì bước sang Step 3 cài thuật toán mới không bị lung lay hay phải đập đi xây lại dữ liệu!

---

## 🧭 BẢN ĐỒ CÁC NỘI DUNG ĐÃ LÀM VÀ TẠI SAO LẠI LÀM NHƯ VẬY

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   STEP 2: KHÓA BỘ DỮ LIỆU                              │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
    ┌───────────────────┬───────────────────┼───────────────────┬───────────────────┐
    ▼                   ▼                   ▼                   ▼                   ▼
[1. Địa bàn GIS]    [2. Mạng đường]     [3. CVRPLIB]        [4. Toy Instance]   [5. Case Study]
Chọn Phường Tây     Đồ thị OSMnx        Đọc 6 file chuẩn    12 điểm + 1 Depot   50 điểm + 1 Depot
Thạnh, Buffer 400m  SCC 868 nút ô tô    Làm tròn TSPLIB     Tính tay 3 tuyến    K=4, Q=1500kg
Depot KCN Tân Bình  Dijkstra có hướng   Khớp 100% BKS       8 test bắt biên     Feasible Witness
```

---

# PHẦN I: CHI TIẾT TỪNG NỘI DUNG ĐÃ LÀM VÀ NGUYÊN DO KHOA HỌC (WHAT & WHY)

---

## 📍 1. LỰA CHỌN ĐỊA BÀN NGHIÊN CỨU & XỬ LÝ RANH GIỚI HÀNH CHÍNH

### Những gì nhóm đã làm:
1. Đánh giá 3 khu vực ứng viên: Phường Tây Thạnh (Tân Phú), Phường Tân Sơn Nhì (Tân Phú), Phường Bình Hưng Hòa (Bình Tân).
2. **Quyết định chọn:** **Phường Tây Thạnh, Quận Tân Phú, TP. Hồ Chí Minh**.
3. Trích xuất ranh giới số chuẩn WGS84 EPSG:4326 dạng Polygon từ OpenStreetMap qua Overpass API (`admin_level = 8`).
4. Thiết lập vùng đệm mở rộng **Buffer 400 mét**.
5. Bố trí Trạm trung chuyển (Depot) tại tọa độ $(10.8122, 106.6215)$ nằm trong khuôn viên **Khu công nghiệp Tân Bình thuộc Phường Tây Thạnh**, tiếp giáp trực tiếp đường trục CN13.
6. Lưu trữ minh chứng: [ward_selection.md](../reports/ward_selection.md), [ward_boundary.geojson](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson), ảnh [map_boundary.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/map_boundary.png).

---

### TẠI SAO LẠI LÀM NHƯ VẬY?

#### ❓ Tại sao không giữ tên "Phường Sơn Kỳ" cũ như trong thuyết minh ban đầu?
* **Thực tế hành chính:** Địa danh lịch sử "Phường Sơn Kỳ" sau các đợt sắp xếp địa giới hành chính của TP.HCM đã được phân bổ về các phường lân cận (Bình Hưng Hòa, Tây Thạnh, Tân Sơn Nhì). Hiện nay trên bản đồ hành chính chính thức không còn đơn vị độc lập mang tên Phường Sơn Kỳ cấp phường pháp lý nữa.
* **Lý do khoa học:** Nếu nhóm tự vẽ ranh giới "Sơn Kỳ cũ" theo cảm tính, Hội đồng sẽ bắt bẻ ngay: *"Ranh giới này lấy từ đâu? Căn cứ pháp lý nào?"*. Do đó, nhóm chuyển sang chọn **Phường Tây Thạnh** – một đơn vị hành chính cấp 8 hiện hành có mã định danh OpenStreetMap chính thống, đồng thời kế thừa trực tiếp dữ liệu khảo sát thực địa từ Step 1 (dọc trục Lê Trọng Tấn). Đây là bước xử lý thể hiện sự trung thực học thuật và tính chuyên nghiệp cao.

#### ❓ Tại sao phải mở rộng vùng đệm (Buffer) 400m mà không cắt sát mép ranh giới phường?
* **Hiện tượng "đứt gãy mạng đường biên" (Boundary Effect):** Các trục đường huyết mạch bao quanh phường (như Lê Trọng Tấn, CN1, CN13, Chế Lan Viên) thường nằm ngay trên mép ranh giới hành chính. Nếu cắt sát ranh giới, đồ thị đường bộ sẽ bị "cắt ngang xương", dẫn đến việc xe gom rác chạy đến ranh giới phường thì biến thành ngõ cụt, không thể quay đầu hay kết nối ra đường lớn.
* **Vùng đệm 400m** (nằm đúng dải khuyến nghị chuẩn $300 - 500\text{m}$ của ngành GIS) giúp đồ thị giữ trọn vẹn các nút giao thông, bùng binh quay đầu và đường vành đai lân cận, bảo đảm xe tải vận hành thông suốt.

#### ❓ Tại sao lại đặt Depot tại Khu công nghiệp Tân Bình?
* Xe ép rác là phương tiện chuyên dụng chở chất thải nặng mùi. Trong quy hoạch đô thị thực tế, **không ai cho phép đặt bãi tập kết xe rác trong lõi khu dân cư đông đúc**. 
* KCN Tân Bình nằm ngay trong Phường Tây Thạnh, có đường lớn cho xe tải trọng tải lớn ra vào, tiếp giáp đường CN13, hoàn toàn phù hợp với quy chuẩn quy hoạch hạ tầng kỹ thuật đô thị.

---

## 🛣️ 2. TRÍCH XUẤT ĐỒ THỊ MẠNG ĐƯỜNG & MA TRẬN KHOẢNG CÁCH CÓ HƯỚNG

### Những gì nhóm đã làm:
1. Dùng thư viện `osmnx` tải đồ thị xe ô tô (`network_type = "drive"`) trong phạm vi ranh giới mở rộng. Đồ thị gồm **935 nút và 2,123 cạnh**.
2. Lưu đồ thị gốc vĩnh viễn thành tệp chuẩn XML: [data/ward/raw/road_network.graphml](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/road_network.graphml).
3. Lọc và trích xuất **Thành phần Liên thông Mạnh lớn nhất (SCC - Strongly Connected Component)** gồm **868 nút** (chiếm $92.8\%$).
4. Ánh xạ (Snap) toàn bộ 51 điểm (1 Depot + 50 điểm gom) vào nút ô tô gần nhất thuộc tập SCC này; ghi lại khoảng cách snap (`snap_distance_m`).
5. Sử dụng thuật toán **Dijkstra có hướng** tính toán ma trận khoảng cách $51 \times 51$ với đơn vị là **mét (m)**: [distance_matrix.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/distance_matrix.csv).
6. Đối chiếu thủ công bằng tay 3 cặp điểm hai chiều và 1 vòng khép kín trong `feasibility_report.md`.

---

### TẠI SAO LẠI LÀM NHƯ VẬY?

#### ❓ Tại sao tuyệt đối KHÔNG ĐƯỢC dùng khoảng cách hình học Euclid (Đường chim bay)?
* Khoảng cách chim bay $d = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$ giả định xe có thể bay thẳng qua nhà dân, sông ngòi, công viên.
* Đô thị thực tế có **đường một chiều** và **dải phân cách cứng**: Hai nhà đối diện nhau qua đường chỉ cách nhau 15m chim bay, nhưng xe ô tô phải đi xuôi chiều 500m tới ngã tư rồi mới quay đầu ngược lại 500m (tổng cộng hơn 1 km). Nếu tối ưu theo đường chim bay, toàn bộ lộ trình đưa cho tài xế sẽ bị phá sản!

#### ❓ Thành phần Liên thông Mạnh (SCC) là gì và tại sao bắt buộc phải lọc SCC?
* **Định nghĩa toán học:** Trong đồ thị có hướng, một thành phần được gọi là liên thông mạnh nếu giữa hai đỉnh bất kỳ $u$ và $v$, luôn tồn tại cả đường đi từ $u \to v$ VÀ đường quay về từ $v \to u$.
* **Mối nguy hiểm nếu không lọc SCC:** Mạng đường OpenStreetMap chứa nhiều nhánh đường cụt một chiều (xe chỉ rẽ vào được mà không thể lùi hay quay đầu đi ra). Nếu một điểm thu gom bị snap vào nút ngõ cụt này, xe đi vào gom rác xong sẽ **không có đường quay về Depot** ($d(i, \text{Depot}) = \infty$). Giá trị $\infty$ này sẽ làm sập toàn bộ thuật toán SFO-VND!
* **Giải pháp của nhóm:** Bắt buộc snap 51 điểm vào 868 nút thuộc SCC lớn nhất. Cơ chế này loại bỏ $100\%$ rủi ro bị đứt đường, đảm bảo không có bất kỳ cặp điểm nào có khoảng cách vô cực.

#### ❓ Tại sao ma trận khoảng cách lại có tính chất bất đối xứng $d(A, B) \ne d(B, A)$?
* Chiều đi từ Depot $\to$ Điểm 1 là $1,649.4\text{ m}$, nhưng chiều về từ Điểm 1 $\to$ Depot chỉ có $1,587.1\text{ m}$ (chênh lệch $62.3\text{ m}$).
* Điều này phản ánh hoàn hảo thực tế giao thông: Xe đi qua các đoạn đường gom một chiều và các nút giao lệch pha, chứng minh nhóm tính toán trên đồ thị có hướng thật chứ không phải nhân đôi ma trận đối xứng.

#### ❓ Tại sao nếu mất kết nối, tuyệt đối KHÔNG ĐƯỢC điền số 0 vào ma trận?
* Nếu điền số 0, thuật toán sẽ hiểu lầm rằng khoảng cách giữa 2 điểm đó bằng 0 mét (tức là 2 điểm trùng nhau hoặc xe dịch chuyển tức thời không tốn xăng). Khi đó thuật toán sẽ liên tục chọn đi qua cung này, dẫn đến nghiệm "ảo" hoàn toàn sai lệch.

#### ❓ Tại sao phải lưu file `.graphml` vĩnh viễn mà không tải trực tiếp từ OSM mỗi lần chạy?
* **Bảo đảm tính tái lập (Reproducibility):** OpenStreetMap được cộng đồng cập nhật từng phút. Nếu mỗi lần chạy lại gọi API OSM, đồ thị có thể bị thay đổi số nút/số cạnh, làm sai lệch kết quả đối chứng. Lưu file `.graphml` giúp hệ thống chạy độc lập, offline, bảo đảm 10 năm sau chạy lại vẫn ra đúng 935 nút.

---

## 📚 3. CHUẨN HÓA 6 BỘ DỮ LIỆU BENCHMARK QUỐC TẾ CVRPLIB

### Những gì nhóm đã làm:
1. Tải và lưu trữ nguyên bản 6 file `.vrp` và `.sol` chuẩn quốc tế vào thư mục [data/benchmarks/raw/](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/benchmarks/raw/):
   * `E-n33-k4` (Christofides & Eilon, 1969 - BKS: 835)
   * `B-n50-k7` (Augerat et al., 1995 - BKS: 741)
   * `E-n51-k5` (Christofides & Eilon, 1969 - BKS: 521)
   * `A-n53-k7` (Augerat et al., 1995 - BKS: 1010)
   * `A-n60-k9` (Augerat et al., 1995 - BKS: 1354)
   * `E-n76-k7` (Christofides & Eilon, 1969 - BKS: 682)
2. Viết module đọc dữ liệu [src/core/cvrplib_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/core/cvrplib_loader.py) bằng thư viện chuyên dụng `vrplib`.
3. Cài đặt hàm `verify_solution_cost` kiểm chứng nghiệm chuẩn tham chiếu `.sol`.
4. Xuất bảng siêu dữ liệu tổng hợp: [results/benchmark_metadata.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/benchmark_metadata.csv).
5. Xây dựng 19 bài unit test tự động tại [tests/test_loader.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_loader.py) (đạt 19/19 passed).

---

### TẠI SAO LẠI LÀM NHƯ VẬY?

#### ❓ Tại sao nhóm làm case study Phường Tây Thạnh mà vẫn phải tải và đọc Benchmark CVRPLIB?
* **Thước đo học thuật chuẩn mực quốc tế:** Nếu nhóm chỉ thử nghiệm trên dữ liệu tự tạo tại Tây Thạnh, người chấm có thể hoài nghi: *"Biết đâu nhóm tự chọn dữ liệu dễ để thuật toán chạy tốt?"*.
* CVRPLIB là bộ chuẩn kinh điển thế giới (giống như tập MNIST trong Computer Vision). Nếu thuật toán của nhóm đọc chuẩn và đối chiếu được trên CVRPLIB, đó là minh chứng sắt đá rằng mã nguồn của nhóm tuân thủ tiêu chuẩn quốc tế, có thể so sánh công bằng với các bài báo khoa học trên toàn cầu.

#### ❓ Quy ước làm tròn số nguyên TSPLIB `EUC_2D` là gì và tại sao lại cực kỳ nguy hiểm nếu làm sai?
* **Quy ước TSPLIB:** Khoảng cách giữa 2 điểm $(x_i, y_i)$ và $(x_j, y_j)$ được làm tròn thành số nguyên tại **từng cạnh đơn lẻ** trước khi cộng dồn vào tổng chi phí:
  $$d(i, j) = \text{round}\left(\sqrt{(x_i - x_j)^2 + (y_i - y_j)^2}\right)$$
* **Bẫy lập trình kinh điển:** Nhiều sinh viên giữ số thực (float) cho từng cạnh, rồi đến bước cuối cùng mới làm tròn tổng quãng đường. Kết quả là tổng chi phí bị lệch $1 - 3$ đơn vị so với giá trị BKS (Best Known Solution). Điều này khiến bài báo cáo bị coi là tính toán sai! Nhóm đã bắt đúng quy tắc làm tròn nguyên của TSPLIB và khớp chính xác $100\%$ giá trị 835, 741, 521, 1010, 1354, 682.

#### ❓ Sự khác biệt giữa mục tiêu Benchmark CVRPLIB và mục tiêu Case Study Xanh là gì?
* **CVRPLIB:** Bài toán tĩnh kinh điển đơn mục tiêu: chỉ tìm tổng độ dài quãng đường ngắn nhất ($\min \sum d_{ij}$). Không có đường một chiều, không xét khối lượng rác biến thiên trên xe.
* **Case Study Xanh:** Bài toán đa mục tiêu thực tế: tối ưu hóa chi phí nhiên liệu và phát thải $\text{CO}_2$ theo tải trọng rác tích lũy động (mô hình MEET / ISO 14064) trên mạng đường có hướng thực tế.

---

## 🧩 4. XÂY DỰNG TOY INSTANCE 12 ĐIỂM & TÍNH TOÁN BẰNG TAY (HAND CALCULATION)

### Những gì nhóm đã làm:
1. Xây dựng instance nhân tạo nhỏ gồm **1 Depot (ID 0) và 12 điểm thu gom (ID 1 đến 12)**:
   * Cấu hình: $K = 3$ xe, tải trọng tối đa $Q = 200.0\text{ kg}$/xe (Tổng sức chứa = $600\text{ kg}$).
   * Tổng nhu cầu rác: $\sum q_i = 420.0\text{ kg} \le 600.0\text{ kg}$ (Mức dự phòng an toàn $30\%$).
   * Tọa độ 2D rõ ràng, sinh có kiểm soát với `seed = 42`.
2. **Tính toán thủ công từng bước bằng tay (Hand Calculation):**
   * **Xe 1:** $0 \to 1 \to 2 \to 3 \to 4 \to 0$ (Tải: $140\text{ kg} \le 200\text{ kg}$, Cự ly: $98.12\text{ m}$)
   * **Xe 2:** $0 \to 5 \to 6 \to 7 \to 8 \to 0$ (Tải: $135\text{ kg} \le 200\text{ kg}$, Cự ly: $102.32\text{ m}$)
   * **Xe 3:** $0 \to 9 \to 10 \to 11 \to 12 \to 0$ (Tải: $145\text{ kg} \le 200\text{ kg}$, Cự ly: $108.92\text{ m}$)
   * Tổng quãng đường cộng tay: **$309.36\text{ m}$**.
3. Lưu minh chứng: [toy_12_points.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_12_points.csv), [toy_feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_feasible_routes.json), ảnh vẽ trực quan [toy_hand_calculation.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/toy_hand_calculation.png).
4. Viết **8 ca unit test tự động bắt lỗi biên** tại [tests/test_toy_instance.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_toy_instance.py).

---

### TẠI SAO LẠI LÀM NHƯ VẬY?

#### ❓ Tại sao phải tạo bộ dữ liệu đồ chơi 12 điểm khi đã có dữ liệu 50 điểm của phường?
* **Mốc Chân Lý (Ground Truth) để gỡ lỗi (Debug):** Khi lập trình các thuật toán phức tạp như SFO và VND ở Step 3, nếu chạy ngay trên 50 điểm mà thuật toán báo lỗi hoặc ra nghiệm kỳ lạ, ta sẽ như "mò kim đáy bể", không biết lỗi do dữ liệu hay do thuật toán.
* Với bộ Toy 12 điểm, nhóm đã tính tay từng centimet và từng kilôgam. Khi đưa vào code, nếu code chạy ra đúng $309.36\text{ m}$ và 3 tuyến như tính tay $\implies$ chứng minh $100\%$ bộ giải mã Split và bộ tính toán Evaluator hoạt động hoàn hảo!

#### ❓ Tại sao phải viết unit test bắt 7 ca lỗi biên (Negative Testing)?
Nhóm đã chủ động viết các ca kiểm thử cố tình tạo ra dữ liệu sai:
1. `test_duplicate_point_id`: Cố tình trùng ID điểm $\to$ Hệ thống phải bắt lỗi ngay.
2. `test_negative_or_missing_demand`: Lượng rác bị âm $\to$ Ném lỗi lập tức.
3. `test_demand_exceeds_capacity`: Có điểm rác nặng $250\text{ kg} > Q=200\text{ kg}$ $\to$ Bắt lỗi bất khả thi (không xe nào gom nổi 1 mình).
4. `test_missing_depot`: Dữ liệu thiếu điểm xuất phát Depot 0 $\to$ Bắt lỗi.
5. `test_unreachable_node`: Cung về depot bằng $\infty$ $\to$ Bắt lỗi đứt đường.
6. `test_vehicles_exceed_fleet_size`: Dùng 4 xe $> K=3$ $\to$ Bắt lỗi vi phạm quy mô đội xe.
7. `test_duplicate_or_omitted_customer`: Tuyến bị sót khách hoặc phục vụ lặp lại $\to$ Bắt lỗi vi phạm ràng buộc phân hoạch.
> **Ý nghĩa:** Đây là tư duy **Lập trình Phòng thủ (Defensive Programming)**. Nó chứng minh phần mềm của nhóm không chỉ chạy được khi dữ liệu đẹp, mà còn cực kỳ kiên cố trước mọi sai sót dữ liệu thực tế!

---

## 🏢 5. THIẾT LẬP CẤU HÌNH CASE STUDY CẤP PHƯỜNG & CHỨNG MINH KHẢ THI (FEASIBLE WITNESS)

### Những gì nhóm đã làm:
1. Xây dựng bộ dữ liệu **51 điểm** (1 Trạm trung chuyển Depot + 50 điểm thu gom rác trên các trục đường Phường Tây Thạnh: Lê Trọng Tấn, Sơn Kỳ, Tân Kỳ Tân Quý, Bờ Bao Tân Thắng, Đỗ Nhuận).
2. Phân tầng nhu cầu rác thải thực tế (`seed = 42`):
   * 35 điểm dân cư: $35 - 75\text{ kg}$/điểm.
   * 15 điểm kinh doanh/thương mại (Aeon Mall, hàng quán): $75 - 120\text{ kg}$/điểm.
   * Tổng lượng rác toàn phường: **$3,345.0\text{ kg}$**.
3. Khóa kịch bản đội xe: **$K = 4$ xe chuyên dụng**, tải trọng thiết kế **$Q = 1,500\text{ kg}$/xe (1.5 tấn)**.
   * Tổng sức chứa đội xe: $4 \times 1,500 = 6,000.0\text{ kg}$.
   * Tỷ lệ tải toàn hệ thống: $3,345 / 6,000 = 55.75\%$ (Biên độ dự phòng an toàn $44.25\%$).
4. **Thiết lập và chứng minh tồn tại Nghiệm Khả thi (Feasible Witness):**
   * Lưu tại [data/ward/processed/feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/feasible_routes.json).
   * Phân chia hợp lệ thành 4 tuyến xe:
     * Xe 1: Gom 21 điểm (ID 1-21) — Tải $1,475.0\text{ kg} \le 1,500\text{ kg}$ (Cự ly: $20.886\text{ km}$)
     * Xe 2: Gom 23 điểm (ID 22-44) — Tải $1,475.0\text{ kg} \le 1,500\text{ kg}$ (Cự ly: $13.471\text{ km}$)
     * Xe 3: Gom 6 điểm (ID 45-50) — Tải $395.0\text{ kg} \le 1,500\text{ kg}$ (Cự ly: $7.969\text{ km}$)
     * Xe 4: Dự phòng đỉnh tải — Tải $0.0\text{ kg}$
   * Phục vụ đủ 50/50 điểm, không sót, không lặp, $100\%$ không xe nào vượt tải $Q$, tổng cự ly $42.326\text{ km}$.

---

### TẠI SAO LẠI LÀM NHƯ VẬY?

#### ❓ Tại sao lại chọn quy mô 50 điểm mà không phải 10 điểm hay 500 điểm?
* 10 điểm thì quá nhỏ, không phản ánh được tính phức tạp của một phường đô thị.
* 300–500 điểm là quy mô cấp quận, dữ liệu sẽ quá cồng kềnh cho giai đoạn Step 2 làm sạch dữ liệu.
* Quy mô **50 điểm** nằm chính xác trong khung khuyến nghị chuẩn $40 - 100$ điểm của GVHD. Nó đủ lớn để chứng minh tính NP-hard của bài toán, nhưng đủ tinh gọn để kiểm soát sạch $100\%$ ma trận khoảng cách và snap tọa độ.

#### ❓ Tại sao lại chọn xe tải trọng $Q = 1,500\text{ kg}$ (1.5 tấn)?
* **Quy chuẩn thực tế của ngành môi trường đô thị:** Theo quy định phân luồng giao thông của UBND TP.HCM, các dòng xe tải chở rác cỡ lớn (trên 5 tấn) bị cấm lưu thông vào các tuyến đường nội bộ đô thị ban ngày.
* Để thu gom rác trong các khu dân cư đông đúc như Tân Phú, Công ty TNHH MTV Môi trường Đô thị TP.HCM (CITENCO) sử dụng đội xe ép rác mini chuyên dụng có tải trọng từ $1.0 - 1.5$ tấn (như dòng xe Isuzu / Hino mini). Thông số $Q = 1,500\text{ kg}$ là con số bám sát $100\%$ thực tế vận hành!

#### ❓ "Feasible Witness" (Nghiệm chứng khả thi) là gì và tại sao bắt buộc phải có trước khi chạy SFO-VND?
* **Bản chất toán học:** Trong quy hoạch tối ưu, điều kiện cần $\sum q_i \le K \cdot Q$ ($3,345 \le 6,000$) chưa chắc đã đảm bảo bài toán có nghiệm (vì có thể do cách đóng gói bao bì mà không thể chia vào $K$ thùng).
* **Feasible Witness** là việc nhóm đưa ra được **ít nhất một phương án phân tuyến thực tế** thỏa mãn toàn bộ 4 ràng buộc cứng. Nó đóng vai trò là "chứng minh thư" xác nhận bài toán là **Giải được (Feasible)**. Nếu không có bước này, nhỡ dữ liệu bị lỗi bất khả thi mà mang đi nạp vào thuật toán SFO thì sẽ biến công sức ở Step 3 thành vô nghĩa!

---

## 🗂️ 6. PHÂN ĐỊNH RẠCH RÒI THƯ MỤC RAW / PROCESSED & TÍNH TÁI LẬP (REPRODUCIBILITY)

### Những gì nhóm đã làm:
1. Chuẩn hóa cấu trúc thư mục phân tách giữa dữ liệu thô gốc và dữ liệu xử lý:
   ```text
   data/
   ├── benchmarks/
   │   └── raw/               # 6 file .vrp và .sol nguyên bản
   ├── toy/                   # Instance 12 điểm
   └── ward/
       ├── raw/               # Ranh giới GIS gốc, file road_network.graphml
       └── processed/         # collection_points.csv, distance_matrix.csv, scenario.json
   ```
2. Soạn thảo Từ điển Dữ liệu chi tiết: [data_dictionary.md](../reports/data_dictionary.md) quy định rõ: tên trường, kiểu dữ liệu, đơn vị đo (mét, kg, Lít, VNĐ), nhãn phân loại dữ liệu (`điểm thu gom giả lập trên mạng đường OSM`).
3. Cố định `seed = 42` tại [data/ward/processed/scenario.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/scenario.json).
4. Khóa phiên bản thư viện chính xác trong [requirements.txt](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/requirements.txt): Python 3.13.14, `osmnx 2.1.1`, `vrplib 2.2.0`, `networkx 3.6.1`, `geopandas 1.2.0`, `pandas 2.2.3`, `numpy 2.2.3`, `pytest 9.0.3`.

---

### TẠI SAO LẠI LÀM NHƯ VẬY?

#### ❓ Tại sao phải chia tách thư mục `raw` và `processed`?
* **Nguyên tắc bất biến của Kỹ thuật Dữ liệu (Data Engineering):** Thư mục `raw` chứa dữ liệu gốc bất biến (Read-only). Tuyệt đối không được can thiệp sửa tay hay ghi đè vào thư mục này.
* Mọi thao tác làm sạch, gán nhãn, snap tọa độ đều được lưu vào `processed`. Nếu một ngày nào đó script xử lý gặp lỗi logic, ta chỉ việc xóa thư mục `processed` và chạy lại từ `raw`, không sợ mất dữ liệu gốc.

#### ❓ Tại sao phải có `data_dictionary.md` và gắn nhãn "giả lập trên mạng đường OSM"?
* **Minh bạch học thuật:** Nhóm không đi rải các thùng rác bằng nhựa ngoài đường thật để cân từng ký rác mỗi ngày. Tọa độ được trích xuất trên đường thật từ OSMnx, còn khối lượng rác được sinh theo phân tầng hộ dân cư và hàng quán. 
* Gắn nhãn minh bạch `điểm thu gom giả lập trên mạng đường OSM` giúp nhóm khẳng định sự trung thực khoa học, không nhận vơ dữ liệu giả lập là dữ liệu sensor thật.

#### ❓ Cố định `seed = 42` để làm gì?
* Các hàm ngẫu nhiên của máy tính (`random`, `numpy.random`) nếu không cố định hạt giống (seed) thì mỗi lần chạy sẽ sinh ra các giá trị tọa độ hoặc khối lượng rác khác nhau.
* Cố định `seed = 42` bảo đảm tính **Tái lập khoa học (Reproducibility)**: Bất kỳ ai, dù chạy trên máy Windows của bạn Quang hay máy Mac của bạn Hiền, đều sẽ sinh ra đúng $100\%$ bộ số 3,345.0 kg rác và các tọa độ tương ứng!

---

## ✅ 7. BỘ KIỂM ĐỊNH TỰ ĐỘNG (VALIDATION SUITE) 23 TIÊU CHÍ

### Những gì nhóm đã làm:
1. Xây dựng công cụ kiểm tra toàn diện độc lập: [tests/validate_dataset.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/validate_dataset.py).
2. Kiểm tra **23 tiêu chí kỹ thuật** chia làm 7 Suite:
   * **Suite 1:** Kiểm tra cấu trúc thư mục, tệp tin và từ điển dữ liệu.
   * **Suite 2:** Kiểm tra tính hợp lệ dữ liệu Benchmark CVRPLIB.
   * **Suite 3:** Kiểm tra tính hợp lệ và 8 ca biên của Toy Instance.
   * **Suite 4:** Kiểm tra tính toàn vẹn dữ liệu Case Study cấp phường.
   * **Suite 5:** Kiểm tra ma trận khoảng cách có hướng (đường chéo bằng 0, không có $\infty$).
   * **Suite 6:** Kiểm tra tính khả thi của kịch bản $K - Q - \text{Demand}$ và Feasible Witness.
   * **Suite 7:** Kiểm tra tính tái lập dữ liệu qua hạt giống (`seed = 42`).
3. Xuất báo cáo tự động: [results/logs/validation_report.log](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/logs/validation_report.log). Kết quả: **23/23 PASS (100%)**.
4. Chạy toàn bộ test suite Pytest: `py -m pytest` đạt **34/34 passed** trong $6.07$ giây.

---

### TẠI SAO LẠI LÀM NHƯ VẬY?

#### ❓ Tại sao không kiểm tra bằng mắt (manual) mà phải viết code kiểm định tự động?
* Dữ liệu ma trận có tới $51 \times 51 = 2,601$ ô số. Một con người không thể soi bằng mắt từng ô xem có ô nào bị âm hay vô cực hay không.
* Viết script tự động giúp việc kiểm định diễn ra trong 0.2 giây, hoàn toàn khách quan, không có sai sót chủ quan của con người, và xuất ra file log làm minh chứng nghiệm thu không thể chối cãi.

---

## 🔄 8. THEO DÕI VÀ XỬ LÝ 8 VẤN ĐỀ TỒN TẠI TỪ STEP 1 (R1 – R8)

### Bảng trạng thái xử lý chi tiết:

| Vấn đề | Tồn tại từ Step 1 | Quyết định xử lý trong Step 2 | Tại sao xử lý như vậy? |
| :---: | :--- | :--- | :--- |
| **R1** | Tên Phường Sơn Kỳ cũ có thể gây tranh cãi pháp lý. | **Đã khóa:** Chọn Phường Tây Thạnh (OSM `admin_level = 8`), buffer 400m. | Bảo đảm tính hợp pháp hành chính trên OpenStreetMap và tránh đứt đường vành đai. |
| **R2** | Nguy cơ tổng lượng rác vượt tải trọng đội xe. | **Đã khóa:** Khóa $K=4$, $Q=1500$ kg, $\sum q = 3345$ kg $\le 6000$ kg. Có Feasible Witness. | Bảo đảm điều kiện cần và đủ để bài toán chắc chắn có nghiệm giải được. |
| **R3** | Lẫn lộn giữa dữ liệu thực địa và dữ liệu mô phỏng. | **Đã khóa:** Lập `data_dictionary.md`, gắn nhãn minh bạch `giả lập trên mạng đường OSM`. | Giữ vững tính trung thực học thuật, không ngụy tạo kết quả sensor thật. |
| **R4** | Sai số do dùng đường chim bay hoặc đứt đường 1 chiều. | **Đã khóa:** Dijkstra có hướng trên SCC 868 nút ô tô, $d(A, B) \ne d(B, A)$, 0 cặp $\infty$. | Phản ánh đúng đường một chiều và dải phân cách đô thị, triệt tiêu ngõ cụt. |
| **R5** | Sai lệch giá trị tham chiếu BKS do làm tròn sai. | **Đã khóa:** Dùng `vrplib`, làm tròn nguyên từng cạnh TSPLIB `EUC_2D`, khớp 100% 6 BKS. | Tuân thủ đúng chuẩn mực quốc tế CVRPLIB để có thể đăng bài báo khoa học. |
| **R6** | Hàm chi phí–$\text{CO}_2$ MEET/ISO 14064 chưa cố định công thức. | **Chuyển sang Step 3:** Đã liệt kê định mức tại `config.py`, sẽ khóa công thức ở Step 3. | Tuân thủ đúng phân kỳ Step 2: "Chưa cần cài thuật toán hay hàm mục tiêu phức tạp". |
| **R7** | Cơ chế Split Decoder và VND cập nhật ngược về SFO. | **Chuyển sang Step 3 & 6:** Đã thiết kế kiến trúc Re-encoding, cài đặt ở Step 3. | Tách bạch giữa pha chuẩn bị dữ liệu (Step 2) và pha hiện thực thuật toán (Step 3). |
| **R8** | Kịch bản 300–400 điểm, What-if và bản đồ tương tác. | **Chuyển sang Step 4, 6 & 8:** Tập trung làm sạch và kiểm định vững chắc 50 điểm trước. | Tránh dàn trải nguồn lực, bảo đảm nền móng vững chắc trước khi mở rộng quy mô. |

---

# PHẦN II: Ý TƯỞNG BÁO CÁO

Khi báo cáo Step 2, trình bày gãy gọn theo cấu trúc 5 bước sau:

### 🎤 Bước 1: Tuyên bố Mục tiêu & Triết lý của Step 2 (1 phút)
> *"Kính thưa Thầy hướng dẫn và các bạn! Hôm nay nhóm xin báo cáo kết quả nghiệm thu **Step 2: Chuẩn bị và Khóa Bộ Dữ liệu**. 
> Với triết lý 'Garbage In, Garbage Out', nhóm xác định dữ liệu là nền móng cốt lõi quyết định sự thành bại của giải thuật tối ưu SFO-VND. Vì vậy trong Step 2, nhóm tập trung toàn lực để làm sạch, chuẩn hóa và kiểm định dữ liệu, bảo đảm tính liên thông giao thông đô thị $100\%$ và tính khả thi toán học trước khi bước vào cài đặt giải thuật ở Step 3."*

### 🎤 Bước 2: Dữ liệu Benchmark CVRPLIB chuẩn quốc tế (1.5 phút)
> *"Thứ nhất, về dữ liệu đối chuẩn quốc tế: Nhóm đã nạp thành công **6 bộ dữ liệu CVRPLIB kinh điển** (`E-n33-k4`, `B-n50-k7`, `E-n51-k5`, `A-n53-k7`, `A-n60-k9`, `E-n76-k7`).
> Điểm mấu chốt là nhóm đã xử lý chuẩn xác quy tắc làm tròn số nguyên `EUC_2D` tại từng cạnh theo chuẩn TSPLIB, giúp kết quả kiểm chứng nghiệm tham chiếu khớp hoàn toàn $100\%$ với giá trị BKS công bố quốc tế. Bộ dữ liệu này đã vượt qua 19/19 bài unit test tự động."*

### 🎤 Bước 3: Instance nhỏ 12 điểm & Minh chứng tính tay (1.5 phút)
> *"Thứ hai, để phục vụ việc kiểm thử và debug giải thuật ở Step 3, nhóm đã thiết lập một instance nhỏ gồm **1 Depot và 12 điểm thu gom** với đội xe $K=3, Q=200\text{ kg}$. 
> Nhóm đã tự tay tính toán thủ công từng chặng, chứng minh tồn tại phương án phân tuyến 3 xe chở $420\text{ kg}$ rác với tổng chiều dài $309.36\text{ m}$. Đồng thời, nhóm xây dựng 8 ca kiểm thử biên (Negative Testing) để chứng minh hệ thống có khả năng phòng thủ vững chắc trước các lỗi: trùng ID, thiếu depot, rác âm hoặc điểm vượt tải trọng."*

### 🎤 Bước 4: Case Study Phường Tây Thạnh & Mạng đường có hướng SCC (2 phút)
> *"Thứ ba, về Case Study thực tế:
> - Nhóm đã giải quyết triệt để vấn đề lịch sử của địa danh Sơn Kỳ cũ bằng việc lựa chọn **Phường Tây Thạnh, Quận Tân Phú** có ranh giới GIS pháp lý chính thức từ OpenStreetMap, kết hợp vùng đệm **Buffer 400m** để giữ trọn các nút giao quay đầu. Trạm trung chuyển Depot được đặt hợp pháp tại Khu công nghiệp Tân Bình.
> - Đặc biệt, nhóm tuyệt đối không dùng đường chim bay. Nhóm trích xuất đồ thị xe ô tô từ OSMnx và lọc ra **Thành phần Liên thông Mạnh (SCC) gồm 868 nút**. Snap toàn bộ 51 điểm vào SCC này bảo đảm $100\%$ các điểm đều có đường đi đến và đường quay về Depot an toàn, không có ngõ cụt. Ma trận khoảng cách $51 \times 51$ tính bằng Dijkstra phản ánh chính xác tính chất bất đối xứng của đường một chiều.
> - Kịch bản đội xe gồm $K=4$ xe ép rác 1.5 tấn, phục vụ 50 điểm thu gom với tổng lượng rác $3,345\text{ kg}$. Nhóm đã thiết lập thành công **Feasible Witness** (Bằng chứng phân tuyến khả thi), chứng minh bài toán cấp phường hoàn toàn giải được."*

### 🎤 Bước 5: Kết luận & Đề xuất chuyển giao Step 3 (1 phút)
> *"Toàn bộ dữ liệu của nhóm đã vượt qua **23/23 tiêu chí kiểm định** tự động tại `validate_dataset.py` và **34/34 bài unit test Pytest**, cố định `seed = 42` bảo đảm khả năng tái lập độc lập.
> Nhóm đã xử lý dứt điểm các vấn đề R1–R5 từ Step 1 và phân loại chuyển giao R6–R8 sang các bước tiếp theo. Nhóm kính đề xuất Thầy nghiệm thu Step 2 để nhóm chính thức bước sang Step 3 cài đặt thuật toán SFO-VND ạ!"*

---

# PHẦN III: BỘ CÂU HỎI VẶN VẸO CỦA THẦY / HỘI ĐỒNG VỀ STEP 2 & CÁCH ĐÁP TRẢ

### ❓ Câu 1: Tại sao trong báo cáo nói đề tài là Sơn Kỳ mà trong dữ liệu Step 2 lại làm ở Phường Tây Thạnh?
* **Trả lời sắc bén:**
  > *"Dạ thưa Thầy, sau các đợt sắp xếp địa giới hành chính, Phường Sơn Kỳ cũ hiện nay đã được chia tách và sáp nhập vào các phường lân cận như Tây Thạnh, Bình Hưng Hòa và Tân Sơn Nhì. Trên hệ thống cơ sở dữ liệu GIS chuẩn OpenStreetMap hiện nay không còn ranh giới hành chính pháp lý cấp 8 độc lập cho Sơn Kỳ cũ.  
  > Để bảo đảm tính pháp lý và tính chuẩn xác của dữ liệu, nhóm chọn Phường Tây Thạnh – nơi có ranh giới GeoJSON chính thức, đồng thời kế thừa trực tiếp dữ liệu khảo sát thực địa các tuyến đường chính từ Step 1 (như trục Lê Trọng Tấn, Sơn Kỳ). Đây là biện pháp xử lý chuẩn mực nhằm bảo đảm tính khoa học của đề tài ạ."*

### ❓ Câu 2: Làm sao nhóm chứng minh được ma trận khoảng cách không bị đứt đường hoặc có điểm bị cô lập trong ngõ hẻm một chiều?
* **Trả lời sắc bén:**
  > *"Dạ thưa Thầy, nhóm đã sử dụng thuật toán lý thuyết đồ thị để trích xuất **Thành phần Liên thông Mạnh lớn nhất (Strongly Connected Component - SCC)** gồm 868 nút ô tô từ đồ thị OSMnx.  
  > Theo định nghĩa toán học, trong một SCC, mọi cặp đỉnh đều có đường đi 2 chiều nối với nhau. Nhóm bắt buộc toàn bộ 51 điểm thu gom phải snap vào các nút thuộc SCC này. Do đó, ma trận khoảng cách $51 \times 51$ tính bằng Dijkstra có đúng $0$ cặp điểm bị vô cực ($\infty$), đường chéo bằng $0$ và $100\%$ các điểm đều liên thông 2 chiều với Depot ạ."*

### ❓ Câu 3: Tại sao nhóm không cài đặt luôn thuật toán SFO ở Step 2 cho nhanh, phân chia các Step làm gì cho rườm rà?
* **Trả lời sắc bén:**
  > *"Dạ thưa Thầy, việc phân chia rạch ròi giữa Step 2 (Dữ liệu) và Step 3 (Giải thuật) là tuân thủ nghiêm ngặt quy trình nghiên cứu khoa học chuẩn mực.  
  > Nếu vội vàng cài SFO khi dữ liệu chưa được kiểm định, nhỡ thuật toán không hội tụ ta sẽ không thể biết được nguyên nhân do tham số SFO sai hay do ma trận khoảng cách bị đứt gãy. Việc hoàn thành Step 2 giúp nhóm đóng băng một bộ dữ liệu sạch $100\%$ và có Feasible Witness làm mốc chân lý. Khi sang Step 3, nhóm chỉ cần tập trung duy nhất vào việc tối ưu thuật toán mà không bao giờ phải lo lắng về lỗi dữ liệu nữa ạ."*

### ❓ Câu 4: Quy ước làm tròn TSPLIB EUC_2D trong CVRPLIB có ý nghĩa gì mà nhóm lại nhấn mạnh trong báo cáo?
* **Trả lời sắc bén:**
  > *"Dạ thưa Thầy, trong thư viện CVRPLIB quốc tế, khoảng cách giữa 2 điểm được tính theo tọa độ Euclid 2D nhưng phải **làm tròn thành số nguyên ngay tại từng cạnh** trước khi cộng dồn vào chu trình tuyến xe.  
  > Nếu người lập trình để kiểu số thực float cộng dồn cả tuyến rồi mới làm tròn số cuối cùng, sai số làm tròn tích lũy sẽ làm tổng chi phí bị lệch $1 - 3$ đơn vị so với kỷ lục thế giới BKS. Nhóm đã nhận diện được bẫy kỹ thuật này, viết hàm làm tròn đúng chuẩn TSPLIB và kiểm chứng khớp chính xác $100\%$ cả 6 bộ benchmark ạ."*

### ❓ Câu 5: Dữ liệu lượng rác tại 50 điểm của phường là dữ liệu nhóm tự bịa ra hay lấy ở đâu?
* **Trả lời sắc bén:**
  > *"Dạ thưa Thầy, nhóm xin trả lời rất thẳng thắn và minh bạch: Tọa độ 50 điểm là tọa độ thực tế được trích xuất dọc theo các trục đường giao thông của Phường Tây Thạnh từ OpenStreetMap. Còn khối lượng rác là dữ liệu **mô phỏng có kiểm soát (Controlled Simulation)** được cố định bởi `seed = 42`.  
  > Nhóm không tự bịa ngẫu nhiên mà phân tầng giả lập theo định mức phát sinh rác thải đô thị thực tế tại TP.HCM: điểm dân cư từ $35 - 75\text{ kg}$/ngày và điểm kinh doanh/hàng quán từ $75 - 120\text{ kg}$/ngày. Toàn bộ định nghĩa này được nhóm công bố minh bạch trong Từ điển Dữ liệu `data_dictionary.md` và gắn nhãn rõ ràng là 'điểm thu gom giả lập trên mạng đường OSM' chứ không nhận vơ là số đo từ cảm biến thật ạ."*

---

> 💡 **THÔNG ĐIỆP CỐT LÕI ĐỂ BẢO VỆ THÀNH CÔNG STEP 2:**  
> Hãy luôn khẳng định với Thầy rằng: **Dữ liệu của Step 2 đã được khóa cứng, đạt 100% kiểm định tự động, có bằng chứng khả thi Feasible Witness và ma trận đường bộ có hướng thực tế không có giá trị ảo.** Nhóm đã hoàn thành xuất sắc nhiệm vụ của Step 2 và hoàn toàn tự tin tiến vào Step 3!

