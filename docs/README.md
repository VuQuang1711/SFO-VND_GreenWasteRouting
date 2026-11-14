# 📚 HỆ THỐNG TÀI LIỆU DỰ ÁN (MASTER DOCUMENTATION PORTAL)
## Green Waste Route: Urban Waste Collection Routing Optimization Using Hybrid SFO-VND

> **Đơn vị:** Trường Đại học Công Thương Thành phố Hồ Chí Minh (HUIT)  
> **Khoa/Ngành:** Ngành Khoa học Dữ liệu  
> **Chương trình:** Nghiên cứu Khoa học Sinh viên — Khóa 15  
> **Đề tài:** Tối ưu hóa lộ trình thu gom rác thải đô thị nhằm giảm chi phí và phát thải carbon bằng thuật toán Sailfish Optimizer lai Variable Neighborhood Descent (SFO-VND)  
> **Thành viên nghiên cứu:**  
> 1. **Vũ Thế Quang** *(Nhóm trưởng — Khóa schema, Kịch bản K-Q-demand, Validator & Feasible Witness)*  
> 2. **Lê Nguyễn Tâm Đức** *(Phụ trách GIS, Mạng đường OSMnx & Ma trận khoảng cách Dijkstra)*  
> 3. **Nguyễn Ngọc Thảo Hiền** *(Phụ trách Thu thập & Kiểm định Benchmark quốc tế CVRPLIB)*  

---

## 🧭 1. CẤU TRÚC THƯ MỤC TÀI LIỆU CHUẨN HÓA

Thư mục `docs/` được chuẩn hóa toàn diện theo các nguyên tắc kỹ thuật phần mềm và nghiên cứu khoa học: phân định rành mạch các nhóm tài liệu, loại bỏ tệp tin trùng lặp, chuẩn hóa định dạng tên theo snake_case và thiết lập liên kết tương đối đồng bộ:

```text
docs/
├── README.md                      # Cổng điều hướng trung tâm của toàn bộ tài liệu
│
├── reports/                       # Báo cáo chính thức & Hồ sơ nghiệm thu của đề tài
│   ├── step2_official_report.md   # Mẫu báo cáo chính thức nộp GVHD (10 mục toàn diện, số liệu mới nhất)
│   ├── step2_executive_summary.md # Báo cáo tóm tắt nghiệm thu nội bộ Step 2
│   ├── feasibility_report.md      # Báo cáo tính khả thi & Bảng theo dõi xử lý 8 vấn đề tồn tại (R1 - R8)
│   ├── ward_selection.md          # Báo cáo cơ sở lựa chọn địa bàn Tây Thạnh & ranh giới GIS WGS84
│   └── data_dictionary.md         # Từ điển dữ liệu: cấu trúc bảng, kiểu dữ liệu, provenance & đơn vị đo
│
├── step2_outputs/                 # 6 Báo cáo kết quả đầu ra chuyên sâu của Step 2 (kèm minh chứng)
│   ├── README.md                  # Tổng mục lục và tóm tắt 6 kết quả chuyên đề
│   ├── 01_cvrplib_benchmark.md    # Kết quả 1: Bộ 6 benchmark CVRPLIB chuẩn quốc tế & khớp 100% BKS
│   ├── 02_toy_instance.md         # Kết quả 2: Toy instance 12 điểm tính tay & 8 ca kiểm thử biên tự động
│   ├── 03_tay_thanh_case_study.md # Kết quả 3: Case study 50 điểm Tây Thạnh, đồ thị ô tô SCC & kịch bản K-Q
│   ├── 04_dijkstra_matrix.md      # Kết quả 4: Ma trận khoảng cách có hướng Dijkstra 51x51 m
│   ├── 05_feasible_witness.md     # Kết quả 5: Minh chứng phân tuyến khả thi (Feasible Witness 4 xe hợp lệ)
│   └── 06_quality_validation.md   # Kết quả 6: Kiểm định chất lượng dữ liệu 24 tiêu chí & tính tái lập
│
├── guides/                        # Cẩm nang thực hành, kiểm thử và tài liệu bảo vệ đề tài
│   ├── step2_test_guide.md        # Hướng dẫn chi tiết từng câu lệnh kiểm tra (test) toàn diện Step 2
│   ├── theory_and_defense_guide.md# Cẩm nang toàn diện lý thuyết SFO, VND, GCVRP & kịch bản thuyết trình
│   └── scientific_rationale.md    # Cẩm nang giải trình khoa học: "Những gì đã làm và tại sao làm như vậy"
│
└── architecture/                  # Kiến trúc hệ thống & Kế hoạch triển khai Step 3
    └── system_architecture.md     # Thiết kế phân tầng, luồng dữ liệu, mô hình toán học & roadmap Step 3
```

