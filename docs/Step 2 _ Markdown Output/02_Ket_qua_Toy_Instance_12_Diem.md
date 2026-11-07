# KẾT QUẢ 2: TOY INSTANCE 12 ĐIỂM TÍNH TAY & PHÂN TÍCH CHUYÊN SÂU

> **Đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu  
> **Thành viên phụ trách chính:** Vũ Thế Quang *(Nhóm trưởng - Thuật toán & Kiểm thử)*  
> **Tài liệu tham chiếu:** *STEP2_Huong_dan_chi_tiet_SFO_VND_Green_Waste_Routing.pdf (Mục 2.4 & 3)*

---

## 📌 1. BẢNG TỔNG HỢP KẾT QUẢ ĐẦU RA TOY INSTANCE

Nhóm đã xây dựng độc lập một bộ dữ liệu nhỏ có kiểm soát gồm **1 Trạm trung chuyển Depot (ID 0) và 12 Điểm gom rác (ID 1 đến 12)** với cấu hình tham số:
* Đội xe: $K = 3$ xe; Tải trọng tối đa: $Q = 200.0\text{ kg}$/xe.
* Tổng sức chứa toàn đội xe: $K \times Q = 3 \times 200 = 600.0\text{ kg}$.
* Nhu cầu từng điểm (kg): $[30, 45, 25, 40, 35, 50, 20, 30, 25, 45, 40, 35]$.
* Tổng nhu cầu rác phát sinh: $\sum q_i = 420.0\text{ kg} \le 600.0\text{ kg}$ *(Đạt điều kiện cần, tỷ lệ lấp đầy lý thuyết 70.0%, hệ số an toàn dự phòng 30.0%)*.

### 1.1. Bảng tọa độ và lượng rác chi tiết ([`data/toy/toy_12_points.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_12_points.csv))

| point_id | Tên điểm | Tọa độ $x$ (m) | Tọa độ $y$ (m) | Lượng rác $q_i$ (kg) | Vai trò nút |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **0** | Trạm tập kết trung chuyển (Depot) | 0.0 | 0.0 | 0.0 | `depot` |
| **1** | Điểm thu gom rác số 1 | 10.0 | 20.0 | 30.0 | `customer` |
| **2** | Điểm thu gom rác số 2 | 20.0 | 30.0 | 45.0 | `customer` |
| **3** | Điểm thu gom rác số 3 | 30.0 | 30.0 | 25.0 | `customer` |
| **4** | Điểm thu gom rác số 4 | 30.0 | 10.0 | 40.0 | `customer` |
| **5** | Điểm thu gom rác số 5 | -20.0 | 20.0 | 35.0 | `customer` |
| **6** | Điểm thu gom rác số 6 | -30.0 | 30.0 | 50.0 | `customer` |
| **7** | Điểm thu gom rác số 7 | -40.0 | 20.0 | 20.0 | `customer` |
| **8** | Điểm thu gom rác số 8 | -30.0 | 0.0 | 30.0 | `customer` |
| **9** | Điểm thu gom rác số 9 | 10.0 | -20.0 | 25.0 | `customer` |
| **10** | Điểm thu gom rác số 10 | 20.0 | -30.0 | 45.0 | `customer` |
| **11** | Điểm thu gom rác số 11 | -10.0 | -30.0 | 40.0 | `customer` |
| **12** | Điểm thu gom rác số 12 | -20.0 | -20.0 | 35.0 | `customer` |

---

### 1.2. Minh chứng tính toán thủ công từng tuyến (Feasible Witness)

Nhóm đã tính toán chi tiết bằng tay từng cạnh và từng tuyến xe, lưu kết quả tại [`data/toy/toy_feasible_routes.json`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_feasible_routes.json):

| Xe phục vụ | Hành trình chu trình ($0 \to \dots \to 0$) | Khối lượng gom từng điểm (kg) | Tổng tải gom tuyến (kg) | Ràng buộc tải ($Q \le 200$) | Chi tiết khoảng cách từng chặng Euclid (m) | Chiều dài tuyến (m) |
| :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **XE 1** | $0 \to 1 \to 2 \to 3 \to 4 \to 0$ | $30 + 45 + 25 + 40$ | **140.0 kg** | **PASS** *(70.0%)* | $0\to 1 (22.36) + 1\to 2 (14.14) + 2\to 3 (10.00) + 3\to 4 (20.00) + 4\to 0 (31.62)$ | **98.12 m** |
| **XE 2** | $0 \to 5 \to 6 \to 7 \to 8 \to 0$ | $35 + 50 + 20 + 30$ | **135.0 kg** | **PASS** *(67.5%)* | $0\to 5 (28.28) + 5\to 6 (14.14) + 6\to 7 (14.14) + 7\to 8 (14.14) + 8\to 0 (31.62)$ | **102.32 m** |
| **XE 3** | $0 \to 9 \to 10 \to 11 \to 12 \to 0$ | $25 + 45 + 40 + 35$ | **145.0 kg** | **PASS** *(72.5%)* | $0\to 9 (22.36) + 9\to 10 (14.14) + 10\to 11 (30.00) + 11\to 12 (14.14) + 12\to 0 (28.28)$ | **108.92 m** |
| **TỔNG** | **3 xe (K=3)** | **12/12 khách hàng** | **420.0 kg** | **HỢP LỆ TUYỆT ĐỐI** | **Tổng chiều dài toàn bộ hành trình:** | **309.36 m** |

