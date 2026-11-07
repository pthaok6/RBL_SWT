# HƯỚNG DẪN CHẠY KỊCH BẢN CAPTURE/REPLAY (THÀNH VIÊN 3)

Thư mục này chứa toàn bộ tài nguyên kiểm thử tự động theo phương pháp **Capture/Replay** cho luồng **Tìm kiếm sản phẩm** trên web `https://my-app-nextjs-xi.vercel.app/`.

---

## 1. Cấu trúc thư mục

```
03_CaptureReplay/
├── search_products.side          # File dự án chuẩn của Selenium IDE (TC01 -> TC05)
├── search_products.spec.js        # File test script Playwright
├── demo_visual.js                 # Script chạy demo trực quan mở trình duyệt (slowMo 800ms)
├── runner_benchmark.js            # Script đo thời gian thực nghiệm & xuất số liệu
├── experiment_broken_locators.js  # Script thực nghiệm khi đổi 3 locators (mô phỏng test fail)
├── experiment_fixed_locators.js   # Script xác nhận sau khi bảo trì locators (test pass)
├── execution_console_log.txt      # Nhật ký chạy thực tế đầy đủ trên PowerShell
├── broken_locators_log.txt        # Log ghi nhận lỗi timeout khi hỏng locator
├── fixed_locators_log.txt         # Log ghi nhận thành công sau khi sửa locator
├── 03_CaptureReplay_Metrics.csv   # File CSV tổng hợp thời gian từng test case & toàn bộ suite
├── timing_metrics.json            # Chi tiết thông số đo đạc 3 lượt chạy và thời gian trung bình
├── 03_CaptureReplay_Report.md     # Báo cáo phân tích chuyên sâu cho Thành viên 3
├── playwright.config.js           # Cấu hình Playwright test runner
├── package.json                   # Cấu hình phụ thuộc Node.js
└── README.md                      # Hướng dẫn chạy (file này)
```

---

## 2. Cách chạy bằng Selenium IDE (Giao diện trực quan)

1. Cài đặt tiện ích mở rộng **Selenium IDE** trên trình duyệt Chrome hoặc Firefox từ Chrome Web Store / Firefox Add-ons.
2. Mở tiện ích **Selenium IDE**.
3. Chọn **Open an existing project** và chọn file:
   ```
   03_CaptureReplay/search_products.side
   ```
4. Chọn test suite **Search Products Test Suite** hoặc chọn từng test case từ `TC01` đến `TC05`.
5. Bấm nút **Run all tests** (biểu tượng Play kép) để chạy lại toàn bộ kịch bản và xem trình duyệt thực thi.

---

## 3. Cách chạy bằng Playwright (Dòng lệnh CLI)

### Bước 1: Cài đặt môi trường (nếu chạy lần đầu)
Mở terminal tại thư mục gốc của project hoặc tại thư mục `03_CaptureReplay`:
```powershell
cd 03_CaptureReplay
npm install
npx playwright install chromium
```

### Bước 2: Chạy Demo trực quan (Mở trình duyệt thực tế để xem tự động thao tác)
```powershell
npm run demo
# Hoặc: node demo_visual.js
```
*Trình duyệt sẽ tự động mở lên, làm chậm tốc độ (slowMo 800ms) để giáo viên/nhóm quan sát rõ từng thao tác nhập liệu, lọc và tìm kiếm.*

### Bước 3: Chạy kiểm thử tự động tiêu chuẩn (Playwright Test Runner)
```powershell
npm test
# Hoặc: npx playwright test
```
*Để xem báo cáo trực quan dạng HTML của Playwright:*
```powershell
npm run report
```

### Bước 4: Chạy kịch bản Benchmark đo thời gian thực nghiệm ($T_{auto}$ qua 3 lượt)
```powershell
node runner_benchmark.js
```
Kết quả đo sẽ tự động cập nhật vào:
- `03_CaptureReplay_Metrics.csv`
- `timing_metrics.json`
- Các ảnh chụp minh chứng lưu tại `../evidence/evidence_TC0x_CaptureReplay.png`

### Bước 5: Chạy thí nghiệm kiểm tra tính dễ gãy và bảo trì ($T_{maint}$ / $R$)
- Chạy kịch bản lỗi khi đổi locator:
  ```powershell
  node experiment_broken_locators.js
  ```
- Chạy kịch bản sau khi sửa locator chuẩn:
  ```powershell
  node experiment_fixed_locators.js
  ```

