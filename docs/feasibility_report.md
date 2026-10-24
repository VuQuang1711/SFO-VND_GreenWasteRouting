# 📋 BÁO CÁO TÍNH KHẢ THI & THEO DÕI CÁC VẤN ĐỀ TỒN TẠI (FEASIBILITY REPORT)

> **Đề tài:** Tối ưu hóa lộ trình thu gom rác đô thị bằng thuật toán lai SFO-VND  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu  
> **Thành viên phụ trách:** Vũ Thế Quang (Nhóm trưởng - Khóa schema & Validator), Lê Nguyễn Tâm Đức (Mạng đường), Nguyễn Ngọc Thảo Hiền (Benchmark CVRPLIB)

---

## 📌 1. Bảng theo dõi xử lý các vấn đề Step 1 tồn tại (R1 – R8)

Tuân thủ hướng dẫn nghiệm thu nội bộ Step 2, nhóm tổng hợp trạng thái xử lý chi tiết của 8 vấn đề trọng tâm như sau:

| Mã vấn đề | Nội dung tồn tại từ Step 1 | Giải pháp & Kết quả đã thực hiện trong Step 2 | Trạng thái nghiệm thu | Mốc chốt tiếp theo |
| :---: | :--- | :--- | :---: | :---: |
| **R1** | **Sơn Kỳ là địa danh cũ**<br>Nguy cơ sai lệch địa bàn hành chính sau sáp nhập. | • Xác định địa bàn Sơn Kỳ cũ được phân bổ vào Bình Hưng Hòa, Tây Thạnh, Tân Sơn Nhì.<br>• Chọn **Phường Tây Thạnh (Quận Tân Phú)** làm địa bàn chính thức có đối chiếu ranh giới GIS chuẩn WGS84 EPSG:4326 từ OpenStreetMap.<br>• Thiết lập vùng đệm 400m kết nối mạng đường.<br>• Xuất file [ward_selection.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/ward_selection.md), [ward_boundary.geojson](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/raw/ward_boundary.geojson). | **ĐÃ HOÀN TẤT (PASS)** | Khóa tại Step 2 |
| **R2** | **Dữ liệu rác có thể vượt tải**<br>Nguy cơ không tồn tại phương án phân tuyến khả thi. | • Phân tầng 50 điểm gom ($Q = 1500$ kg, $K = 4$ xe, Tổng sức chứa = 6000 kg).<br>• Tổng demand = 3329.0 kg $\le 6000$ kg (Điều kiện cần đạt).<br>• Tạo và kiểm chứng phương án phân tuyến hợp lệ (**Feasible Witness**), lưu minh chứng tại [feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/feasible_routes.json) (Xe 1: 757kg, Xe 2: 700kg, Xe 3: 752kg, Xe 4: 1120kg). | **ĐÃ HOÀN TẤT (PASS)** | Khóa tại Step 2 |
| **R3** | **Thực tế / OSM / mô phỏng chưa tách sạch**<br>Lẫn lộn dữ liệu khảo sát và giả lập. | • Xây dựng Từ điển dữ liệu chuẩn [data_dictionary.md](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/data_dictionary.md).<br>• Gắn nhãn phân loại minh bạch: `điểm thu gom giả lập trên mạng đường OSM` (không gọi là thùng rác thực tế).<br>• Ghi rõ thời điểm lấy (2026-10-24), đơn vị đo (kg, mét, phút) và quy tắc sinh. | **ĐÃ HOÀN TẤT (PASS)** | Khóa tại Step 2 |
| **R4** | **Distance matrix, đường một chiều**<br>Sai số do dùng khoảng cách chim bay hoặc đứt đường. | • Tuyệt đối không dùng khoảng cách Euclid/chim bay thay đường bộ.<br>• Tính Dijkstra có hướng trên thành phần liên thông mạnh SCC (868 nút) của đồ thị ô tô OSMnx.<br>• Bảo đảm $100\%$ các điểm đều có đường đi từ/về Depot, $D[i,i] = 0.0$, ma trận bất đối xứng phản ánh đường 1 chiều.<br>• Đối chiếu thủ công 3 cặp điểm và 1 vòng khép kín. | **ĐÃ HOÀN TẤT (PASS)** | Khóa tại Step 2 |
| **R5** | **Benchmark/BKS sai quy ước**<br>Quy ước làm tròn và số khách hàng chưa chuẩn. | • Sử dụng thư viện chuẩn `vrplib.read_instance` đọc file `.vrp` gốc.<br>• Phân biệt rõ số nút $N$ (gồm cả depot) và số khách $N-1$.<br>• Quy ước làm tròn nguyên EUC_2D theo chuẩn TSPLIB/CVRPLIB.<br>• Đã kiểm chứng 6 bộ dữ liệu: `E-n33-k4`, `B-n50-k7`, `E-n51-k5`, `A-n53-k7`, `A-n60-k9`, `E-n76-k7`. | **ĐÃ HOÀN TẤT (PASS)** | Khóa tại Step 2 |
| **R6** | **Hàm cost–CO₂, MEET/ISO 14064 chưa khóa**<br>Tự ý đặt hệ số phát thải mà không có cơ sở. | • Liệt kê các thông số định mức trong [config.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/config.py): trọng lượng rỗng xe (2500 kg), định mức dầu rỗng (0.12 L/km), hệ số tải (0.00004 L/km/kg), hệ số phát thải dầu diesel (2.68 kg CO₂/L theo ISO 14064).<br>• Phân biệt rõ đây là công thức ước tính lý thuyết, chưa phải số đo sensor thực tế. | **GHI NHẬN ĐẦY ĐỦ** | **Chính thức khóa ở Step 3** |
| **R7** | **Greedy Split hay Split tối ưu, VND cập nhật ngược**<br>Cơ chế giải mã và cập nhật nghiệm ưu tú. | • Đã phân tích câu hỏi thiết kế: Split động xét tải trọng rác tích lũy và cập nhật nghiệm tinh hoa từ VND về quần thể SFO.<br>• Chưa ghép thuật toán SFO-VND tại bước này theo đúng yêu cầu "Chưa cần cài SFO hay VND". | **CHUYỂN GIAO THIẾT KẾ** | **Thực hiện ở Step 3 & 6** |
| **R8** | **Quy mô 300–400 điểm, What-if, Attack Power/VND elite**<br>Quy mô quá lớn gây bất ổn định dữ liệu. | • Tạm để ngoài phạm vi Step 2 để tập trung làm sạch và khóa bộ dữ liệu nhỏ (12 điểm toy) và vừa (50 điểm cấp phường).<br>• Bảo đảm tính ổn định và tính khả thi tuyệt đối của dữ liệu nền tảng. | **TẠM ĐỂ NGOÀI PHẠM VI** | **Thực hiện ở Step 4, 6 & 8** |

