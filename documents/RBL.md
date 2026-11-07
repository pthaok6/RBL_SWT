### **Cấu trúc thư mục chung**

[https\://github.com/pthaok6/RBL\_SWT](https://github.com/pthaok6/RBL_SWT) 

## **1\. Bảng phân chia công việc cho 5 thành viên**

Phương án tối ưu: mỗi thành viên có đầu ra riêng, có thể bắt đầu ngay trong ngày đầu tiên.

**Thành viên 1 — Lý thuyết ISTQB và phân loại công cụ**

Độc lập hoàn toàn

* Lập bảng phân loại 6 công cụ theo 6 nhóm: quản lý, tĩnh, thiết kế, thực thi, hiệu năng và chuyên biệt.  
* Tóm tắt lý thuyết regression testing, test automation và lợi ích/rủi ro của công cụ.  
* Liên hệ các nguyên lý kiểm thử ISTQB liên quan.  
* Dùng AI hỗ trợ tra cứu, diễn giải và tạo bảng có nguồn tham khảo.

Bàn giao: `01_LyThuyet.docx`, `01_CongCu.xlsx`

**Thành viên 2 — Test case và kiểm thử thủ công**

Độc lập sau khi chốt đề bài chung

* Viết 5–8 test case cho một luồng web, chẳng hạn đăng nhập.  
* Xác định bước thực hiện, dữ liệu đầu vào, kết quả mong đợi và kết quả thực tế.  
* Chạy test thủ công, bấm giờ từng lần và lưu bằng chứng.  
* Tự lập bảng dữ liệu test theo định dạng CSV để các kết quả có thể được tái sử dụng.

Bàn giao: `02_TestCases.xlsx`, `02_ManualResults.csv`, ảnh chụp/log.

**Thành viên 3 — Tự động hóa capture/replay**

Module độc lập

* Dùng Selenium IDE hoặc Playwright Codegen để ghi lại thao tác kiểm thử.  
* Chỉnh sửa và chạy lại script đã ghi.  
* Đổi 2–3 locator trên giao diện thử nghiệm, đo thời gian sửa script và kiểm tra lại.  
* Ghi nhận thời gian chạy, tỷ lệ thành công và các lỗi phát sinh.

Bàn giao: `03_CaptureReplay/`, script, hướng dẫn chạy và log đo thời gian.

**Thành viên 4 — Tự động hóa data-driven**

Module độc lập

* Dùng pytest kết hợp Selenium hoặc Playwright.  
* Tạo script đọc dữ liệu kiểm thử từ CSV và chạy nhiều trường hợp.  
* Thiết kế cơ chế kiểm tra kết quả mong đợi và ghi nhận kết quả từng test.  
* Đổi 2–3 locator trên giao diện thử nghiệm, đo thời gian sửa và chạy lại.

Bàn giao: `04_DataDriven/`, script, dữ liệu mẫu, hướng dẫn chạy và log.

**Thành viên 5 — Mô hình chi phí, báo cáo và slide**

Độc lập trong giai đoạn chuẩn bị

* Tạo mẫu báo cáo PDF, mục lục và bảng phân công.  
* Tạo mẫu bảng so sánh chạy tay, capture/replay và data-driven.  
* Chuẩn bị công thức điểm hòa vốn, biểu đồ và bố cục slide 10–12 trang.  
* Soạn phần giới thiệu, kết luận mẫu và câu hỏi phản biện.  
* Chỉ điền số liệu thực nghiệm sau khi các thành viên hoàn thành phép đo.

Bàn giao: `05_ReportTemplate.docx`, `05_BreakEven.xlsx`, `05_Slides.pptx`.

## **2\. Quy tắc để không xảy ra xung đột khi ghép bài**

Điểm quan trọng nhất: các thành viên không tự chọn các thông số khác nhau cho cùng một thí nghiệm. Nhóm cần thống nhất một bộ quy ước chung ngay từ đầu.

| Hạng mục | Quy ước chung |
| ----- | ----- |
| Ứng dụng kiểm thử | repo: [https\://github.com/pthaok6/LabFer202](https://github.com/pthaok6/LabFer202)  web: [https\://my-app-nextjs-xi.vercel.app/](https://my-app-nextjs-xi.vercel.app/)  |
| Luồng kiểm thử | Luồng tìm kiếm sản phẩm |
| Test case | 5 trường hợp, dùng chung ID `TC01` đến `TC05` |
| Dữ liệu | CSV với cột `test_id`, `input`, `expected_result` và các cột cần thiết khác |
| Capture/replay | Selenium IDE hoặc Playwright Codegen |
| Data-driven | pytest \+ Selenium hoặc pytest \+ Playwright |
| Đo thời gian | Cùng cách bấm giờ, ghi rõ số lần chạy và đơn vị |
| Định dạng bàn giao | Mỗi người chỉ sửa file trong thư mục được giao |

Lưu ý: Các trường hợp đăng nhập có thể cần nhiều cột dữ liệu hơn; nhóm nên chốt schema CSV phù hợp với ứng dụng. Cả hai phương pháp tự động hóa phải kiểm tra cùng một bộ tình huống để kết quả so sánh có ý nghĩa.

## **3\. Mỗi thành viên dùng AI như thế nào?**

Bối cảnh: Dự án sinh viên kiểm thử một ứng dụng web bằng một luồng chức năng chung. Nhóm cần so sánh kiểm thử thủ công với hai cách tự động hóa: capture/replay và data-driven.

Yêu cầu:

* Chỉ thực hiện nhiệm vụ được giao, không tự mở rộng phạm vi.  
* Dùng thuật ngữ kiểm thử phần mềm chính xác nhưng giải thích dễ hiểu.  
* Không bịa kết quả chạy, thời gian đo, nguồn tham khảo hoặc bằng chứng.  
* Tách rõ nội dung lý thuyết, giả định và kết quả thực nghiệm.  
* Tạo đầu ra đúng định dạng bàn giao đã quy định.  
* Không sửa hoặc tạo thay thế các file thuộc thành viên khác.  
* Nếu thiếu thông tin quan trọng, hãy nêu rõ thay vì tự giả định.

Sau đó, mỗi thành viên thêm phần nhiệm vụ cụ thể của mình. Ví dụ, thành viên 3 yêu cầu AI chỉ hỗ trợ script capture/replay; thành viên 4 yêu cầu AI chỉ hỗ trợ script data-driven. Không để AI tự tạo lại toàn bộ dự án ở mỗi máy.

## **4\. Công thức hòa vốn cần thống nhất**

Thành viên 5 có thể chuẩn bị sẵn bảng tính với công thức dưới đây; các thành viên thực nghiệm chỉ cần cung cấp số liệu thực đo.

Ký hiệu:

* $M$: thời gian chạy thủ công cho một lần.  
* $A$: thời gian chạy tự động cho một lần.  
* $S$: thời gian đầu tư ban đầu để xây dựng script.  
* $R$: thời gian bảo trì script sau mỗi lần sửa đổi hoặc chu kỳ bảo trì quy ước.

Điểm hòa vốn theo số lần chạy, trong trường hợp có chi phí thiết lập ban đầu và chi phí bảo trì trung bình:

${N}_{BE}=\frac{S}{M-A-R}$

Công thức chỉ có ý nghĩa khi $M>A+R$. Nếu không thỏa mãn, tự động hóa chưa tiết kiệm thời gian theo mô hình đang xét.

Cần thống nhất cách tính: nếu chi phí sửa locator đã nằm trong $R$, không cộng lại lần nữa. Với đề tài này, nhóm cũng nên báo cáo riêng chi phí xây dựng ban đầu và chi phí sửa locator đo được, thay vì chỉ đưa ra một con số hòa vốn không có giải thích.

