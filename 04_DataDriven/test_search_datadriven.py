"""
Data-Driven Automated Regression Test Suite (Member 4)
Framework: pytest + Playwright (Python)
Target Web: https://my-app-nextjs-xi.vercel.app/
Flow: Search Products (TC01 -> TC05 read dynamically from test_data.csv)
"""

import csv
import time
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import sync_playwright, Browser, Page

from locators import SearchPage, STANDARD_LOCATORS

BASE_DIR = Path(__file__).resolve().parent
CSV_DATA_PATH = BASE_DIR / "test_data.csv"
PYTEST_LOG_CSV = BASE_DIR / "pytest_execution_results.csv"
LOCAL_EVIDENCE_DIR = BASE_DIR / "evidence"
SHARED_EVIDENCE_DIR = BASE_DIR.parent / "evidence"


def load_test_data(csv_path: Path = CSV_DATA_PATH) -> list[dict[str, Any]]:
    """Đọc dữ liệu kiểm thử từ file CSV theo hướng Data-Driven."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu CSV tại: {csv_path}")

    rows: list[dict[str, Any]] = []
    with csv_path.open(mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "test_id": row["test_id"].strip(),
                    "test_name": row["test_name"].strip(),
                    "input": row["input"],
                    "category": row.get("category", "All").strip(),
                    "assertion_type": row["assertion_type"].strip(),
                    "expected_result": row["expected_result"].strip(),
                    "expected_min_count": int(row.get("expected_min_count", 0) or 0),
                    "description": row.get("description", "").strip(),
                }
            )
    return rows


# Lưu kết quả của phiên chạy pytest để xuất ra CSV sau khi hoàn tất suite
_SESSION_RESULTS: list[dict[str, Any]] = []


@pytest.fixture(scope="session")
def browser_instance():
    """Khởi tạo trình duyệt Chromium dùng chung cho toàn bộ Data-Driven Suite."""
    LOCAL_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    SHARED_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

    # Sau khi kết thúc toàn bộ các test cases, ghi nhận log kết quả ra file CSV
    if _SESSION_RESULTS:
        fieldnames = [
            "test_id",
            "test_name",
            "input",
            "category",
            "expected_result",
            "actual_result",
            "status",
            "duration_ms",
            "duration_sec",
        ]
        with PYTEST_LOG_CSV.open(mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(_SESSION_RESULTS)


@pytest.fixture(scope="function")
def search_page(browser_instance: Browser):
    """Tạo context và page mới cho mỗi dòng dữ liệu kiểm thử."""
    context = browser_instance.new_context(viewport={"width": 1280, "height": 800})
    page: Page = context.new_page()
    yield SearchPage(page, locators=STANDARD_LOCATORS)
    context.close()


@pytest.mark.parametrize(
    "test_case",
    load_test_data(),
    ids=lambda tc: f"{tc['test_id']}_{tc['test_name'].replace(' ', '_')}",
)
def test_search_products_data_driven(
    search_page: SearchPage, test_case: dict[str, Any]
) -> None:
    """Hàm kiểm thử Data-Driven duy nhất nhận tham số từ từng dòng của test_data.csv."""
    tc_id = test_case["test_id"]
    tc_name = test_case["test_name"]
    keyword = test_case["input"]
    category = test_case["category"]
    assertion_type = test_case["assertion_type"]
    expected_result = test_case["expected_result"]
    expected_min_count = test_case["expected_min_count"]

    start_time = time.perf_counter()
    status = "PASS"
    actual_result = ""

    try:
        # Bước 1: Mở trang chủ ứng dụng web
        search_page.navigate()

        # Bước 2: Thực hiện tìm kiếm với dữ liệu từ CSV
        search_page.perform_search(keyword=keyword, category=category)

        # Bước 3: Kiểm tra kết quả thực tế so với kết quả mong đợi (Assertion)
        passed, actual_result = search_page.verify_expected_result(
            assertion_type=assertion_type,
            expected_result=expected_result,
            expected_min_count=expected_min_count,
        )
        assert passed, f"Verification failed for {tc_id}: {actual_result}"

        # Bước 4: Chụp ảnh màn hình làm bằng chứng
        screenshot_name = f"evidence_{tc_id}_DataDriven.png"
        search_page.page.screenshot(
            path=str(LOCAL_EVIDENCE_DIR / screenshot_name), full_page=True
        )
        search_page.page.screenshot(
            path=str(SHARED_EVIDENCE_DIR / screenshot_name), full_page=True
        )

    except Exception as exc:
        status = "FAIL"
        actual_result = f"ERROR: {exc}"
        raise

    finally:
        duration_ms = round((time.perf_counter() - start_time) * 1000)
        duration_sec = round(duration_ms / 1000.0, 2)
        print(
            f"\n  [{tc_id}] {tc_name} | Input='{keyword}', Category='{category}' "
            f"-> Status: {status} | Actual: {actual_result} | Time: {duration_ms}ms ({duration_sec}s)"
        )
        _SESSION_RESULTS.append(
            {
                "test_id": tc_id,
                "test_name": tc_name,
                "input": keyword,
                "category": category,
                "expected_result": expected_result,
                "actual_result": actual_result,
                "status": status,
                "duration_ms": duration_ms,
                "duration_sec": duration_sec,
            }
        )

