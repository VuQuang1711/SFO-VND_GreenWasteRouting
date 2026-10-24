# 📖 TỪ ĐIỂN DỮ LIỆU DỰ ÁN (DATA DICTIONARY)

> **Đề tài:** Tối ưu hóa lộ trình thu gom rác đô thị bằng thuật toán lai SFO-VND  
> **Phiên bản:** v1.0 (Khóa dữ liệu Step 2)  
> **Ngày ban hành:** 2026-10-24  
> **Thành viên phụ trách:** Vũ Thế Quang (Khóa schema & Kịch bản K-Q-demand)

---

## 📌 1. Nguyên tắc phân loại nguồn gốc dữ liệu (Data Provenance)

Tuân thủ nghiêm ngặt yêu cầu của Hướng dẫn Step 2 (Vấn đề R3):
1. **Không lập lờ giữa dữ liệu thực tế và mô phỏng:** Các điểm thu gom rác do nhóm xây dựng trên mạng đường được gắn nhãn minh bạch là `điểm thu gom giả lập trên mạng đường OSM`, tuyệt đối không ghi nhận là "vị trí thùng rác thực tế của chính quyền".
2. **Nguồn gốc mạng lưới:** Trích xuất từ cơ sở dữ liệu mở **OpenStreetMap (OSM)** thông qua thư viện `OSMnx`, tuân thủ giấy phép dữ liệu mở ODbL (Open Database License).
3. **Đơn vị đo lường chuẩn hóa thống nhất:**
   * **Khối lượng rác / Tải trọng xe:** Kilôgam ($\text{kg}$).
   * **Khoảng cách ma trận / Khoảng cách snap:** Mét ($\text{m}$) (được quy đổi ra kilômét $\text{km}$ khi nạp vào bộ giải thuật tính phát thải).
   * **Thời gian phục vụ:** Phút ($\text{phút}$).

---

## 🗂️ 2. Chi tiết cấu trúc dữ liệu Case Study Cấp Phường

### 2.1. Tệp `collection_points.csv`
* **Vị trí lưu trữ:** `data/ward/processed/collection_points.csv`
* **Mô tả:** Danh sách trạm tập kết Depot (ID 0) và 50 điểm thu gom rác thải.

| Tên trường (Column) | Kiểu dữ liệu | Đơn vị | Ràng buộc | Nguồn gốc | Ý nghĩa & Quy tắc sinh |
| :--- | :---: | :---: | :---: | :--- | :--- |
| `point_id` | `int64` | - | Khóa chính, duy nhất, từ 0 đến 50 | Tự gán | ID 0 quy ước là Depot; ID 1..50 là các điểm thu gom rác. |
| `name` | `string` | - | Không rỗng | Khảo sát / Địa chỉ | Tên gợi nhớ hoặc số nhà trục đường thực tế. |
| `latitude` | `float64` | Độ thập phân | $10.800 \le \text{lat} \le 10.830$ | OSMnx / GPS | Tọa độ vĩ độ chuẩn WGS84 (EPSG:4326). |
| `longitude` | `float64` | Độ thập phân | $106.600 \le \text{lon} \le 106.640$ | OSMnx / GPS | Tọa độ kinh độ chuẩn WGS84 (EPSG:4326). |
| `demand_kg` | `float64` | kg | $\ge 0.0$ và $\le 1500.0$ | Mô phỏng có kiểm soát | Khối lượng rác phát sinh. Điểm dân cư: 35–75 kg; Điểm kinh doanh: 75–120 kg. Depot = 0.0 kg. |
| `point_type` | `string` | - | `depot`, `residential`, `commercial` | Phân tầng giả định | Phân loại loại hình điểm gom (1 Depot, 35 Dân cư, 15 Kinh doanh). |
| `source_type` | `string` | - | Không rỗng | Quy chuẩn Step 2 | Ghi rõ bản chất: `trạm trung chuyển chất thải quy hoạch` hoặc `điểm thu gom giả lập trên mạng đường OSM`. |
| `snapped_node` | `int64` | - | Nút thuộc SCC của đồ thị | OSMnx snap | ID nút giao thông gần nhất trên mạng đường xe ô tô. |
| `snap_distance_m`| `float64` | m | $\ge 0.0$, thường $\le 50.0\text{m}$ | Thuật toán snap | Khoảng cách từ tọa độ điểm đến nút đường gần nhất. |

---

### 2.2. Tệp `depot.csv`
* **Vị trí lưu trữ:** `data/ward/processed/depot.csv`
* **Mô tả:** Thông số kỹ thuật của Trạm trung chuyển / Bãi xuất phát và tiếp nhận xe rác.

