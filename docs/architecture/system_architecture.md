# 🏛️ KIẾN TRÚC HỆ THỐNG VÀ THIẾT KẾ THUẬT TOÁN LAI SFO-VND
## System Architecture & Algorithm Design Specification

> **Đơn vị đào tạo:** Trường Đại học Công Thương Thành phố Hồ Chí Minh (HUIT)  
> **Khoa/Ngành:** Ngành Khoa học Dữ liệu  
> **Đề tài NCKH:** Tối ưu hóa lộ trình thu gom rác thải đô thị nhằm giảm chi phí và phát thải carbon bằng thuật toán Sailfish Optimizer lai Variable Neighborhood Descent (SFO-VND)  
> **Giai đoạn:** Chuẩn hóa kiến trúc & Chuyển giao từ Step 2 sang Step 3  
> **Nhóm thực hiện:** Vũ Thế Quang (Nhóm trưởng), Lê Nguyễn Tâm Đức, Nguyễn Ngọc Thảo Hiền  

---

## 📌 1. TỔNG QUAN KIẾN TRÚC PHÂN TẦNG (TIERED ARCHITECTURE)

Hệ thống được thiết kế theo mô hình phân tầng chặt chẽ (Separation of Concerns), bảo đảm tính module hóa cao, tính tái lập độc lập và khả năng mở rộng trong tương lai:

```mermaid
flowchart TD
    subgraph DataTier["1. TẦNG DỮ LIỆU (DATA LAYER)"]
        D1["CVRPLIB Raw Benchmark (.vrp, .sol)"]
        D2["Toy Instance 12 điểm (Hand-calculated)"]
        D3["OSM GIS Boundary & Network (.graphml)"]
        D4["50 Điểm Thu Gom & Ma trận Dijkstra (51x51)"]
    end

    subgraph CoreTier["2. TẦNG XỬ LÝ LÕI (CORE & DEFENSE LAYER)"]
        C1["cvrplib_loader.py (Đọc chuẩn TSPLIB)"]
        C2["data_loader.py (Đọc phòng thủ & kiểm tra)"]
        C3["decoder.py (Random-Key + Dynamic Split)"]
        C4["evaluator.py (Khoảng cách + MEET/ISO 14064 CO2)"]
        C5["validator.py (Kiểm định 4 ràng buộc cứng CVRP)"]
    end

    subgraph AlgoTier["3. TẦNG THUẬT TOÁN TỐI ƯU (ALGORITHM LAYER)"]
        A1["sfo.py (Sailfish Optimizer - Khám phá liên tục)"]
        A2["vnd.py (Variable Neighborhood Descent: 2-opt, Relocate, Swap)"]
        A3["hybrid_sfo_vnd.py (Thuật toán lai SFO-VND hợp nhất)"]
        A4["baselines/ (Greedy Nearest Neighbor & Genetic Algorithm GA)"]
    end

    subgraph PresentationTier["4. TẦNG TRỰC QUAN HÓA & GIAO DIỆN (PRESENTATION & WEB)"]
        P1["extract_map.py & route_mapper.py (Ánh xạ Folium)"]
        P2["web/app.py (Flask Web Application)"]
        P3["Dashboard Before/After & Convergence Curve"]
    end

    DataTier --> CoreTier
    CoreTier --> AlgoTier
    AlgoTier --> PresentationTier
```

---

## 🔄 2. QUY TRÌNH LUỒNG DỮ LIỆU & TỐI ƯU HÓA (DATA FLOW PIPELINE)

Quy trình giải quyết bài toán Green Capacitated Vehicle Routing Problem (GCVRP) từ dữ liệu GIS đến nghiệm tối ưu diễn ra theo các bước tuần tự:

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng / Hội đồng
    participant Map as GIS & Dijkstra Engine
    participant SFO as SFO Population (Liên tục)
    participant Decoder as Random-Key + Split Decoder
    participant VND as VND Local Search
    participant Eval as Evaluator (Cost & CO2)
    participant UI as Web Dashboard

    User->>Map: Nạp ranh giới WGS84 & Đồ thị OSMnx (SCC 868 nút)
    Map-->>Decoder: Cung cấp Ma trận khoảng cách có hướng 51x51 m
    SFO->>SFO: Khởi tạo bầy cá cờ & cá mòi trong [0, 1]^N (seed=42)
    loop Quá trình tiến hóa từng thế hệ (t = 1 .. T_max)
        SFO->>Decoder: Chuyển vector thực continuous sang thứ tự khách hàng
        Decoder->>Eval: Phân đoạn tuyến thỏa mãn tải trọng Q_max và hạm đội K
        Eval-->>SFO: Trả về giá trị Fitness (Chi phí xăng dầu + CO2 + Phạt)
        Note over SFO,VND: Chọn lọc nghiệm tinh hoa (Elite Sailfish)
        SFO->>VND: Kích hoạt VND cải tiến cục bộ nghiệm ưu tú
        VND->>VND: Quét tuần tự: N_1 (2-opt) -> N_2 (Relocate) -> N_3 (Swap)
        VND-->>SFO: Cập nhật ngược nghiệm cải tiến vào bầy Sailfish
    end
    SFO->>UI: Xuất giải pháp tối ưu (Tuyến đường, Cự ly, Nhiên liệu, CO2)
    UI->>User: Hiển thị trực quan bản đồ Leaflet & so sánh Before/After