> 📷 **Minh chứng đồ họa:** Xem sơ đồ lộ trình tính toán bằng tay tại [`results/figures/toy_hand_calculation.png`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/toy_hand_calculation.png).

---

## 🧠 2. PHÂN TÍCH CHUYÊN SÂU: TẠI SAO LẠI THỰC HIỆN NHƯ VẬY?

### 2.1. Tại sao GVHD bắt buộc phải có Toy Instance trước khi làm Case Study lớn?
1. **Kiểm soát tuyệt đối độ chính xác (Ground Truth):** Trên một bài toán 50 hay 300 điểm với hàng nghìn cung đường, mắt thường và máy tính không thể nhẩm nhanh được từng chặng. Với Toy Instance 12 điểm, nhóm sinh viên có thể dùng bút chì và máy tính cầm tay (Casio) cộng từng con số, đảm bảo không có bất kỳ "ảo giác" hay lỗi tiềm ẩn nào trong logic tính toán khoảng cách và tích lũy tải trọng.
2. **"Tấm khiên chắn lỗi" cho Step 3:** Khi chuyển sang Step 3 để cài đặt thuật toán tối ưu lai SFO-VND và bộ giải mã Split, Toy Instance chính là bộ test đầu tiên để xác minh xem thuật toán có tìm ra được nghiệm tối ưu $\le 309.36$ m hay không. Nếu thuật toán không giải nổi bài toán 12 điểm này thì chắc chắn không thể chạy trên bài toán cấp phường.

### 2.2. Tại sao "Tổng Demand $\le K \times Q$" chỉ là ĐIỀU KIỆN CẦN chứ CHƯA ĐỦ?
Đây là một định lý nền tảng trong lý thuyết tối ưu tổ hợp (Bin Packing Problem & CVRP):
* Giả sử ta có $K = 2$ xe, sức chứa $Q = 100$ kg/xe (Tổng sức chứa = 200 kg).
* Ta có 3 khách hàng với nhu cầu: $q_1 = 60\text{ kg}$, $q_2 = 60\text{ kg}$, $q_3 = 60\text{ kg}$.
* Tổng nhu cầu: $\sum q_i = 180\text{ kg} \le 200\text{ kg}$ *(Thỏa mãn điều kiện cần!)*.
* **Nhưng bài toán KHÔNG THỂ CÓ NGHIỆM KHẢ THI:** Bởi vì mỗi xe chỉ chở được tối đa 100 kg, nên mỗi xe chỉ có thể chở duy nhất 1 khách hàng (60 kg). Để chở hết 3 khách hàng, bắt buộc phải cần ít nhất 3 xe. Với đội xe chỉ có 2 xe ($K=2$), bài toán bị **vô nghiệm (Infeasible)**!
* Vì lý do này, GVHD yêu cầu nhóm phải cung cấp **Bằng chứng phân tuyến khả thi (Feasible Witness)** — tức là chỉ rõ từng xe chở cụ thể những điểm nào, để chứng minh bài toán chắc chắn giải được trên thực tế.

### 2.3. Tại sao phải thiết lập 8 ca kiểm thử biên (Edge-case testing)?
Trong [`tests/test_toy_instance.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_toy_instance.py), nhóm chủ động xây dựng 7 bài kiểm tra tự động để cố tình "bẫy lỗi":
1. `test_duplicate_point_id`: Phát hiện trùng mã định danh khách hàng.
2. `test_negative_or_missing_demand`: Bắt lỗi khối lượng rác âm hoặc bị khuyết thiếu (NaN).
3. `test_demand_exceeds_capacity`: Bắt lỗi điểm có $q_i > Q$ (rác tại 1 điểm vượt quá sức chứa nguyên 1 xe).
4. `test_missing_depot`: Bắt lỗi thiếu trạm tập kết Depot ID 0.
5. `test_unreachable_node`: Bắt lỗi đồ thị bị đứt đường không thể quay về Depot ($d(i, 0) = \infty$).
6. `test_vehicles_exceed_fleet_size`: Bắt lỗi thuật toán kích hoạt số xe vượt quá quy định ($K > 3$).
7. `test_duplicate_or_omitted_customer`: Bắt lỗi xe phục vụ lặp 1 điểm nhiều lần hoặc bỏ sót điểm thu gom rác.
* Nhờ có 8 ca test này, mã nguồn nạp dữ liệu trở nên "phòng thủ vững chắc" (Defensive Programming), không bao giờ bị sập nguồn khi gặp dữ liệu nhiễu ngoài thực tế.

---

## 📁 3. MINH CHỨNG VÀ LIÊN KẾT TỆP LIÊN QUAN

1. Dữ liệu CSV: [`data/toy/toy_12_points.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_12_points.csv)
2. Cấu hình JSON: [`data/toy/toy_instance.json`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_instance.json)
3. Minh chứng tuyến hợp lệ: [`data/toy/toy_feasible_routes.json`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_feasible_routes.json)
4. Bộ kiểm thử tự động: [`tests/test_toy_instance.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/tests/test_toy_instance.py) *(8/8 tests PASS)*
5. Ảnh sơ đồ tính tay: [`results/figures/toy_hand_calculation.png`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/figures/toy_hand_calculation.png)