| Tên trường | Kiểu dữ liệu | Đơn vị | Giá trị thực tế | Ý nghĩa |
| :--- | :---: | :---: | :--- | :--- |
| `depot_id` | `int64` | - | `0` | Mã quy ước của Depot trong toàn bộ giải thuật. |
| `name` | `string` | - | Trạm trung chuyển chất thải Tây Thạnh | Trạm trung chuyển khu công nghiệp Tân Bình - Tây Thạnh. |
| `latitude` | `float64` | Độ | `10.8122` | Vĩ độ trạm trung chuyển. |
| `longitude` | `float64` | Độ | `106.6215` | Kinh độ trạm trung chuyển. |
| `source_type` | `string` | - | trạm trung chuyển chất thải quy hoạch | Điểm tập kết hợp pháp theo quy hoạch địa phương. |
| `snapped_node` | `int64` | - | `4225472861` | Nút mạng đường giao thông tiếp cận trực tiếp cổng bãi. |
| `snap_distance_m`| `float64`| m | `20.2` | Khoảng cách đấu nối từ trạm vào tim đường trục chính. |

---

### 2.3. Tệp `vehicles.csv`
* **Vị trí lưu trữ:** `data/ward/processed/vehicles.csv`
* **Mô tả:** Đội xe thu gom chuyên dụng phục vụ địa bàn trong ca làm việc.

| Tên trường | Kiểu dữ liệu | Đơn vị | Giá trị | Ý nghĩa |
| :--- | :---: | :---: | :--- | :--- |
| `vehicle_id` | `string` | - | `XE_01` đến `XE_04` | Mã định danh xe thu gom ($K = 4$ xe). |
| `capacity_kg` | `float64` | kg | `1500.0` | Tải trọng tối đa cho phép của thùng ép rác ($Q = 1.5$ tấn). |
| `available` | `bool` | - | `True` | Trạng thái sẵn sàng vận hành trong ca gom. |

---

### 2.4. Tệp `distance_matrix.csv`
* **Vị trí lưu trữ:** `data/ward/processed/distance_matrix.csv`
* **Mô tả:** Ma trận khoảng cách mạng đường bộ có hướng kích thước $51 \times 51$.
* **Đơn vị:** Mét ($\text{m}$).
* **Đặc tính kỹ thuật:**
  * Tính toán bằng thuật toán tìm đường ngắn nhất **Dijkstra** có trọng số theo thuộc tính chiều dài cung đường `length` từ đồ thị OSMnx có hướng (`DiGraph`).
  * Đường chéo $D[i, i] = 0.0$ với mọi $i$.
  * Bất đối xứng $D[i, j] \ne D[j, i]$ phản ánh chính xác hệ thống đường một chiều, phân làn và cấm rẽ.
  * $100\%$ các điểm đều có đường đi từ Depot và quay về Depot ($D[0, i] < \infty$ và $D[i, 0] < \infty$). Không tự ý thay giá trị khuyết bằng 0.

---

### 2.5. Tệp `scenario.json`
* **Vị trí lưu trữ:** `data/ward/processed/scenario.json`
* **Mô tả:** Metadata tổng hợp định hình kịch bản thực nghiệm Step 2.

```json
{
  "ward_name": "Phường Tây Thạnh, Quận Tân Phú, Thành phố Hồ Chí Minh",
  "admin_source": "OpenStreetMap_Nominatim_Overpass_API_admin_level_8",
  "seed": 42,
  "demand_rule": "Phân tầng 2 nhóm: 35 điểm dân cư (35-75 kg, seed 42) + 15 điểm kinh doanh/thương mại (75-120 kg, seed 42)",
  "K": 4,
  "Q": 1500.0,
  "units": {
    "demand": "kg",
    "distance": "meters",
    "fleet_size": "vehicles"
  },
  "road_network_source": "OpenStreetMap_network_type_drive_buffer_400m",
  "created_at": "2026-10-24T10:41:00+07:00",
  "total_demand_kg": 3329.0,
  "total_customers": 50,
  "depot_id": 0
}
```

---

### 2.6. Tệp `feasible_routes.json`
* **Vị trí lưu trữ:** `data/ward/processed/feasible_routes.json`
* **Mô tả:** Bằng chứng tồn tại phương án phân tuyến hợp lệ (Feasible Witness) cho Case Study 50 điểm.
* **Cấu trúc trường:**
  * `vehicle_id`: Mã xe (`XE_01` .. `XE_04`).
  * `customer_ids`: Danh sách thứ tự các điểm khách gom rác trên tuyến.
  * `full_path`: Lộ trình khép kín bắt đầu và kết thúc tại Depot: `[0, ..., 0]`.
  * `route_load_kg`: Tổng khối lượng gom trên tuyến ($\le 1500.0$ kg).
  * `route_distance_km`: Chiều dài tuyến đường bộ thực tế (km).
  * `validation_status`: Trạng thái kiểm định (`PASS`).

---

## 🧸 3. Chi tiết cấu trúc dữ liệu Toy Instance (12 Điểm)

* **Mục đích:** Kiểm thử giải thuật, gỡ lỗi biên và minh chứng tính toán bằng tay (Mục 11-13).
* **Vị trí lưu trữ:** Thư mục `data/toy/`
  1. [toy_12_points.csv](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_12_points.csv): Tọa độ $(x, y)$, tên điểm, demand (kg).
  2. [toy_instance.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_instance.json): Toàn bộ thông số $K=3, Q=200\text{kg}$, ma trận khoảng cách $13 \times 13$, seed 42.
  3. [toy_feasible_routes.json](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/data/toy/toy_feasible_routes.json): Phương án phân tuyến minh chứng với tổng quãng đường 309.36m.