---

## 🧮 2. Minh chứng tính toán bằng tay (Toy Instance 12 Điểm)

Nhóm xây dựng một instance nhân tạo có quy mô nhỏ gồm **1 Depot (ID 0) và 12 Điểm thu gom (ID 1 đến 12)** với cấu hình:
* Đội xe: $K = 3$ xe; Tải trọng tối đa: $Q = 200.0$ kg/xe.
* Tổng sức chứa đội xe: $3 \times 200 = 600.0$ kg.
* Danh sách nhu cầu (Demand kg):
  $$[30, 45, 25, 40, 35, 50, 20, 30, 25, 45, 40, 35]$$
* Tổng nhu cầu rác thải toàn hệ thống:
  $$\sum q_i = 30 + 45 + 25 + 40 + 35 + 50 + 20 + 30 + 25 + 45 + 40 + 35 = 420.0\text{ kg} \le 600.0\text{ kg}$$

### Bảng chi tiết tính toán thủ công từng tuyến xe (Feasible Witness):

| Xe phục vụ | Thứ tự di chuyển (Cycle) | Tải trọng từng điểm (kg) | Tổng tải tuyến (kg) | Ràng buộc tải ($Q \le 200$) | Chi tiết khoảng cách từng chặng (m) | Quãng đường tuyến (m) |
| :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **XE_01** | $0 \to 1 \to 2 \to 3 \to 4 \to 0$ | $30 + 45 + 25 + 40$ | **140.0 kg** | **ĐẠT (PASS)** | $0\to 1 (22.36) + 1\to 2 (14.14) + 2\to 3 (10.00) + 3\to 4 (20.00) + 4\to 0 (31.62)$ | **98.12 m** |
| **XE_02** | $0 \to 5 \to 6 \to 7 \to 8 \to 0$ | $35 + 50 + 20 + 30$ | **135.0 kg** | **ĐẠT (PASS)** | $0\to 5 (28.28) + 5\to 6 (14.14) + 6\to 7 (14.14) + 7\to 8 (14.14) + 8\to 0 (31.62)$ | **102.32 m** |
| **XE_03** | $0 \to 9 \to 10 \to 11 \to 12 \to 0$ | $25 + 45 + 40 + 35$ | **145.0 kg** | **ĐẠT (PASS)** | $0\to 9 (22.36) + 9\to 10 (14.14) + 10\to 11 (30.00) + 11\to 12 (14.14) + 12\to 0 (28.28)$ | **108.92 m** |
| **TỔNG CỘNG** | **3 xe (K=3)** | **12 khách hàng** | **420.0 kg** | **HỢP LỆ TOÀN DIỆN** | **Tổng chi phí quãng đường toàn mạng:** | **309.36 m** |