```

---

## 📐 3. MÔ HÌNH TOÁN HỌC GCVRP VÀ HÀM MỤC TIÊU XANH

### 3.1. Các biến quyết định và ràng buộc
Cho đồ thị có hướng $G = (V, A)$ với $V = \{0, 1, \dots, n\}$ (trong đó $0$ là Depot, $V_c = \{1, \dots, n\}$ là các điểm thu gom rác).
* Biến nhị phân $x_{ijk} \in \{0, 1\}$: nhận giá trị $1$ nếu xe $k$ di chuyển trực tiếp từ điểm $i$ đến điểm $j$, ngược lại nhận $0$.
* Biến phụ tải $u_{ik} \ge 0$: khối lượng rác tích lũy trên xe $k$ sau khi rời điểm $i$.

**Các ràng buộc cốt lõi:**
1. **Phủ đủ khách hàng:** Mỗi điểm thu gom được thăm chính xác 1 lần:
   $$\sum_{k=1}^K \sum_{j \in V, j \neq i} x_{ijk} = 1, \quad \forall i \in V_c$$
2. **Bảo toàn luồng tại trạm Depot:** Mỗi xe rời depot và phải quay về depot:
   $$\sum_{j \in V_c} x_{0jk} = \sum_{i \in V_c} x_{i0k} \le 1, \quad \forall k \in \{1, \dots, K\}$$
3. **Giới hạn tải trọng phương tiện:** Khối lượng rác trên từng tuyến không vượt quá sức chứa cho phép $Q$:
   $$\sum_{i \in V_c} q_i \left( \sum_{j \in V, j \neq i} x_{ijk} \right) \le Q, \quad \forall k \in \{1, \dots, K\}$$
4. **Loại bỏ chu trình con (Sub-tour Elimination):**
   $$u_{ik} - u_{jk} + Q \cdot x_{ijk} \le Q - q_j, \quad \forall i, j \in V_c, i \neq j, \forall k$$

### 3.2. Mô hình tính toán năng lượng & phát thải $\text{CO}_2$ (MEET / ISO 14064)(Test)
Khác với CVRP truyền thống chỉ tối thiểu hóa cự ly, mô hình **GCVRP** tính đến tải trọng thực tế thay đổi trên từng chặng di chuyển:
* Tổng trọng lượng xe tại chặng $(i, j)$: $W_{ij} = W_{\text{empty}} + L_{ij}$, trong đó $W_{\text{empty}} = 2,500\text{ kg}$, $L_{ij}$ là lượng rác đang chở.
* Suất tiêu hao nhiên liệu trên chặng $(i, j)$:
  $$\text{rate}_{ij} = \alpha_0 + \alpha_1 \cdot W_{ij} \quad (\text{Lít/km})$$
  với $\alpha_0 = 0.12\text{ L/km}$ (định mức chạy không tải), $\alpha_1 = 0.00004\text{ L/km/kg}$ (hệ số tiêu hao theo tải).
* Nhiên liệu tiêu thụ: $\text{Fuel}_{ij} = d_{ij} \cdot \text{rate}_{ij}$.
* Lượng phát thải $\text{CO}_2$: $E_{\text{CO}_2, ij} = \text{Fuel}_{ij} \times 2.68\text{ kg CO}_2\text{/Lít}$.

---

## 🎯 4. LỘ TRÌNH TRIỂN KHAI STEP 3 (STEP 3 ROADMAP)

Sau khi bộ dữ liệu Step 2 đã được khóa hoàn toàn (Locked & Validated), các hạng mục kỹ thuật trong Step 3 bao gồm:

| STT | Nhiệm vụ kỹ thuật Step 3 | File phụ trách | Tiêu chí nghiệm thu |
| :---: | :--- | :--- | :--- |
| **3.1** | **Hiệu chỉnh siêu tham số SFO** | `src/algorithms/sfo.py` | Khảo sát $N_p \in [30, 80]$, $T_{\max} \in [100, 500]$, tỉ lệ cá cờ/cá mòi $PP$. Vẽ biểu đồ hội tụ. |
| **3.2** | **Thử nghiệm cấu trúc lân cận VND** | `src/algorithms/vnd.py` | Đánh giá thứ tự lân cận: $2\text{-opt} \to \text{Relocate} \to \text{Swap}$ so với đảo thứ tự. Ghi nhận thời gian và biên độ cải thiện. |
| **3.3** | **Thực nghiệm 6 bộ Benchmark CVRPLIB** | `src/algorithms/hybrid_sfo_vnd.py` | So sánh nghiệm tìm được với BKS (Best Known Solutions). Đạt Gap $\le 3.5\%$ trên các bộ chuẩn. |
| **3.4** | **Thực nghiệm Case Study Tây Thạnh 50 điểm** | `main.py`, `results/` | Đối chứng hiệu quả giải thuật: SFO-VND vs. Greedy Baseline vs. Genetic Algorithm (GA). |
| **3.5** | **Hoàn thiện Giao diện Web tương tác** | `web/app.py`, `web/templates/` | Hiển thị bản đồ phân tuyến đa màu, bảng thống kê Before/After và biểu đồ hội tụ trực tiếp trên trình duyệt. |