---

## 🎯 2. HƯỚNG DẪN TRA CỨU NHANH THEO VAI TRÒ (READING PATHS)

Tùy theo mục đích tra cứu và vai trò, bạn đọc có thể tiếp cận tài liệu theo các lộ trình khuyến nghị:

### 👨‍🏫 Dành cho Giảng viên hướng dẫn (GVHD) & Hội đồng thẩm định
1. Đọc **[step2_official_report.md](./reports/step2_official_report.md)** để duyệt toàn bộ 10 mục nghiệm thu theo đúng biểu mẫu phân công.
2. Kiểm tra tiến độ giải quyết 8 vấn đề cốt lõi tại **[feasibility_report.md](./reports/feasibility_report.md)**.
3. Tham khảo cơ sở lựa chọn phường tại **[ward_selection.md](./reports/ward_selection.md)** và chứng cứ khả thi tại **[05_feasible_witness.md](./step2_outputs/05_feasible_witness.md)**.
4. Xem xét kế hoạch nghiên cứu giai đoạn tiếp theo tại **[system_architecture.md](./architecture/system_architecture.md)**.

### 👥 Dành cho Sinh viên nghiên cứu & Thành viên phản biện
1. Xem cẩm nang giải thích khoa học tại **[scientific_rationale.md](./guides/scientific_rationale.md)** để nắm bản chất "Tại sao lại làm như vậy?".
2. Ôn tập kiến thức lý thuyết và câu hỏi vấn đáp tại **[theory_and_defense_guide.md](./guides/theory_and_defense_guide.md)**.
3. Tra cứu quy cách thuộc tính, trường dữ liệu tại **[data_dictionary.md](./reports/data_dictionary.md)**.

### 💻 Dành cho Kỹ sư phát triển (Developer & Tester)
1. Thực hành chạy kiểm thử độc lập theo từng bước tại **[step2_test_guide.md](./guides/step2_test_guide.md)**.
2. Kiểm tra bộ dữ liệu và log kiểm định tại **[06_quality_validation.md](./step2_outputs/06_quality_validation.md)**.
3. Nắm vững luồng mã hóa/giải mã và quy trình tối ưu tại **[system_architecture.md](./architecture/system_architecture.md)**.

---

## 📊 3. BẢNG TỔNG HỢP LIÊN KẾT TÀI LIỆU CHI TIẾT

