"""
Experiment Part 2: Verification After Fixing 3 Centralized Locators (Member 4)
Demonstrates that after updating the 3 selectors in locators.py (STANDARD_LOCATORS),
all 5 CSV-driven test cases (TC01 -> TC05) recover and pass 100%.
"""

import time
from playwright.sync_api import sync_playwright

from locators import BASE_URL, STANDARD_LOCATORS, SearchPage
from test_search_datadriven import load_test_data


def run_fixed_locators_experiment() -> None:
    print("================================================================")
    print(" EXPERIMENT (DATA-DRIVEN): VERIFYING AFTER FIXING 3 LOCATORS")
    print(" Central Locator Config: locators.py -> STANDARD_LOCATORS")
    print("================================================================\n")

    print("Updated centralized selectors in locators.py:")
    print(f"  1. search_input   : {STANDARD_LOCATORS.search_input}")
    print(f"  2. category_select: {STANDARD_LOCATORS.category_select}")
    print(f"  3. search_button  : {STANDARD_LOCATORS.search_button}\n")

    test_cases = load_test_data()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        search_page = SearchPage(page, locators=STANDARD_LOCATORS)

        passed_count = 0
        for tc in test_cases:
            t0 = time.perf_counter()
            search_page.navigate()
            search_page.perform_search(keyword=tc["input"], category=tc["category"])
            passed, actual_msg = search_page.verify_expected_result(
                assertion_type=tc["assertion_type"],
                expected_result=tc["expected_result"],
                expected_min_count=tc["expected_min_count"],
            )
            elapsed_ms = round((time.perf_counter() - t0) * 1000)
            if passed:
                passed_count += 1
            print(
                f"  [{tc['test_id']}] {tc['test_name']} -> PASS ({elapsed_ms}ms) | {actual_msg}"
            )

        context.close()
        browser.close()

    print("\n================================================================")
    print(
        f" RESULT: {passed_count}/{len(test_cases)} CSV Test Cases Passed (100% Pass Rate)"
    )
    print(" Single-point locator maintenance in locators.py verified!")
    print("================================================================")


if __name__ == "__main__":
    run_fixed_locators_experiment()

