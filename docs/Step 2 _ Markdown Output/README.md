# 📑 TỔNG HỢP TOÀN BỘ KẾT QUẢ VÀ BÁO CÁO NGHIỆM THU STEP 2

> **Đề tài NCKH:** Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND  
> **Chương trình:** Nghiên cứu Khoa học Sinh viên — Khóa 15  
> **Giai đoạn:** Step 2 — Chuẩn bị và khóa bộ dữ liệu (Phiên bản v1.0)  
> **Nhóm sinh viên thực hiện:**  
> 1. **Vũ Thế Quang** *(Nhóm trưởng)*  
> 2. **Lê Nguyễn Tâm Đức**  
> 3. **Nguyễn Ngọc Thảo Hiền**  

---

## 🧭 MỤC LỤC CHI TIẾT TỪNG KẾT QUẢ (STEP 2 MARKDOWN OUTPUT)

Thư mục này được tổ chức theo tiêu chuẩn khoa học cao cấp: **Mỗi đầu ra kết quả chính của Step 2 được đóng gói thành 01 tệp Markdown chuyên biệt**, bao gồm:
* Số liệu đầu ra thực tế và đối chứng minh chứng.
* Phân tích chuyên sâu cơ sở lý thuyết toán học và tại sao lại thiết kế/xử lý như vậy.
* Đầy đủ liên kết kiểm chứng đến mã nguồn, tệp dữ liệu gốc và nhật ký kiểm định.

---

### 📂 Danh mục 7 Báo cáo chuyên đề:

1. 🏆 [**01_Ket_qua_CVRPLIB_Benchmark.md**](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/Step%202%20_%20Markdown%20Output/01_Ket_qua_CVRPLIB_Benchmark.md)
   * *Nội dung:* Nạp thành công 6 bộ benchmark quốc tế (`E-n33-k4`, `B-n50-k7`, `E-n51-k5`, `A-n53-k7`, `A-n60-k9`, `E-n76-k7`), khớp 100% nghiệm tối ưu BKS.
   * *Phân tích chuyên sâu:* Tại sao dùng thư viện `vrplib`? Tại sao quy ước làm tròn nguyên EUC_2D TSPLIB là bắt buộc? Tại sao không được gộp BKS khoảng cách với hàm fitness xanh?

2. 🎲 [**02_Ket_qua_Toy_Instance_12_Diem.md**](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/Step%202%20_%20Markdown%20Output/02_Ket_qua_Toy_Instance_12_Diem.md)
   * *Nội dung:* Bài toán nhỏ 12 điểm khách + 1 depot ($K=3, Q=200$ kg), bảng tính toán chi tiết bằng tay từng chặng, 3 tuyến hợp lệ (309.36m).
   * *Phân tích chuyên sâu:* Tại sao phải tính tay Ground Truth? Tại sao tổng demand $\le K \times Q$ chỉ là điều kiện cần chứ chưa đủ? 8 ca kiểm thử biên tự động bắt lỗi.

3. 🏙️ [**03_Ket_qua_Case_Study_Tay_Thanh_50_Diem.md**](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/Step%202%20_%20Markdown%20Output/03_Ket_qua_Case_Study_Tay_Thanh_50_Diem.md)
   * *Nội dung:* Địa bàn Phường Tây Thạnh (Quận Tân Phú), đồ thị ô tô 935 nút/2,123 cạnh, SCC 868 nút, 50 điểm thu gom trên 13 trục đường (snap = 0.0m), tổng demand 3,345 kg.
   * *Phân tích chuyên sâu:* Tại sao chọn Phường Tây Thạnh thay vì Sơn Kỳ cũ? Tại sao buffer 400m? Tại sao lấy điểm trực tiếp trên SCC đường ô tô? Phân tầng nhu cầu dân cư và thương mại.

4. 🛣️ [**04_Ket_qua_Ma_tran_Khoang_cach_Co_huong_Dijkstra.md**](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/Step%202%20_%20Markdown%20Output/04_Ket_qua_Ma_tran_Khoang_cach_Co_huong_Dijkstra.md)
   * *Nội dung:* Ma trận cự ly $51 \times 51$ mét tính bằng Dijkstra có hướng, đối chiếu 3 cặp điểm bất đối xứng và 1 chu trình khép kín 2,864.6m (khớp 100%).
   * *Phân tích chuyên sâu:* Tại sao cấm dùng đường chim bay? Tại sao đường 1 chiều và dải phân cách làm ma trận bất đối xứng? Tại sao tuyệt đối không được tự ý điền 0 khi mất kết nối?

5. 📋 [**05_Ket_qua_Phan_tuyen_Kha_thi_Feasible_Witness.md**](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/Step%202%20_%20Markdown%20Output/05_Ket_qua_Phan_tuyen_Kha_thi_Feasible_Witness.md)
   * *Nội dung:* Phương án phân tuyến 4 xe không vượt tải ($Q=1500$ kg), đối chứng với kết quả tối ưu 3 xe của Hybrid SFO-VND (giảm 14.92% cự ly, cắt giảm 21.49% $\text{CO}_2$).
   * *Phân tích chuyên sâu:* Tại sao bắt buộc có Feasible Witness trước khi cài metaheuristic? 4 ràng buộc cứng kinh điển của bài toán CVRP.

6. 🛡️ [**06_Ket_qua_Kiem_dinh_Chat_luong_va_Tai_lap.md**](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/Step%202%20_%20Markdown%20Output/06_Ket_qua_Kiem_dinh_Chat_luong_va_Tai_lap.md)
   * *Nội dung:* Bộ kiểm định tự động `validate_dataset.py` đạt **23/23 tiêu chí PASS**, bộ kiểm thử Pytest đạt **34/34 unit tests PASS**, môi trường `requirements.txt`.
   * *Phân tích chuyên sâu:* Nguyên lý kiểm thử liên tục (CI) cho dữ liệu. Cơ chế Reproducibility & Offline-First (chạy lại độc lập không phụ thuộc Internet).

7. 📑 [**Step 2 _ Mau Bao Cao .md**](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/Step%202%20_%20Markdown%20Output/Step%202%20_%20Mau%20Bao%20Cao%20.md)
   * *Nội dung:* **MẪU BÁO CÁO TOÀN DIỆN 10 MỤC NỘP GIẢNG VIÊN HƯỚNG DẪN**, tích hợp toàn bộ số liệu mới nhất, bảng phân công minh chứng và 3 câu hỏi xin ý kiến Thầy trước khi sang Step 3.

8. 🧪 [**huong_dan_test_tung_buoc_cua_step_2.md**](file:///e:/15DHKHDL03/2026-2027/HKI_26_27/SFO_VND/Source/docs/Step%202%20_%20Markdown%20Output/huong_dan_test_tung_buoc_cua_step_2.md)
   * *Nội dung:* **HƯỚNG DẪN TỰ KIỂM TRA (TEST) TỪNG BƯỚC CỦA STEP 2** — Cẩm nang chi tiết 9 quy trình kiểm thử từ Benchmark, Toy tính tay, Snap 0m, Ma trận Dijkstra 51x51, Feasible Witness, 23 tiêu chí validation, 34 bài pytest, bản đồ trực quan đến bảng Cheat sheet lệnh test nhanh.

