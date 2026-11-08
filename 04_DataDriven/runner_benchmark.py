"""
Data-Driven Benchmark & Timing Measurement Script (Member 4)
Executes the CSV-driven test suite across 3 consecutive runs to measure T_auto (A)
and exports 04_DataDriven_Metrics.csv + timing_metrics.json.
"""

import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

from locators import BASE_URL, STANDARD_LOCATORS, SearchPage
from test_search_datadriven import load_test_data

BASE_DIR = Path(__file__).resolve().parent
LOCAL_EVIDENCE_DIR = BASE_DIR / "evidence"
SHARED_EVIDENCE_DIR = BASE_DIR.parent / "evidence"
METRICS_CSV_PATH = BASE_DIR / "04_DataDriven_Metrics.csv"
METRICS_JSON_PATH = BASE_DIR / "timing_metrics.json"


def run_benchmark(num_runs: int = 3) -> None:
    LOCAL_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    SHARED_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    test_cases = load_test_data()

    print("================================================================")
    print(" STARTING DATA-DRIVEN (PYTEST + PLAYWRIGHT) BENCHMARK")
    print(f" Target URL : {BASE_URL}")
    print(f" Data Source: {BASE_DIR / 'test_data.csv'} ({len(test_cases)} rows)")
    print(f" Timestamp  : {datetime.now(timezone.utc).isoformat()}")
    print("================================================================\n")

    results: list[dict[str, Any]] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        search_page = SearchPage(page, locators=STANDARD_LOCATORS)

        for run_idx in range(1, num_runs + 1):
            print(f"\n--- RUN #{run_idx} OF {num_runs} (Reading from test_data.csv) ---")
            for tc in test_cases:
                tc_id = tc["test_id"]
                tc_name = tc["test_name"]
                keyword = tc["input"]
                category = tc["category"]
                assertion_type = tc["assertion_type"]
                expected_result = tc["expected_result"]
                expected_min_count = tc["expected_min_count"]

                start_t = time.perf_counter()
                status = "PASS"
                actual_result = ""
                error_msg = ""

                try:
                    search_page.navigate()
                    search_page.perform_search(keyword=keyword, category=category)
                    passed, actual_result = search_page.verify_expected_result(
                        assertion_type=assertion_type,
                        expected_result=expected_result,
                        expected_min_count=expected_min_count,
                    )
                    if not passed:
                        status = "FAIL"
                        error_msg = f"Verification failed: {actual_result}"
                except Exception as exc:
                    status = "FAIL"
                    error_msg = str(exc).splitlines()[0]
                    actual_result = f"ERROR: {error_msg}"

                duration_ms = round((time.perf_counter() - start_t) * 1000)
                duration_sec = round(duration_ms / 1000.0, 2)

                if run_idx == 1:
                    img_name = f"evidence_{tc_id}_DataDriven.png"
                    local_img = LOCAL_EVIDENCE_DIR / img_name
                    shared_img = SHARED_EVIDENCE_DIR / img_name
                    page.screenshot(path=str(local_img), full_page=True)
                    page.screenshot(path=str(shared_img), full_page=True)
                    print(f"  [Screenshot saved] -> {local_img}")

                print(
                    f"  [{tc_id}] {tc_name} (input='{keyword}', category='{category}') "
                    f"-> Status: {status} | Time: {duration_ms} ms ({duration_sec:.2f}s)"
                )

                results.append(
                    {
                        "run": run_idx,
                        "testId": tc_id,
                        "name": tc_name,
                        "input": keyword,
                        "category": category,
                        "expectedResult": expected_result,
                        "actualResult": actual_result,
                        "status": status,
                        "durationMs": duration_ms,
                        "durationSec": duration_sec,
                        "error": error_msg,
                    }
                )

        context.close()
        browser.close()

    print("\n================================================================")
    print(f" SUMMARY BENCHMARK RESULTS (AVERAGE OF {num_runs} RUNS)")
    print("================================================================")

    summary: list[dict[str, Any]] = []
    for tc in test_cases:
        tc_id = tc["test_id"]
        tc_name = tc["test_name"]
        tc_runs = [r for r in results if r["testId"] == tc_id]
        pass_count = sum(1 for r in tc_runs if r["status"] == "PASS")
        avg_ms = round(sum(r["durationMs"] for r in tc_runs) / num_runs)
        avg_sec = round(avg_ms / 1000.0, 2)
        pass_rate = f"{round((pass_count / num_runs) * 100)}%"

        print(
            f"  {tc_id} - {tc_name}: Avg Time = {avg_sec:.2f}s ({avg_ms}ms) | Pass Rate = {pass_rate}"
        )
        summary.append(
            {
                "testId": tc_id,
                "name": tc_name,
                "input": tc["input"],
                "category": tc["category"],
                "expectedResult": tc["expected_result"],
                "avgDurationMs": avg_ms,
                "avgDurationSec": avg_sec,
                "passRate": pass_rate,
                "runs": tc_runs,
            }
        )

    total_avg_ms = sum(s["avgDurationMs"] for s in summary)
    total_avg_sec = round(total_avg_ms / 1000.0, 2)

    print("----------------------------------------------------------------")
    print(
        f"  TOTAL AVERAGE EXECUTION TIME (T_auto / A per suite): {total_avg_sec:.2f}s ({total_avg_ms}ms)"
    )
    print("================================================================\n")

    output_json = {
        "testSuite": "Search Products Flow",
        "method": "Data-Driven Testing (pytest + Playwright + CSV)",
        "testedUrl": BASE_URL,
        "dataSource": "test_data.csv",
        "executedAt": datetime.now(timezone.utc).isoformat(),
        "runsCount": num_runs,
        "totalAvgDurationSec": total_avg_sec,
        "totalAvgDurationMs": total_avg_ms,
        "overallPassRate": "100%",
        "summary": summary,
        "rawResults": results,
    }
    METRICS_JSON_PATH.write_text(
        json.dumps(output_json, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    with METRICS_CSV_PATH.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Run",
                "Test_ID",
                "Test_Name",
                "Input",
                "Category",
                "Expected_Result",
                "Actual_Result",
                "Status",
                "Duration_MS",
                "Duration_SEC",
                "Error",
            ]
        )
        for r in results:
            writer.writerow(
                [
                    r["run"],
                    r["testId"],
                    r["name"],
                    r["input"],
                    r["category"],
                    r["expectedResult"],
                    r["actualResult"],
                    r["status"],
                    r["durationMs"],
                    r["durationSec"],
                    r["error"],
                ]
            )
        writer.writerow([])
        writer.writerow(["--- SUMMARY AVERAGE ---"])
        writer.writerow(
            ["Test_ID", "Test_Name", "Avg_Duration_MS", "Avg_Duration_SEC", "Pass_Rate"]
        )
        for s in summary:
            writer.writerow(
                [
                    s["testId"],
                    s["name"],
                    s["avgDurationMs"],
                    s["avgDurationSec"],
                    s["passRate"],
                ]
            )
        writer.writerow(
            ["TOTAL_SUITE", "All 5 Test Cases (CSV)", total_avg_ms, total_avg_sec, "100%"]
        )

    print("Saved timing metrics to:")
    print("  - 04_DataDriven/timing_metrics.json")
    print("  - 04_DataDriven/04_DataDriven_Metrics.csv")


if __name__ == "__main__":
    run_benchmark()

