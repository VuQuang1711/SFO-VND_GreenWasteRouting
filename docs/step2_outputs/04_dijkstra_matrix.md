# 🛣️ KẾT QUẢ 4: MA TRẬN KHOẢNG CÁCH CÓ HƯỚNG DIJKSTRA & PHÂN TÍCH CHUYÊN SÂU

> **Đơn vị:** Trường Đại học Công Thương Thành phố Hồ Chí Minh (HUIT)  
> **Đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu  
> **Thành viên phụ trách chính:** Lê Nguyễn Tâm Đức *(Mạng đường & Ma trận Dijkstra)*, Vũ Thế Quang *(Kiểm thử tính liên thông)*  
> **Tài liệu tham chiếu:** *STEP2_Huong_dan_chi_tiet_SFO_VND_Green_Waste_Routing.pdf (Mục 2.6 & 3)*

---

## 📌 1. BẢNG TỔNG HỢP KẾT QUẢ ĐẦU RA MA TRẬN KHOẢNG CÁCH

Nhóm đã tính toán ma trận cự ly đường bộ thực tế quy mô **$51 \times 51$ (1 Depot + 50 điểm thu gom)** bằng thuật toán tìm đường ngắn nhất **Dijkstra** trên đồ thị có hướng của thành phần liên thông mạnh (SCC) 868 nút, lưu tại [`data/ward/processed/distance_matrix.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/distance_matrix.csv).

| Tiêu chí kiểm định ma trận | Quy định của GVHD | Kết quả thực tế của nhóm | Đánh giá |
| :--- | :--- | :--- | :---: |
| **Kích thước ma trận** | Đúng số điểm $(N \times N)$ | **$51 \times 51$** (Hàng 0..50, Cột 0..50) | **PASS** |
| **Đơn vị đo lường** | Mét (m), không nhầm lẫn km | **Mét (m)**, độ chính xác 1 chữ số thập phân | **PASS** |
| **Giá trị đường chéo $d(i,i)$** | $d(i,i) = 0.0$ với mọi $i$ | $\max(d(i,i)) = \mathbf{0.0\text{ m}}$ | **PASS** |
| **Cặp không có đường đi ($\infty$)** | Báo cáo rõ, không gán 0 | **0 cặp bị vô cực** (100% các cặp đều có đường đi) | **PASS** |
| **Tính liên thông với Depot** | $d(0, i) < \infty$ và $d(i, 0) < \infty$ | **100%** điểm đều đi được từ Depot và quay về được Depot | **PASS** |
| **Tính chất có hướng (Bất đối xứng)** | Phản ánh đường 1 chiều | $d(i, j) \ne d(j, i)$ tại các cung đường có dải phân cách / 1 chiều | **PASS** |

---

### 1.1. Bảng đối chiếu thủ công 3 cặp điểm hai chiều (Kiểm tra tính bất đối xứng)

| Cặp điểm kiểm tra | Chiều đi $d(A \to B)$ (m) | Chiều về $d(B \to A)$ (m) | Độ chênh lệch $\Delta$ (m) | Nguyên nhân thực tế trên mạng đường OSM |
| :--- | :---: | :---: | :---: | :--- |
| **Depot (0) $\leftrightarrow$ Điểm 1** | $d(0, 1) = \mathbf{1,487.6}$ | $d(1, 0) = \mathbf{1,360.5}$ | **127.1 m** | Các đoạn rẽ nhánh một chiều và phân luồng tại nút giao Tây Thạnh – Lê Trọng Tấn. |
| **Điểm 1 $\leftrightarrow$ Điểm 15** | $d(1, 15) = \mathbf{1,384.6}$ | $d(15, 1) = \mathbf{1,603.1}$ | **218.5 m** | Dải phân cách cứng trên trục Tây Thạnh buộc xe chiều về phải đi qua giao lộ tiếp theo để quay đầu. |
| **Điểm 15 $\leftrightarrow$ Điểm 30** | $d(15, 30) = \mathbf{701.6}$ | $d(30, 15) = \mathbf{2,116.2}$ | **1,414.6 m** | Khu vực có đường gom một chiều, xe phải đi vòng qua trục Nguyễn Hữu Dật để chuyển hướng. |

---

### 1.2. Minh chứng đối chiếu thủ công 1 vòng chu trình khép kín (Depot $\to$ A $\to$ B $\to$ Depot)

Xét chu trình khép kín gồm Depot (0) và 2 điểm lân cận Điểm 1 và Điểm 2:
$$\text{Depot (0)} \longrightarrow \text{Điểm 1} \longrightarrow \text{Điểm 2} \longrightarrow \text{Depot (0)}$$

* **Chặng 1 ($0 \to 1$):** Tra ma trận dòng 0 cột 1: $d(0, 1) = 1,487.6\text{ m}$.
* **Chặng 2 ($1 \to 2$):** Tra ma trận dòng 1 cột 2: $d(1, 2) = 256.9\text{ m}$.
* **Chặng 3 ($2 \to 0$):** Tra ma trận dòng 2 cột 0: $d(2, 0) = 1,120.1\text{ m}$.
* **Tổng chiều dài chu trình tính bằng tay:**
  $$D_{\text{cycle}} = 1,487.6 + 256.9 + 1,120.1 = \mathbf{2,864.6\text{ m}} = \mathbf{2.865\text{ km}}$$
* **Đối chiếu với kết quả chương trình (Script):** Script chạy Dijkstra độc lập ra chính xác **2,864.6 m** $\implies$ **Khớp 100.0%, độ lệch bằng 0.0 m**.

---

## 🧠 2. PHÂN TÍCH CHUYÊN SÂU: TẠI SAO LẠI THỰC HIỆN NHƯ VẬY?

### 2.1. Tại sao TUYỆT ĐỐI CẤM sử dụng khoảng cách chim bay (Euclidean Distance)?
* Trong bài toán lý thuyết thuần túy, người ta có thể nối thẳng hai điểm bằng đường chim bay $\sqrt{(x_1-x_2)^2 + (y_1-y_2)^2}$. Nhưng trên thực tế đô thị TP.HCM:
  - Giữa hai điểm có thể có con kênh (Kênh 19/5), bức tường nhà xưởng KCN Tân Bình hoặc các dãy nhà phố ngăn cách.
  - Khoảng cách chim bay chỉ 100m nhưng xe ô tô tải có thể phải đi vòng qua cầu hoặc giao lộ mất hơn 1.5 km.
* Nếu dùng khoảng cách chim bay, lộ trình tính ra sẽ "chạy xuyên qua nhà dân và lòng sông", khiến kết quả nghiên cứu hoàn toàn vô giá trị trong thực tiễn vận hành xe rác.

### 2.2. Tại sao ma trận đường bộ bắt buộc phải là MA TRẬN BẤT ĐỐI XỨNG ($d_{ij} \ne d_{ji}$)?
* Giao thông đô thị hiện đại có rất nhiều tuyến đường một chiều, dải phân cách bê tông cứng ở giữa đường và các biển báo cấm rẽ trái:
  - Khi xe đi từ A đến B, xe đi theo chiều thuận mất 500m.
  - Khi xe muốn quay ngược từ B về A, xe không được phép đi lùi hay rẽ ngược chiều mà phải chạy tiếp đến điểm mở dải phân cách cách đó 700m để vòng đầu xe lại, khiến quãng đường về lên tới 1,900m.
* Việc xây dựng ma trận có hướng dựa trên đồ thị `DiGraph` của OSMnx phản ánh trung thực bản chất vật lý của mạng giao thông đô thị, giúp giải thuật tìm ra lộ trình thực tế xe có thể lăn bánh hợp pháp.

### 2.3. Tại sao TUYỆT ĐỐI KHÔNG ĐƯỢC tự ý điền giá trị 0 khi gặp đoạn đứt đường?
Căn cứ chỉ dẫn tại Mục 21 Hướng dẫn Step 2:
> *"Nếu có cặp không có đường đi, ghi thiếu/không kết nối và nêu cách xử lý; chỉ phần tử đường chéo d(i,i) bằng 0. Không tự đổi thành 0."*

* **Nguy cơ tiềm ẩn:** Nếu một cặp điểm $(u, v)$ bị đứt đường (vô cực $\infty$) mà lập trình viên tự tiện gán bằng 0.0:
  - Thuật toán tối ưu (SFO-VND) sẽ xem chi phí giữa $u$ và $v$ là miễn phí ($0$ đồng, $0$ km).
  - Thuật toán sẽ ngay lập tức "nhảy cóc" từ $u$ sang $v$ (hiện tượng Teleportation), tạo ra một nghiệm giả cực kỳ ngắn trên giấy tờ nhưng không thể di chuyển được ngoài đời.
* **Giải pháp khoa học của nhóm:** Thay vì điền 0, nhóm trích xuất **Thành phần liên thông mạnh lớn nhất (Strongly Connected Component - SCC gồm 868 nút)**. Trong SCC, lý thuyết đồ thị bảo đảm mọi nút đều có đường đi đến mọi nút khác. Nhờ vậy, ma trận đạt $100\%$ liên thông tự nhiên mà không cần bất kỳ sự can thiệp giả tạo nào!

---

## 📁 3. MINH CHỨNG VÀ LIÊN KẾT TỆP LIÊN QUAN

1. Ma trận cự ly CSV: [`data/ward/processed/distance_matrix.csv`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/ward/processed/distance_matrix.csv)
2. Script trích xuất và tính toán: [`src/map/extract_map.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/map/extract_map.py) & [`src/map/generate_tay_thanh_dataset.py`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/src/map/generate_tay_thanh_dataset.py)
3. Bản đồ mạng đường tương tác HTML: [`results/view_road_network.html`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/view_road_network.html)
4. Bản đồ hành trình tối ưu HTML: [`results/green_waste_routing_map.html`](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/results/green_waste_routing_map.html)

