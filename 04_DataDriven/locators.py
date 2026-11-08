"""
Centralized Locator Repository & Page Object for Search Flow (Data-Driven Testing)
Target Application: https://my-app-nextjs-xi.vercel.app/
Repository: https://github.com/pthaok6/LabFer202
"""

from dataclasses import dataclass
from playwright.sync_api import Page, expect


BASE_URL = "https://my-app-nextjs-xi.vercel.app/"


@dataclass(frozen=True)
class SearchLocators:
    """Centralized UI selectors for the Product Search flow.
    When UI locators change, only this single configuration needs to be updated.
    """
    search_input: str
    category_select: str
    search_button: str
    product_list: str
    product_heading: str
    no_results: str


# Bộ Locator chuẩn hiện tại trên giao diện (Sau khi đồng bộ / bảo trì)
STANDARD_LOCATORS = SearchLocators(
    search_input='[data-testid="search-input"]',
    category_select='[data-testid="category-select"]',
    search_button='[data-testid="btn-search"]',
    product_list='[data-testid="product-list"]',
    product_heading='[data-testid="product-list"] h3',
    no_results='[data-testid="no-results"]',
)

# Bộ 3 Locator giả lập bị thay đổi trên giao diện (Phục vụ thí nghiệm đo thời gian sửa R)
BROKEN_LOCATORS = SearchLocators(
    search_input='input.legacy-search-field',          # Locator 1 bị đổi
    category_select='select#old-filter-category',      # Locator 2 bị đổi
    search_button='button.btn-submit-search-v1',       # Locator 3 bị đổi
    product_list='[data-testid="product-list"]',
    product_heading='[data-testid="product-list"] h3',
    no_results='[data-testid="no-results"]',
)


class SearchPage:
    """Page Object encapsulating product search actions and result verification."""

    def __init__(self, page: Page, locators: SearchLocators = STANDARD_LOCATORS):
        self.page = page
        self.locators = locators

    def navigate(self) -> None:
        self.page.goto(BASE_URL, wait_until="networkidle")

    def perform_search(self, keyword: str, category: str, timeout: float = 5000) -> None:
        # 1. Nhập từ khóa tìm kiếm
        search_box = self.page.locator(self.locators.search_input)
        search_box.fill(keyword, timeout=timeout)

        # 2. Chọn danh mục sản phẩm
        cat_select = self.page.locator(self.locators.category_select)
        if not category or category.strip().lower() == "all":
            cat_select.select_option(value="", timeout=timeout)
        else:
            cat_select.select_option(label=category.strip(), timeout=timeout)

        # 3. Bấm nút Search
        btn = self.page.locator(self.locators.search_button)
        btn.click(timeout=timeout)
        self.page.wait_for_load_state("networkidle")

    def verify_expected_result(
        self,
        assertion_type: str,
        expected_result: str,
        expected_min_count: int = 0,
    ) -> tuple[bool, str]:
        """Kiểm tra kết quả thực tế so với kết quả mong đợi từ file CSV.
        Trả về (passed: bool, actual_result: str).
        """
        if assertion_type == "exact_title":
            heading = self.page.locator(
                self.locators.product_heading, has_text=expected_result
            )
            expect(heading).to_be_visible(timeout=5000)
            expect(heading).to_have_text(expected_result, timeout=5000)
            actual_text = heading.first.text_content() or ""
            return True, f"Found exact product: '{actual_text.strip()}'"

        elif assertion_type == "contains_title":
            heading = self.page.locator(
                self.locators.product_heading, has_text=expected_result
            )
            expect(heading).to_be_visible(timeout=5000)
            actual_text = heading.first.text_content() or ""
            assert expected_result.lower() in actual_text.lower(), (
                f"Expected '{expected_result}' in '{actual_text}'"
            )
            return True, f"Found matching product: '{actual_text.strip()}'"

        elif assertion_type == "no_results":
            no_res = self.page.locator(self.locators.no_results)
            expect(no_res).to_be_visible(timeout=5000)
            expect(no_res).to_have_text(expected_result, timeout=5000)
            actual_text = no_res.text_content() or ""
            return True, f"Displayed message: '{actual_text.strip()}'"

        elif assertion_type == "min_count":
            product_list = self.page.locator(self.locators.product_list)
            expect(product_list).to_be_visible(timeout=5000)
            headings = self.page.locator(self.locators.product_heading)
            count = headings.count()
            assert count >= expected_min_count, (
                f"Expected at least {expected_min_count} products, but got {count}"
            )
            return True, f"{count} products displayed (expected >= {expected_min_count})"

        else:
            raise ValueError(f"Unsupported assertion_type in CSV: {assertion_type}")

