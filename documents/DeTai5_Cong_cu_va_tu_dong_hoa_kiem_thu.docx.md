MÔN KIỂM THỬ PHẦN MỀM (ISTQB CTFL) – ĐỀ TÀI NHÓM

**ĐỀ TÀI 5**

# **Công cụ hỗ trợ kiểm thử: tự động hoá kiểm thử regression**

| Chương sách (trang) | Ch.6 (tr. 169–196) |
| :---- | :---- |
| **Slide** | SWT6 |
| **Thời lượng** | 2 tuần, nhóm 4–6 sinh viên |
| **Nhóm số** |  |
| **Thành viên (họ tên – MSSV)** |  |

Tài liệu nền là giáo trình *Foundations of Software Testing – ISTQB Certification* và bộ slide của môn. Bài làm phải có phần thực hành; báo cáo chỉ chép lý thuyết sẽ không đạt.

# **1\. Mục tiêu**

Tự động hoá một bộ test regression nhỏ bằng 2 cách và so sánh chi phí với chạy tay.

**Câu hỏi chính:** Sau bao nhiêu lần chạy thì tự động hoá rẻ hơn chạy tay?

**Đối tượng kiểm thử:** một ứng dụng web chạy trên máy của nhóm (mã nguồn mở hoặc tự viết).

# **2\. Nhiệm vụ**

1. Lập bảng 6 công cụ, mỗi công cụ thuộc một nhóm theo ISTQB (quản lý, tĩnh, thiết kế, thực thi, hiệu năng, chuyên biệt).

2. Chọn 1 luồng (đăng nhập, tìm kiếm) và viết 5–8 test case; chạy tay và bấm giờ.

3. Tự động hoá bộ test bằng 2 cách: capture/replay và data-driven.

4. Đổi 2–3 locator trên giao diện; đo thời gian sửa script của mỗi cách.

5. Tính điểm hoà vốn; nêu lợi ích và rủi ro của công cụ theo SWT6 (slide 37–39).

**Công cụ gợi ý:** Selenium IDE hoặc Playwright codegen (capture/replay); pytest \+ Selenium/Playwright (data-driven).

# **3\. Sản phẩm nộp**

* Bảng phân loại công cụ.

* 2 bộ script chạy được.

* Bảng đo thời gian và điểm hoà vốn.

# **4\. Format bài làm**

Nộp 3 thứ: báo cáo PDF, slide và sản phẩm thực hành (thư mục nén hoặc link repo). Tên file: NhomX\_DeTaiY\_BaoCao.pdf, NhomX\_DeTaiY\_Slide.pptx.

### ***Cấu trúc báo cáo***

1. **Bìa và bảng phân công:** tên đề tài, số nhóm, họ tên và MSSV, việc mỗi người làm.

2. **Giới thiệu** (1 trang): mục tiêu, câu hỏi chính, hệ thống được kiểm thử.

3. **Cơ sở lý thuyết** (2–3 trang): tóm tắt có dẫn chiếu sách và slide.

4. **Thực hành** (5–7 trang): các bước đã làm và sản phẩm tạo ra.

5. **Kết quả và thảo luận** (2–3 trang): trả lời câu hỏi chính bằng số liệu; liên hệ với ít nhất 2 trong 7 nguyên lý kiểm thử.

6. **Kết luận và tài liệu tham khảo** (1 trang).

Báo cáo 10–15 trang (không kể phụ lục), A4, Times New Roman 13, giãn dòng 1,3. Test case, log và ảnh chụp đầy đủ để ở phụ lục.

**Slide:** 10–12 slide; 10 phút trình bày, 5 phút hỏi đáp. Mọi thành viên đều phải trả lời được câu hỏi.

# **5\. Tiêu chí chấm điểm**

| Tiêu chí | Trọng số | Mức đạt tốt |
| :---- | :---: | :---- |
| Thực hành và sản phẩm | 40% | Đủ sản phẩm nộp; kiểm tra hoặc chạy lại được |
| Hiểu và dùng đúng lý thuyết | 20% | Đúng khái niệm, đúng thuật ngữ ISTQB |
| Kết quả, trả lời câu hỏi chính | 20% | Có số liệu và bảng so sánh |
| Báo cáo và thuyết trình | 20% | Đúng format, trình bày rõ, trả lời được câu hỏi |

Điểm cá nhân điều chỉnh theo mức đóng góp trong bảng phân công.