# HƯỚNG DẪN CHẠY KỊCH BẢN DATA-DRIVEN TESTING (THÀNH VIÊN 4)

Thư mục này chứa toàn bộ tài nguyên kiểm thử tự động theo phương pháp **Data-Driven Testing (Hướng dữ liệu)** sử dụng **pytest + Playwright (Python)** kết hợp đọc dữ liệu kiểm thử từ file **CSV** cho luồng **Tìm kiếm sản phẩm (Search Products Flow)** trên ứng dụng web `https://my-app-nextjs-xi.vercel.app/`.

---

## 1. Cấu trúc thư mục bàn giao (`04_DataDriven/`)

```text
04_DataDriven/
├── test_data.csv                  # Dữ liệu kiểm thử đầu vào chuẩn hóa (TC01 -> TC05)
├── locators.py                    # Quản lý tập trung Locator (Page Object / Single Point of Maintenance)
├── test_search_datadriven.py      # Script kiểm thử chính dùng pytest (@pytest.mark.parametrize) đọc CSV
├── runner_benchmark.py            # Script đo thời gian thực nghiệm 3 lượt chạy & xuất số liệu CSV/JSON
├── experiment_broken_locators.py  # Thí nghiệm khi 3 locator trên UI thay đổi (ghi nhận lỗi Timeout)
├── experiment_fixed_locators.py   # Thí nghiệm xác minh sau khi sửa 3 locator tại 1 nơi duy nhất (locators.py)
├── demo_visual.py                 # Script chạy demo trực quan mở trình duyệt (slow_mo=800ms)
├── pytest_execution_results.csv   # Kết quả ghi nhận tự động sau khi chạy lệnh pytest
├── 04_DataDriven_Metrics.csv      # Bảng tổng hợp thời gian chạy 3 lượt và trung bình (T_auto / A)
├── timing_metrics.json            # Dữ liệu JSON chi tiết phục vụ tính toán điểm hòa vốn
├── pytest_console_log.txt         # Log thực thi thực tế của lệnh pytest
├── execution_console_log.txt      # Log thực thi thực tế của benchmark 3 lượt chạy
├── broken_locators_log.txt        # Log ghi nhận lỗi khi 3 locator giao diện thay đổi
├── fixed_locators_log.txt         # Log xác nhận Pass 100% sau khi cập nhật locator tập trung
├── evidence/                      # Thư mục lưu ảnh chụp màn hình bằng chứng từng test case
│   ├── evidence_TC01_DataDriven.png
│   ├── evidence_TC02_DataDriven.png
│   ├── evidence_TC03_DataDriven.png
│   ├── evidence_TC04_DataDriven.png
│   └── evidence_TC05_DataDriven.png
├── 04_DataDriven_Report.md        # Báo cáo kết quả thực nghiệm & phân tích của Thành viên 4
├── pytest.ini                     # Cấu hình mặc định cho pytest
├── requirements.txt               # Danh sách thư viện Python cần thiết
└── README.md                      # Hướng dẫn cài đặt và chạy (file này)
```

---

## 2. Cấu trúc dữ liệu kiểm thử (`test_data.csv`)

File `test_data.csv` tuân thủ quy ước chung của nhóm với các cột bắt buộc (`test_id`, `input`, `expected_result`) và các cột điều khiển kiểm tra tự động:

| Cột | Ý nghĩa |
| :--- | :--- |
| `test_id` | Mã định danh Test Case dùng chung toàn nhóm (`TC01` đến `TC05`) |
| `test_name` | Tên mô tả kịch bản kiểm thử |
| `input` | Từ khóa nhập vào ô tìm kiếm (`Ripple Glass Set`, `lamp`, `table`, `Laptop Dell XPS`, `""`) |
| `category` | Danh mục lọc (`All` hoặc `Lighting`) |
| `assertion_type` | Cơ chế đối chiếu kết quả (`exact_title`, `contains_title`, `no_results`, `min_count`) |
| `expected_result` | Kết quả mong đợi cần kiểm chứng trên giao diện |
| `expected_min_count` | Số lượng sản phẩm tối thiểu mong đợi |
| `description` | Diễn giải mục tiêu của từng trường hợp kiểm thử |

> **Ưu điểm mở rộng:** Khi muốn thêm `TC06`, `TC07`,..., kiểm thử viên chỉ cần thêm dòng mới vào `test_data.csv` mà **không cần sửa bất kỳ dòng code nào** trong `test_search_datadriven.py`.

---

## 3. Hướng dẫn cài đặt và chạy thực nghiệm

### Bước 1: Cài đặt môi trường Python (chỉ cần làm lần đầu)
Mở PowerShell / Terminal tại thư mục `04_DataDriven`:
```powershell
cd 04_DataDriven
pip install -r requirements.txt
python -m playwright install chromium
```

### Bước 2: Chạy bộ kiểm thử Data-Driven bằng `pytest`
```powershell
python -m pytest
# Hoặc chỉ định rõ file:
python -m pytest test_search_datadriven.py -v -s
```
Sau khi chạy xong:
- Kết quả từng test case (`PASS`/`FAIL`, kết quả thực tế, thời gian chạy) được xuất tự động ra file `pytest_execution_results.csv`.
- Ảnh chụp màn hình bằng chứng từng test case được lưu vào `04_DataDriven/evidence/evidence_TC0x_DataDriven.png` (và đồng bộ sang `../evidence/`).

### Bước 3: Chạy Demo trực quan trên trình duyệt (Headed Mode)
Để mở trình duyệt Chromium thực tế với tốc độ làm chậm (`slow_mo=800ms`) phục vụ thuyết trình trên lớp:
```powershell
python demo_visual.py
```

### Bước 4: Chạy Benchmark đo thời gian tự động qua 3 lượt ($A / T_{auto}$)
```powershell
python runner_benchmark.py
```
Kết quả đo lường sẽ tự động lưu vào:
- `04_DataDriven_Metrics.csv`
- `timing_metrics.json`

### Bước 5: Chạy thí nghiệm đổi 3 Locator và đo thời gian bảo trì ($R / T_{maint}$)
1. **Chạy khi 3 locator trên giao diện bị thay đổi (mô phỏng lỗi UI update):**
   ```powershell
   python experiment_broken_locators.py
   ```
2. **Chạy sau khi cập nhật 3 locator tại một nơi duy nhất (`locators.py` -> `STANDARD_LOCATORS`):**
   ```powershell
   python experiment_fixed_locators.py
   ```

