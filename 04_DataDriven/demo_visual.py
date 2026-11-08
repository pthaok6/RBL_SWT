"""
Visual Demo Runner for Data-Driven Testing (Member 4)
Opens a visible Chromium browser with slow_mo=800ms and executes TC01 -> TC05
directly from test_data.csv for live presentation.
"""

from playwright.sync_api import sync_playwright

from locators import STANDARD_LOCATORS, SearchPage
from test_search_datadriven import load_test_data


def run_visual_demo() -> None:
    test_cases = load_test_data()
    print("================================================================")
    print(" STARTING DATA-DRIVEN VISUAL DEMO (HEADED MODE, SLOW_MO=800ms)")
    print(f" Loaded {len(test_cases)} test cases from test_data.csv")
    print("================================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        search_page = SearchPage(page, locators=STANDARD_LOCATORS)

        for tc in test_cases:
            print(f"--> Running [{tc['test_id']}] {tc['test_name']}...")
            print(
                f"    CSV Input: q='{tc['input']}', category='{tc['category']}' | Expected: {tc['expected_result']}"
            )
            search_page.navigate()
            search_page.perform_search(keyword=tc["input"], category=tc["category"])
            passed, actual_msg = search_page.verify_expected_result(
                assertion_type=tc["assertion_type"],
                expected_result=tc["expected_result"],
                expected_min_count=tc["expected_min_count"],
            )
            print(f"    Result   : {'PASS' if passed else 'FAIL'} ({actual_msg})\n")

        context.close()
        browser.close()

    print("================================================================")
    print(" DATA-DRIVEN VISUAL DEMO COMPLETED SUCCESSFULLY!")
    print("================================================================")


if __name__ == "__main__":
    run_visual_demo()