| STT | Tài liệu | Đường dẫn tệp | Mục tiêu chính | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| **I** | **HỒ SƠ BÁO CÁO NGHIỆM THU** | | | |
| 1 | Báo cáo chính thức Step 2 (Mẫu GVHD) | [`reports/step2_official_report.md`](./reports/step2_official_report.md) | Báo cáo đầy đủ 10 mục nộp GVHD | **Hoàn tất (PASS)** |
| 2 | Báo cáo tóm tắt nghiệm thu nội bộ | [`reports/step2_executive_summary.md`](./reports/step2_executive_summary.md) | Biên bản nghiệm thu nội bộ nhóm | **Hoàn tất (PASS)** |
| 3 | Báo cáo tính khả thi & Vấn đề R1–R8 | [`reports/feasibility_report.md`](./reports/feasibility_report.md) | Theo dõi xử lý các rủi ro Step 1 | **Hoàn tất (PASS)** |
| 4 | Báo cáo lựa chọn địa bàn Tây Thạnh | [`reports/ward_selection.md`](./reports/ward_selection.md) | Căn cứ địa lý GIS & buffer 400m | **Hoàn tất (PASS)** |
| 5 | Từ điển dữ liệu chuẩn (Data Dictionary) | [`reports/data_dictionary.md`](./reports/data_dictionary.md) | Khóa schema, xuất xứ & đơn vị đo | **Hoàn tất (PASS)** |
| **II** | **6 KẾT QUẢ ĐẦU RA STEP 2** | | | |
| 6 | Kết quả 1: Benchmark CVRPLIB | [`step2_outputs/01_cvrplib_benchmark.md`](./step2_outputs/01_cvrplib_benchmark.md) | 6 bộ dữ liệu chuẩn quốc tế & BKS | **Hoàn tất (PASS)** |
| 7 | Kết quả 2: Toy Instance 12 điểm | [`step2_outputs/02_toy_instance.md`](./step2_outputs/02_toy_instance.md) | Bảng tính tay & 8 ca test biên | **Hoàn tất (PASS)** |
| 8 | Kết quả 3: Case Study Tây Thạnh 50 điểm | [`step2_outputs/03_tay_thanh_case_study.md`](./step2_outputs/03_tay_thanh_case_study.md) | Dữ liệu 50 điểm, kịch bản K-Q | **Hoàn tất (PASS)** |
| 9 | Kết quả 4: Ma trận Dijkstra có hướng | [`step2_outputs/04_dijkstra_matrix.md`](./step2_outputs/04_dijkstra_matrix.md) | Ma trận cự ly $51 \times 51$ mét | **Hoàn tất (PASS)** |
| 10 | Kết quả 5: Feasible Witness | [`step2_outputs/05_feasible_witness.md`](./step2_outputs/05_feasible_witness.md) | Tuyến khả thi 4 xe không vượt tải | **Hoàn tất (PASS)** |
| 11 | Kết quả 6: Kiểm định chất lượng | [`step2_outputs/06_quality_validation.md`](./step2_outputs/06_quality_validation.md) | 24 tiêu chí tự động PASS 100% | **Hoàn tất (PASS)** |
| **III**| **CẨM NANG THỰC HÀNH & BẢO VỆ** | | | |
| 12 | Hướng dẫn tự kiểm tra từng bước | [`guides/step2_test_guide.md`](./guides/step2_test_guide.md) | Quy trình chạy test & lệnh CLI | **Hoàn tất (PASS)** |
| 13 | Cẩm nang lý thuyết & thuyết trình | [`guides/theory_and_defense_guide.md`](./guides/theory_and_defense_guide.md) | Kiến thức nền tảng SFO, VND & Q&A | **Hoàn tất (PASS)** |
| 14 | Cẩm nang giải trình khoa học Step 2 | [`guides/scientific_rationale.md`](./guides/scientific_rationale.md) | Cơ sở khoa học của từng quyết định | **Hoàn tất (PASS)** |
| **IV** | **KIẾN TRÚC & ROADMAP STEP 3** | | | |
| 15 | Kiến trúc hệ thống & Thiết kế thuật toán | [`architecture/system_architecture.md`](./architecture/system_architecture.md) | Phân tầng, luồng tối ưu & Roadmap | **Sẵn sàng Step 3** |

---

## ⚡ 4. LỆNH KIỂM CHỨNG NHANH (QUICK VERIFICATION COMMANDS)

Để kiểm chứng tính toàn vẹn và tính tái lập của toàn bộ hệ thống ngay trên máy trạm cục bộ, thực hiện:

```powershell
# 1. Chạy toàn bộ 40 ca kiểm thử Pytest tự động (Core, CVRPLIB Loader, Toy Instance)
py -m pytest

# 2. Chạy bộ kiểm định dữ liệu 24 tiêu chí chặt chẽ của Step 2
py tests/validate_dataset.py

# 3. Chạy kiểm thử nạp 6 bộ Benchmark CVRPLIB
py -m pytest tests/test_loader.py -v
```

> [!NOTE]
> Tất cả các kiểm thử đều hoạt động theo nguyên lý **Offline-First**, hoàn toàn không cần kết nối mạng hay tải lại tài nguyên ngoài, bảo đảm tính độc lập và khả năng tái lập 100%.
