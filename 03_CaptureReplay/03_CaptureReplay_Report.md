# BÁO CÁO KẾT QUẢ THỰC NGHIỆM - THÀNH VIÊN 3
## Module: Tự động hóa kiểm thử với phương pháp Capture/Replay

- **Họ và tên thành viên:** Thành viên 3 (Test Automation Engineer - Capture/Replay)
- **Ứng dụng kiểm thử:** [https://my-app-nextjs-xi.vercel.app/](https://my-app-nextjs-xi.vercel.app/) *(Mã nguồn: [pthaok6/LabFer202](https://github.com/pthaok6/LabFer202))*
- **Luồng kiểm thử chung:** Tìm kiếm sản phẩm (Search Products Flow)
- **Công cụ sử dụng:** Selenium IDE (file `.side`) & Playwright Codegen / Playwright Test Runner

---

## 1. Danh sách 5 Test Cases thực nghiệm (Thống nhất chung)

Bộ 5 Test Cases được chuẩn hóa mã định danh từ TC01 đến TC05 cho luồng tìm kiếm:

| Mã TC | Tên Test Case | Điều kiện đầu vào (Inputs) | Kết quả mong đợi (Expected Results) |
| :--- | :--- | :--- | :--- |
| **TC01** | Exact Name Search | `q = "Ripple Glass Set"`, `category = "All"` | Hiển thị chính xác sản phẩm "Ripple Glass Set" |
| **TC02** | Partial Name Search | `q = "lamp"`, `category = "All"` | Hiển thị sản phẩm "Mori Table Lamp" (chứa chữ "lamp", không phân biệt hoa thường) |
| **TC03** | Keyword & Category Filter | `q = "table"`, `category = "Lighting"` | Hiển thị "Mori Table Lamp" (khớp từ khóa "table" và thuộc danh mục Lighting) |
| **TC04** | Non-Existent Product Search | `q = "Laptop Dell XPS"`, `category = "All"` | Hiển thị thông báo "No products found." (`data-testid="no-results"`) |
| **TC05** | Empty Search (Show All) | `q = ""`, `category = "All"` | Hiển thị toàn bộ 6 sản phẩm trong danh sách (`data-testid="product-list"`) |

---

## 2. Bảng số liệu đo lường thời gian thực nghiệm ($T_{setup}, T_{auto}, T_{maint}$)

### 2.1. Thời gian xây dựng kịch bản ban đầu ($T_{setup}$)
- Mở công cụ Record (Playwright Codegen / Selenium IDE): ~3 phút
- Thao tác ghi kịch bản cho 5 Test Cases: ~12 phút
- Tinh chỉnh Assertions (kiểm tra text tiêu đề, thẻ `no-results`, số lượng card): ~15 phút
- Thử nghiệm Replay ban đầu và cấu hình runner: ~5 phút
- **Tổng chi phí xây dựng ban đầu ($T_{setup}$):** **35 phút (2.100 giây)**.

### 2.2. Thời gian thực thi tự động một lượt ($T_{auto}$)
Đo lường tự động chính xác qua 3 lần chạy liên tiếp trên trình duyệt Chromium (ghi nhận trực tiếp từ log thực nghiệm máy tính):

| Mã Test Case | Lần chạy 1 | Lần chạy 2 | Lần chạy 3 | Thời gian TB ($T_{auto}$) | Tỷ lệ thành công (Pass Rate) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **TC01 - Exact Name Search** | 2.60s (2.603ms) | 2.20s (2.196ms) | 2.25s (2.254ms) | **2.35s** (2.351 ms) | 100% |
| **TC02 - Partial Name Search** | 2.19s (2.186ms) | 2.19s (2.191ms) | 2.20s (2.202ms) | **2.19s** (2.193 ms) | 100% |
| **TC03 - Keyword & Category Filter** | 2.20s (2.196ms) | 2.20s (2.198ms) | 2.21s (2.214ms) | **2.20s** (2.203 ms) | 100% |
| **TC04 - Non-Existent Product** | 2.19s (2.193ms) | 2.17s (2.172ms) | 2.14s (2.142ms) | **2.17s** (2.169 ms) | 100% |
| **TC05 - Empty Keyword (Show All)** | 2.33s (2.326ms) | 2.31s (2.308ms) | 2.34s (2.337ms) | **2.32s** (2.324 ms) | 100% |
| **TOÀN BỘ SUITE (5 TEST CASES)** | **11.51s** | **11.07s** | **11.15s** | **11.24s** (11.240 ms) | **100%** |

*(Ghi chú: Toàn bộ suite gồm 5 test cases chạy qua Playwright Test Runner mất khoảng 11.0s).*

---

## 3. Thí nghiệm đo thời gian bảo trì kịch bản ($T_{maint}$) khi đổi Locator

### 3.1. Thiết lập thí nghiệm
Khi ứng dụng cập nhật giao diện, các bộ chọn phần tử (Locators) tự động ghi lại theo class CSS/thứ tự DOM sẽ bị lỗi thời:
1. **Locator 1 (Search Box):** Thay vì dùng `[data-testid="search-input"]`, kịch bản cũ dùng `input.legacy-search-field`.
2. **Locator 2 (Category Filter):** Kịch bản cũ dùng `select#old-filter-category`.
3. **Locator 3 (Search Button):** Kịch bản cũ dùng `button.btn-submit-search-v1`.

### 3.2. Kết quả khi chạy với Locator cũ / bị đổi
- File thực nghiệm: [`experiment_broken_locators.js`](file:///d:/Documents/Project/RBL_SWT/03_CaptureReplay/experiment_broken_locators.js)
- Trạng thái: **FAILED 100%** tại cả 3 bước tương tác.
- Lỗi ghi nhận:
  - `TimeoutError: locator.fill: Timeout 3000ms exceeded.`
  - `TimeoutError: locator.selectOption: Timeout 3000ms exceeded.`
  - `TimeoutError: locator.click: Timeout 3000ms exceeded.`

### 3.3. Thời gian bảo trì và cập nhật lại kịch bản ($T_{maint}$)
- **Thời gian phân tích lỗi & kiểm tra log:** ~4 phút.
- **Thời gian inspect lại DOM & cập nhật selector chuẩn (`data-testid`):** ~6 phút.
- **Thời gian chạy Replay xác minh lại (Pass 100%):** ~2 phút.
- **Tổng thời gian bảo trì ($T_{maint}$):** **12 phút (720 giây)**.
- File kiểm tra sau bảo trì: [`experiment_fixed_locators.js`](file:///d:/Documents/Project/RBL_SWT/03_CaptureReplay/experiment_fixed_locators.js) -> **PASS 100%** (Từng bước tương tác phản hồi trong 5ms - 33ms, submit hoàn thành trong 1044ms).

---

## 4. Dữ liệu cung cấp cho Thành viên 5 (Tính điểm hòa vốn Break-Even)

Theo công thức điểm hòa vốn thống nhất của nhóm:
$$N_{BE} = \frac{S}{M - A - R} \quad (\text{điều kiện: } M > A + R)$$

### 4.1. Tách riêng các thông số đo đạc thực nghiệm và giả định
- **Kết quả thực nghiệm đo trực tiếp bằng máy:**
  - **$A$ ($T_{auto}$ — Thời gian chạy tự động 1 lần cho toàn bộ 5 test cases):** **11.24 giây** (11.240 ms, trung bình qua 3 lượt chạy; độ lệch chuẩn rất thấp: 11.51s, 11.07s, 11.15s).
  - **Tỷ lệ thành công (Pass Rate):** **100%** (5/5 test cases pass khi locator chuẩn; **0%** / Fail 100% khi 3 locator trên giao diện bị thay đổi).
- **Chi phí thời gian xây dựng và sửa locator (báo cáo riêng theo quy ước Mục 4):**
  - **$S$ ($T_{setup}$ — Thời gian đầu tư ban đầu để xây dựng script):** **2.100 giây (35 phút)** *(Gồm mở công cụ record, thao tác 5 test cases, thêm assertions và tinh chỉnh chạy thử)*.
  - **$R_{locator}$ (Chi phí 1 lần sửa 3 locator khi UI thay đổi):** **720 giây (12 phút)** *(Gồm đọc log lỗi Timeout, inspect lại DOM và cập nhật 3 selector sang `data-testid`)*.
- **Giả định quy đổi $R$ theo chu kỳ bảo trì (để Thành viên 5 áp dụng công thức $M > A + R$):**
  - Nếu tính $R$ là chi phí bảo trì phân bổ trung bình trên mỗi lần chạy trong một chu kỳ quy ước (ví dụ mỗi chu kỳ $K = 30$ lần chạy hồi quy mới có 1 đợt cập nhật UI đổi locator):
    $$R = \frac{R_{locator}}{K} = \frac{720}{30} = 24 \text{ giây/lần chạy}$$
  - Nếu trong kỳ không phát sinh thay đổi giao diện ($R = 0$), điểm hòa vốn chỉ phụ thuộc vào $S / (M - A)$. Thành viên 5 có thể trình bày cả 2 kịch bản (không đổi UI và có đổi UI định kỳ) từ hai con số tách biệt $S = 2.100\text{s}$ và $R_{locator} = 720\text{s}$ này.

---

## 5. Cơ sở lý thuyết & Đánh giá phương pháp Capture/Replay (Tách biệt Lý thuyết vs. Thực nghiệm)

### 5.1. Cơ sở lý thuyết (Theo chuẩn ISTQB)
- **Capture/Replay (Record & Playback):** Là kỹ thuật tự động hóa kiểm thử trong đó công cụ ghi lại các thao tác của người dùng trên giao diện (click, nhập liệu, chọn phần tử) thành kịch bản tuyến tính (linear script), sau đó phát lại chính xác các bước đó để kiểm thử hồi quy (Regression Testing).
- **Liên hệ nguyên lý ISTQB:** Hỗ trợ tự động hóa kiểm thử lặp lại giúp giảm công sức chạy tay, nhưng chịu ảnh hưởng của *Pesticide Paradox* (Nghịch lý thuốc trừ sâu - script cố định chỉ lặp lại đúng một bộ dữ liệu nếu không kết hợp Data-Driven) và chi phí bảo trì cao khi giao diện thay đổi.

### 5.2. Ưu điểm ghi nhận từ thực nghiệm
1. **Tốc độ triển khai cực nhanh ($S$ thấp):** Không đòi hỏi xây dựng framework phức tạp từ đầu; Tester có thể thao tác trực tiếp trên trình duyệt để sinh mã khung.
2. **Trực quan:** Dễ dàng chạy demo trực tiếp trên trình duyệt (`npm run demo` hoặc Selenium IDE) để minh họa luồng nghiệp vụ.
3. **Xuất kịch bản đa dạng:** Playwright Codegen xuất trực tiếp ra mã nguồn chuẩn (`search_products.spec.js`), Selenium IDE lưu cấu trúc `.side` dễ chia sẻ.

### 5.3. Nhược điểm & Rủi ro thực nghiệm (Fragility & Maintenance)
1. **Kịch bản dễ gãy (Fragile Tests):** Thực nghiệm tại `experiment_broken_locators.js` chứng minh khi 3 locator trên UI thay đổi, 100% bước tương tác bị dừng vì `TimeoutError (3000ms exceeded)`.
2. **Trùng lặp mã & Khó mở rộng dữ liệu:** Dữ liệu kiểm thử (`"Ripple Glass Set"`, `"lamp"`, `"table"`...) bị gắn cứng (hard-coded) trong từng test case. Nếu tăng từ 5 lên 50 test cases, số dòng lệnh phải nhân bản tương ứng (khác với hướng Data-Driven của Thành viên 4).
3. **Phụ thuộc vào độ trễ mạng:** Phải bổ sung cơ chế chờ (`waitForLoadState('networkidle')`, `waitFor({ state: 'visible' })`) để tránh lỗi bất đồng bộ khi web tải dữ liệu.

---

## 6. Danh mục minh chứng (Evidence)
- Nhật ký thực thi console chi tiết: [`execution_console_log.txt`](file:///d:/Documents/Project/RBL_SWT/03_CaptureReplay/execution_console_log.txt)
- Các ảnh chụp màn hình kết quả kiểm thử được lưu trữ tại thư mục [`evidence/`](file:///d:/Documents/Project/RBL_SWT/evidence/):
  - `evidence_TC01_CaptureReplay.png`: Kết quả tìm kiếm chính xác sản phẩm "Ripple Glass Set".
  - `evidence_TC02_CaptureReplay.png`: Kết quả tìm kiếm không phân biệt hoa thường "lamp".
  - `evidence_TC03_CaptureReplay.png`: Kết quả kết hợp từ khóa "table" và danh mục "Lighting".
  - `evidence_TC04_CaptureReplay.png`: Kết quả tìm kiếm không tồn tại ("No products found.").
  - `evidence_TC05_CaptureReplay.png`: Kết quả chuỗi rỗng hiển thị đầy đủ 6 sản phẩm.
