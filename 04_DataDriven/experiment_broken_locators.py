"""
Experiment Part 1: Simulating 3 UI Locator Changes in Data-Driven Testing (Member 4)
Demonstrates failure when 3 UI selectors change on the web interface,
and highlights how centralized locators (locators.py) isolate the impact to 1 single file.
"""

from playwright.sync_api import sync_playwright

from locators import BASE_URL, BROKEN_LOCATORS


def run_broken_locators_experiment() -> None:
    print("================================================================")
    print(" EXPERIMENT (DATA-DRIVEN): TESTING WITH 3 CHANGED UI LOCATORS")
    print(" Central Locator Config: locators.py -> BROKEN_LOCATORS")
    print("================================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        page.goto(BASE_URL, wait_until="networkidle")

        # 1. Changed Locator 1: Search Input
        print("--- TEST STEP 1: Search Input Locator in locators.py ---")
        print(f"Outdated locator: {BROKEN_LOCATORS.search_input}")
        try:
            page.locator(BROKEN_LOCATORS.search_input).fill(
                "Ripple Glass Set", timeout=3000
            )
            print("  -> Status: UNEXPECTED PASS")
        except Exception as err:
            first_line = str(err).splitlines()[0]
            print("  -> Status: FAILED AS EXPECTED!")
            print(f"  -> Error Message: {type(err).__name__} - {first_line}")

        # 2. Changed Locator 2: Category Select Dropdown
        print("\n--- TEST STEP 2: Category Dropdown Locator in locators.py ---")
        print(f"Outdated locator: {BROKEN_LOCATORS.category_select}")
        try:
            page.locator(BROKEN_LOCATORS.category_select).select_option(
                label="Lighting", timeout=3000
            )
            print("  -> Status: UNEXPECTED PASS")
        except Exception as err:
            first_line = str(err).splitlines()[0]
            print("  -> Status: FAILED AS EXPECTED!")
            print(f"  -> Error Message: {type(err).__name__} - {first_line}")

        # 3. Changed Locator 3: Search Submit Button
        print("\n--- TEST STEP 3: Search Button Locator in locators.py ---")
        print(f"Outdated locator: {BROKEN_LOCATORS.search_button}")
        try:
            page.locator(BROKEN_LOCATORS.search_button).click(timeout=3000)
            print("  -> Status: UNEXPECTED PASS")
        except Exception as err:
            first_line = str(err).splitlines()[0]
            print("  -> Status: FAILED AS EXPECTED!")
            print(f"  -> Error Message: {type(err).__name__} - {first_line}")

        context.close()
        browser.close()

    print("\n================================================================")
    print(" CONCLUSION (BEFORE MAINTENANCE):")
    print(" - All 3 interactions failed due to TimeoutError (3000ms exceeded).")
    print(" - ADVANTAGE OF DATA-DRIVEN + CENTRALIZED LOCATORS:")
    print("   Instead of editing 5 separate test cases (15 selector lines),")
    print("   we only need to update 3 attributes in 1 place (locators.py)")
    print("   without touching test_data.csv or test_search_datadriven.py!")
    print("================================================================")


if __name__ == "__main__":
    run_broken_locators_experiment()

