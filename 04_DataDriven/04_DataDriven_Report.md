# BÁO CÁO KẾT QUẢ THỰC NGHIỆM - THÀNH VIÊN 4
## Module: Tự động hóa kiểm thử theo phương pháp Data-Driven (pytest + Playwright)

- **Vai trò phụ trách:** Thành viên 4 (Test Automation Engineer — Data-Driven Testing)
- **Ứng dụng kiểm thử:** [https://my-app-nextjs-xi.vercel.app/](https://my-app-nextjs-xi.vercel.app/) *(Mã nguồn: [pthaok6/LabFer202](https://github.com/pthaok6/LabFer202))*
- **Luồng kiểm thử chung:** Tìm kiếm sản phẩm (Search Products Flow)
- **Công cụ & Kiến trúc sử dụng:** `pytest` (v9.2.0) + `Playwright` Python (v1.64.1) + Dữ liệu ngoại vi `CSV` (`test_data.csv`) + Quản lý Locator tập trung theo mẫu Page Object (`locators.py`).

---

## 1. Thiết kế dữ liệu kiểm thử (`test_data.csv`) và cơ chế kiểm chứng tự động

### 1.1. Bảng dữ liệu kiểm thử chuẩn hóa từ CSV (`TC01` $\rightarrow$ `TC05`)
Toàn bộ dữ liệu đầu vào và kết quả mong đợi được tách hoàn toàn khỏi mã nguồn kiểm thử và lưu trong file [`test_data.csv`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/test_data.csv) theo đúng quy ước chung của nhóm:

| `test_id` | `test_name` | `input` | `category` | `assertion_type` | `expected_result` | `expected_min_count` |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC01** | Exact Name Search | `Ripple Glass Set` | `All` | `exact_title` | `Ripple Glass Set` | `1` |
| **TC02** | Partial Name Search | `lamp` | `All` | `contains_title` | `Mori Table Lamp` | `1` |
| **TC03** | Keyword and Category Filter | `table` | `Lighting` | `contains_title` | `Mori Table Lamp` | `1` |
| **TC04** | Non-Existent Product Search | `Laptop Dell XPS` | `All` | `no_results` | `No products found.` | `0` |
| **TC05** | Empty Keyword and All Categories | `""` *(rỗng)* | `All` | `min_count` | `6 products displayed` | `6` |

### 1.2. Cơ chế đọc dữ liệu và kiểm tra kết quả mong đợi (Assertion Engine)
Trong [`test_search_datadriven.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/test_search_datadriven.py) và [`locators.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/locators.py):
1. **Hàm nạp dữ liệu động (`load_test_data`):** Đọc file `test_data.csv` bằng `csv.DictReader` và truyền trực tiếp vào decorator `@pytest.mark.parametrize("test_case", load_test_data())`. Chỉ cần **01 hàm kiểm thử duy nhất** (`test_search_products_data_driven`) để thực thi toàn bộ 5 trường hợp kiểm thử (và có thể mở rộng lên 50–100 dòng CSV mà không cần viết thêm hàm test mới).
2. **Cơ chế đối chiếu kết quả tự động (`verify_expected_result`):** Tự động phân nhánh cách kiểm tra dựa trên cột `assertion_type` và `expected_result` trong CSV:
   - `exact_title`: Kiểm tra tiêu đề sản phẩm hiển thị khớp chính xác 100% với `expected_result`.
   - `contains_title`: Kiểm tra sản phẩm trả về chứa chuỗi `expected_result` (không phân biệt hoa/thường).
   - `no_results`: Kiểm tra phần tử `[data-testid="no-results"]` hiển thị đúng thông báo `"No products found."`.
   - `min_count`: Đếm số lượng sản phẩm hiển thị trong `[data-testid="product-list"]` và đối chiếu $\ge$ `expected_min_count` (6 sản phẩm).
3. **Tự động ghi nhận kết quả & bằng chứng:** Sau mỗi test case, script tự động chụp ảnh màn hình lưu vào `04_DataDriven/evidence/evidence_TC0x_DataDriven.png` và xuất bảng kết quả chi tiết ra `pytest_execution_results.csv` / `04_DataDriven_Metrics.csv`.

---

## 2. Số liệu đo lường thời gian thực nghiệm ($S, A, R$)

> **Lưu ý phương pháp luận (theo Quy ước Mục 3 của nhóm):** Báo cáo tách biệt rõ ràng giữa **(1) Kết quả đo đạc thực nghiệm trực tiếp bằng máy tính**, **(2) Chi phí thời gian xây dựng và bảo trì kịch bản**, và **(3) Giả định quy đổi theo chu kỳ bảo trì**.

### 2.1. Thời gian đầu tư xây dựng kịch bản ban đầu ($S / T_{setup}$)
Khác với phương pháp Capture/Replay (chỉ cần bật trình ghi thao tác), phương pháp Data-Driven đòi hỏi đầu tư thời gian thiết kế kiến trúc ban đầu:
- Thiết kế schema file `test_data.csv` và viết bộ đọc dữ liệu CSV (`load_test_data`): ~10 phút
- Xây dựng lớp `SearchPage` và kho lưu trữ phần tử tập trung `SearchLocators` (`locators.py`): ~12 phút
- Viết hàm kiểm thử tham số hóa `@pytest.mark.parametrize` và bộ phân giải `verify_expected_result`: ~18 phút
- Cấu hình `pytest` fixture, cơ chế bấm giờ tự động, chụp ảnh màn hình và xuất file log CSV: ~10 phút
- **Tổng thời gian thiết lập ban đầu ($S$):** **50 phút (3.000 giây)**.

### 2.2. Thời gian thực thi tự động một lượt ($A / T_{auto}$) — Kết quả đo thực nghiệm bằng máy
Dữ liệu được ghi nhận trực tiếp từ thực nghiệm chạy 3 lượt liên tiếp (`runner_benchmark.py`) trên trình duyệt Chromium Headless đối với ứng dụng `https://my-app-nextjs-xi.vercel.app/` (chi tiết trong [`04_DataDriven_Metrics.csv`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/04_DataDriven_Metrics.csv) và [`timing_metrics.json`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/timing_metrics.json)):

| Mã Test Case | Lần chạy 1 | Lần chạy 2 | Lần chạy 3 | Thời gian TB ($A$) | Kết quả thực tế (Actual Result) | Tỷ lệ Pass |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| **TC01 - Exact Name Search** | 3.56s (3.565ms) | 2.45s (2.453ms) | 2.59s (2.593ms) | **2.87s** (2.870ms) | `Found exact product: 'Ripple Glass Set'` | 100% |
| **TC02 - Partial Name Search** | 2.66s (2.656ms) | 2.65s (2.654ms) | 2.46s (2.459ms) | **2.59s** (2.590ms) | `Found matching product: 'Mori Table Lamp'` | 100% |
| **TC03 - Keyword & Category Filter** | 2.82s (2.818ms) | 2.56s (2.563ms) | 2.42s (2.420ms) | **2.60s** (2.600ms) | `Found matching product: 'Mori Table Lamp'` | 100% |
| **TC04 - Non-Existent Product** | 2.70s (2.703ms) | 2.49s (2.494ms) | 2.63s (2.627ms) | **2.61s** (2.608ms) | `Displayed message: 'No products found.'` | 100% |
| **TC05 - Empty Keyword (Show All)** | 2.83s (2.829ms) | 2.70s (2.704ms) | 2.77s (2.773ms) | **2.77s** (2.769ms) | `6 products displayed (expected >= 6)` | 100% |
| **TOÀN BỘ SUITE (5 TEST CASES)** | **14.57s** (14.571ms) | **12.87s** (12.868ms) | **12.87s** (12.872ms) | **13.44s** (13.437ms) | **Khớp 100% với `expected_result` trong CSV** | **100%** |

*(Ghi chú: Khi chạy qua lệnh `python -m pytest` độc lập tại [`pytest_console_log.txt`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/pytest_console_log.txt), mỗi test case được khởi tạo một Browser Context cô lập hoàn toàn và chụp đồng thời 2 ảnh minh chứng full-page nên mất tổng cộng 27.32s cho phần thực thi 5 test cases; trong khi chạy cùng điều kiện benchmark như Thành viên 3 qua `runner_benchmark.py` mất trung bình **13.44s**).*

---

## 3. Thí nghiệm đổi 3 Locator trên giao diện và đo thời gian bảo trì ($R / T_{maint}$)

### 3.1. Thiết lập thí nghiệm (Đồng bộ 3 Locator với Thành viên 3)
Để đảm bảo tính nhất quán khi so sánh giữa Capture/Replay và Data-Driven, thí nghiệm giả lập cùng 3 phần tử trên giao diện bị thay đổi bộ chọn (locators):
1. **Locator 1 (Search Input):** `input.legacy-search-field` $\rightarrow$ đổi sang `[data-testid="search-input"]`
2. **Locator 2 (Category Select):** `select#old-filter-category` $\rightarrow$ đổi sang `[data-testid="category-select"]`
3. **Locator 3 (Search Button):** `button.btn-submit-search-v1` $\rightarrow$ đổi sang `[data-testid="btn-search"]`

### 3.2. Kết quả khi chạy với 3 Locator bị thay đổi (`experiment_broken_locators.py`)
- Minh chứng log: [`broken_locators_log.txt`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/broken_locators_log.txt)
- Trạng thái: **FAILED 100%** tại cả 3 thao tác tương tác với lỗi:
  - `TimeoutError - Locator.fill: Timeout 3000ms exceeded.`
  - `TimeoutError - Locator.select_option: Timeout 3000ms exceeded.`
  - `TimeoutError - Locator.click: Timeout 3000ms exceeded.`

### 3.3. Quy trình sửa lỗi tập trung và thời gian bảo trì ($R_{locator}$)
Trong kiến trúc Data-Driven kết hợp Page Object (`locators.py`), các bộ chọn giao diện **không bị lặp lại** trong từng test case (như Capture/Replay phải sửa tới 15 chỗ trong 5 hàm test). Thay vào đó, kiểm thử viên:
- **Không cần chạm vào** file dữ liệu [`test_data.csv`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/test_data.csv).
- **Không cần chạm vào** file kịch bản kiểm thử [`test_search_datadriven.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/test_search_datadriven.py).
- **Chỉ cần cập nhật đúng 3 dòng khai báo tại 01 nơi duy nhất** là đối tượng `STANDARD_LOCATORS` trong [`locators.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/locators.py#L29-L36).

**Thời gian đo đạc quá trình bảo trì ($R_{locator}$):**
- Đọc log lỗi và định vị file `locators.py`: ~1.5 phút
- Inspect DOM trên trình duyệt và sửa 3 thuộc tính trong `STANDARD_LOCATORS` (`locators.py`): ~2.5 phút
- Chạy lại [`experiment_fixed_locators.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/experiment_fixed_locators.py) để xác nhận toàn bộ 5 dòng dữ liệu CSV đều PASS 100% (`fixed_locators_log.txt`): ~1.0 phút
- **Tổng thời gian bảo trì 1 lần đổi 3 locator ($R_{locator}$):** **5 phút (300 giây)** *(Nhanh hơn **2.4 lần** so với 12 phút / 720 giây của phương pháp Capture/Replay)*.

---

## 4. Bảng tổng hợp số liệu bàn giao cho Thành viên 5 (Tính điểm hòa vốn $N_{BE}$)

Theo công thức điểm hòa vốn thống nhất tại Mục 4 của tài liệu quy ước nhóm (`RBL.md`):
$$N_{BE} = \frac{S}{M - A - R} \quad (\text{với điều kiện: } M > A + R)$$

Dưới đây là bảng đối chiếu thông số của **Thành viên 4 (Data-Driven)** bên cạnh **Thành viên 3 (Capture/Replay)** để Thành viên 5 đưa vào mô hình tính toán:

| Ký hiệu | Ý nghĩa thông số | Thành viên 3 (Capture/Replay) | Thành viên 4 (Data-Driven) | Ghi chú (Thực nghiệm vs. Giả định) |
| :---: | :--- | :---: | :---: | :--- |
| **$S$** | Thời gian đầu tư ban đầu để xây dựng script | 2.100 giây (35 phút) | **3.000 giây (50 phút)** | Thực tế xây dựng: Data-Driven tốn công viết bộ đọc CSV & Page Object ban đầu hơn |
| **$A$** | Thời gian chạy tự động 1 lần cho cả bộ 5 TC | 11.24 giây (11.240 ms) | **13.44 giây (13.437 ms)** | **Số liệu thực nghiệm đo bằng máy** (Trung bình 3 lượt chạy liên tiếp) |
| **$R_{locator}$** | Chi phí 1 đợt sửa 3 locator khi UI thay đổi | 720 giây (12 phút) | **300 giây (5 phút)** | Thực nghiệm bảo trì: Data-Driven chỉ sửa tại 1 nơi duy nhất (`locators.py`) |
| **$R$** *(Kịch bản 1)* | Chi phí bảo trì trung bình/lần chạy khi UI không đổi | 0 giây | **0 giây** | Áp dụng khi giao diện ổn định trong chu kỳ hồi quy |
| **$R$** *(Kịch bản 2)* | Chi phí bảo trì phân bổ mỗi lần chạy (giả định chu kỳ $K = 30$ lần chạy có 1 lần đổi UI) | $\frac{720}{30} = 24\text{ giây/lần}$ | **$\frac{300}{30} = 10\text{ giây/lần}$** | **Giả định quy đổi** cùng hệ quy chiếu $K=30$ để Thành viên 5 vẽ biểu đồ so sánh |

---

## 5. Cơ sở lý thuyết ISTQB & Đánh giá phương pháp Data-Driven

### 5.1. Cơ sở lý thuyết (Theo giáo trình ISTQB CTFL Ch.6)
- **Kỹ thuật kiểm thử hướng dữ liệu (Data-Driven Testing):** Là phương pháp tự động hóa tách biệt dữ liệu đầu vào (inputs) và kết quả mong đợi (expected outcomes) ra khỏi kịch bản điều khiển (control script), lưu trữ dữ liệu trong bảng tính hoặc file CSV. Một kịch bản điều khiển tổng quát duy nhất sẽ đọc từng dòng dữ liệu để thực thi kiểm thử lặp lại với các bộ giá trị khác nhau.
- **Liên hệ 7 nguyên lý kiểm thử ISTQB:**
  1. **Nguyên lý 5 — Nghịch lý thuốc trừ sâu (Pesticide Paradox):** Nếu chạy đi chạy lại một kịch bản Capture/Replay với dữ liệu gắn cứng (hard-coded), bộ test sẽ không tìm thêm được lỗi mới. Data-Driven giải quyết triệt để vấn đề này bằng cách cho phép kiểm thử viên dễ dàng bổ sung hàng chục trường hợp dữ liệu biên, ký tự đặc biệt, chuỗi dài vào `test_data.csv` mà không cần sửa code.
  2. **Nguyên lý 6 — Kiểm thử phụ thuộc vào ngữ cảnh (Testing is Context Dependent):** Thực nghiệm cho thấy không có phương pháp nào tối ưu tuyệt đối trong mọi ngữ cảnh:
     - Nếu số lần chạy hồi quy ít và giao diện hiếm khi thay đổi, **Capture/Replay** có lợi thế nhờ chi phí khởi tạo $S$ thấp ($2.100\text{s}$ so với $3.000\text{s}$).
     - Ngược lại, trong dự án phát triển dài hạn (Agile/CI-CD), số lượng dữ liệu kiểm thử lớn và giao diện thường xuyên tinh chỉnh, **Data-Driven kết hợp Centralized Locators** vượt trội hoàn toàn nhờ chi phí bảo trì $R$ thấp ($300\text{s}$ so với $720\text{s}$) và khả năng tái sử dụng cao.

### 5.2. Ưu điểm và Rủi ro ghi nhận từ thực nghiệm
- **Ưu điểm thực nghiệm:**
  - **Khả năng mở rộng dữ liệu (Scalability):** Thêm test case mới chỉ tốn vài giây thêm dòng vào `test_data.csv`.
  - **Chi phí bảo trì thấp (High Maintainability):** Nhờ gom toàn bộ selector vào `locators.py`, khi 3 locator trên UI thay đổi chỉ cần sửa 3 dòng tại 1 file duy nhất, giảm 58.3% thời gian bảo trì so với Capture/Replay.
  - **Người không chuyên lập trình có thể tham gia thiết kế dữ liệu:** Manual Tester (Thành viên 2) có thể trực tiếp biên tập file CSV mà không cần can thiệp vào mã Python.
- **Nhược điểm & Rủi ro thực nghiệm (theo Slide SWT6):**
  - **Chi phí đầu tư ban đầu cao hơn ($S = 50\text{ phút}$):** Đòi hỏi kỹ năng lập trình Python, hiểu biết về `pytest` fixtures, xử lý bất đồng bộ của Playwright và thiết kế kiến trúc phân tầng.
  - **Rủi ro phụ thuộc cấu trúc dữ liệu:** Nếu nhập sai tên cột hoặc sai mã `assertion_type` trong file CSV, kịch bản cần cơ chế bắt lỗi rõ ràng để tránh báo sai kết quả.

---

## 6. Danh mục sản phẩm và bằng chứng bàn giao (`04_DataDriven/`)

1. **Dữ liệu kiểm thử mẫu:** [`test_data.csv`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/test_data.csv)
2. **Script kiểm thử chính & Quản lý Locator:**
   - [`test_search_datadriven.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/test_search_datadriven.py)
   - [`locators.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/locators.py)
   - [`runner_benchmark.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/runner_benchmark.py)
   - [`experiment_broken_locators.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/experiment_broken_locators.py) & [`experiment_fixed_locators.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/experiment_fixed_locators.py)
   - [`demo_visual.py`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/demo_visual.py)
3. **Dữ liệu đo thời gian & Log thực thi thực tế:**
   - [`04_DataDriven_Metrics.csv`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/04_DataDriven_Metrics.csv) & [`timing_metrics.json`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/timing_metrics.json)
   - [`pytest_execution_results.csv`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/pytest_execution_results.csv) & [`pytest_console_log.txt`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/pytest_console_log.txt)
   - [`execution_console_log.txt`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/execution_console_log.txt)
   - [`broken_locators_log.txt`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/broken_locators_log.txt) & [`fixed_locators_log.txt`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/fixed_locators_log.txt)
4. **Ảnh chụp màn hình bằng chứng (`04_DataDriven/evidence/`):**
   - [`evidence_TC01_DataDriven.png`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/evidence/evidence_TC01_DataDriven.png)
   - [`evidence_TC02_DataDriven.png`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/evidence/evidence_TC02_DataDriven.png)
   - [`evidence_TC03_DataDriven.png`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/evidence/evidence_TC03_DataDriven.png)
   - [`evidence_TC04_DataDriven.png`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/evidence/evidence_TC04_DataDriven.png)
   - [`evidence_TC05_DataDriven.png`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/evidence/evidence_TC05_DataDriven.png)
5. **Hướng dẫn cài đặt và chạy:** [`README.md`](file:///d:/Student_Project/RBL_SWT/04_DataDriven/README.md)