> **Minh chứng đồ họa:** Xem hình ảnh biểu diễn lộ trình và vị trí các điểm tại [toy_hand_calculation.png](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/toy_hand_calculation.png).  
> **Kiểm thử tự động:** Vượt qua 100% 8 ca kiểm thử biên tại [test_toy_instance.py](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_toy_instance.py).

---

## 🔍 3. Đối chiếu khoảng cách thủ công trên Case Study Phường Tây Thạnh

Tuân thủ mục 22 của Hướng dẫn Step 2, nhóm kiểm tra đối chiếu trực tiếp trên ma trận khoảng cách có hướng `data/ward/processed/distance_matrix.csv`:

### 3.1. Đối chiếu 3 cặp điểm hai chiều (Tính chất bất đối xứng đường 1 chiều):
1. **Cặp Depot (0) $\leftrightarrow$ Điểm 1:**
   * Chiều đi $d(0, 1) = 1,649.4\text{ m}$
   * Chiều về $d(1, 0) = 1,587.1\text{ m}$
   * Độ chênh lệch: $\Delta = |1649.4 - 1587.1| = 62.3\text{ m}$ (do các đoạn đường gom một chiều tại trục Lê Trọng Tấn).
2. **Cặp Điểm 1 $\leftrightarrow$ Điểm 15:**
   * Chiều đi $d(1, 15) = 634.7\text{ m}$
   * Chiều về $d(15, 1) = 625.7\text{ m}$
   * Độ chênh lệch: $\Delta = 9.0\text{ m}$.
3. **Cặp Điểm 15 $\leftrightarrow$ Điểm 30:**
   * Chiều đi $d(15, 30) = 1,261.7\text{ m}$
   * Chiều về $d(30, 15) = 1,004.4\text{ m}$
   * Độ chênh lệch: $\Delta = 257.3\text{ m}$ (khu vực có dải phân cách cứng yêu cầu xe phải đi vòng qua giao lộ quay đầu).

### 3.2. Đối chiếu 1 vòng khép kín Depot – A – B – Depot:
Xét vòng di chuyển: $\text{Depot (0)} \to \text{Điểm 1 (A)} \to \text{Điểm 2 (B)} \to \text{Depot (0)}$:
* Chặng 1: $\text{Depot (0)} \to \text{Điểm 1}: d(0, 1) = 1,649.4\text{ m}$
* Chặng 2: $\text{Điểm 1} \to \text{Điểm 2}: d(1, 2) = 100.9\text{ m}$
* Chặng 3: $\text{Điểm 2} \to \text{Depot (0)}: d(2, 0) = 1,486.1\text{ m}$
* **Tổng độ dài vòng khép kín:**
  $$D_{\text{cycle}} = 1649.4 + 100.9 + 1486.1 = 3,236.4\text{ m} = 3.236\text{ km}$$
* Kết luận: Các cung đường đều liên tục, khớp hoàn toàn với dữ liệu Dijkstra trên đồ thị và không có giá trị khuyết bị thay bằng 0.

---

## 🏆 4. Kết luận về tính khả thi của bộ dữ liệu

1. **Bộ dữ liệu CVRPLIB:** Đọc chuẩn xác 6 bộ dữ liệu chính thức, đúng số khách, tải trọng, quy tắc làm tròn nguyên EUC_2D.
2. **Bộ dữ liệu Toy Instance (12 điểm):** Đạt 100% tính khả thi, giải quyết triệt để các trường hợp kiểm thử biên.
3. **Bộ dữ liệu Case Study Phường Tây Thạnh (50 điểm):** Mạng đường liên thông mạnh 100%, có bằng chứng phân tuyến khả thi với 4 xe tải trọng 1500 kg, số liệu minh bạch, sẵn sàng nghiệm thu chuyển sang **Step 3**.
