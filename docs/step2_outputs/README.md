# 📑 TỔNG HỢP TOÀN BỘ KẾT QUẢ ĐẦU RA STEP 2 (STEP 2 DELIVERABLES)

> **Đơn vị đào tạo:** Trường Đại học Công Thương Thành phố Hồ Chí Minh (HUIT)  
> **Khoa/Ngành:** Ngành Khoa học Dữ liệu  
> **Đề tài NCKH:** Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND  
> **Chương trình:** Nghiên cứu Khoa học Sinh viên — Khóa 15  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu (Phiên bản v1.0)  
> **Nhóm sinh viên thực hiện:**  
> 1. **Vũ Thế Quang** *(Nhóm trưởng)*  
> 2. **Lê Nguyễn Tâm Đức**  
> 3. **Nguyễn Ngọc Thảo Hiền**  

---

## 🧭 MỤC LỤC CHI TIẾT CÁC KẾT QUẢ ĐẦU RA (STEP 2 OUTPUTS)

Thư mục này đóng gói **6 báo cáo kết quả chuyên biệt** tương ứng với 6 hạng mục bắt buộc theo yêu cầu nghiệm thu Step 2 của Giảng viên hướng dẫn:
* Bảng số liệu đầu ra thực tế và đối chứng minh chứng.
* Phân tích chuyên sâu cơ sở lý thuyết toán học và lý do khoa học của từng thiết kế/xử lý.
* Đầy đủ liên kết kiểm chứng đến mã nguồn, tệp dữ liệu gốc và nhật ký kiểm định.

---

### 📂 Danh mục 6 Báo cáo kết quả chuyên đề:

1. 🏆 [**01_cvrplib_benchmark.md**](./01_cvrplib_benchmark.md)
   * *Nội dung:* Nạp thành công 6 bộ benchmark quốc tế (`E-n33-k4`, `B-n50-k7`, `E-n51-k5`, `A-n53-k7`, `A-n60-k9`, `E-n76-k7`), khớp 100% nghiệm tối ưu BKS.
   * *Phân tích chuyên sâu:* Tại sao dùng thư viện `vrplib`? Tại sao quy ước làm tròn nguyên EUC_2D TSPLIB là bắt buộc? Tại sao không được gộp BKS khoảng cách với hàm fitness xanh?

2. 🎲 [**02_toy_instance.md**](./02_toy_instance.md)
   * *Nội dung:* Bài toán nhỏ 12 điểm khách + 1 depot ($K=3, Q=200$ kg), bảng tính toán chi tiết bằng tay từng chặng, 3 tuyến hợp lệ (309.36m).
   * *Phân tích chuyên sâu:* Tại sao phải tính tay Ground Truth? Tại sao tổng demand $\le K \times Q$ chỉ là điều kiện cần chứ chưa đủ? 8 ca kiểm thử biên tự động bắt lỗi.

3. 🏙️ [**03_tay_thanh_case_study.md**](./03_tay_thanh_case_study.md)
   * *Nội dung:* Địa bàn Phường Tây Thạnh (Quận Tân Phú), đồ thị ô tô 935 nút/2,123 cạnh, SCC 868 nút, 50 điểm thu gom trên 13 trục đường (snap = 0.0m), tổng demand 3,345 kg.
   * *Phân tích chuyên sâu:* Tại sao chọn Phường Tây Thạnh thay vì Sơn Kỳ cũ? Tại sao buffer 400m? Tại sao lấy điểm trực tiếp trên SCC đường ô tô? Phân tầng nhu cầu dân cư và thương mại.

4. 🛣️ [**04_dijkstra_matrix.md**](./04_dijkstra_matrix.md)
   * *Nội dung:* Ma trận cự ly $51 \times 51$ mét tính bằng Dijkstra có hướng, đối chiếu 3 cặp điểm bất đối xứng và 1 chu trình khép kín 2,864.6m (khớp 100%).
   * *Phân tích chuyên sâu:* Tại sao cấm dùng đường chim bay? Tại sao đường 1 chiều và dải phân cách làm ma trận bất đối xứng? Tại sao tuyệt đối không được tự ý điền 0 khi mất kết nối?

5. 📋 [**05_feasible_witness.md**](./05_feasible_witness.md)
   * *Nội dung:* Phương án phân tuyến 4 xe không vượt tải ($Q=1500$ kg), đối chứng với kết quả tối ưu 3 xe của Hybrid SFO-VND (giảm 14.92% cự ly, cắt giảm 21.49% $\text{CO}_2$).
   * *Phân tích chuyên sâu:* Tại sao bắt buộc có Feasible Witness trước khi cài metaheuristic? 4 ràng buộc cứng kinh điển của bài toán CVRP.

6. 🛡️ [**06_quality_validation.md**](./06_quality_validation.md)
   * *Nội dung:* Bộ kiểm định tự động `validate_dataset.py` đạt **24/24 tiêu chí PASS**, bộ kiểm thử Pytest đạt **40/40 unit tests PASS**, môi trường `requirements.txt`.
   * *Phân tích chuyên sâu:* Nguyên lý kiểm thử liên tục (CI) cho dữ liệu. Cơ chế Reproducibility & Offline-First (chạy lại độc lập không phụ thuộc Internet).

---

### 🔗 Tài liệu liên quan:
* 📑 **Báo cáo chính thức:** [step2_official_report.md](../reports/step2_official_report.md) — Mẫu báo cáo nghiệm thu nộp GVHD.
* 🧪 **Cẩm nang kiểm thử:** [step2_test_guide.md](../guides/step2_test_guide.md) — Hướng dẫn tự kiểm tra từng bước bằng dòng lệnh.
* 🏠 **Trang chủ tài liệu:** [docs/README.md](../README.md) — Cổng tài liệu trung tâm của dự án.
