// @ts-check
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://my-app-nextjs-xi.vercel.app/';

async function testFixedLocators() {
  console.log('================================================================');
  console.log(' EXPERIMENT: TESTING AFTER FIXING 3 LOCATORS (MAINTENANCE VERIFICATION)');
  console.log(' Demonstrating script recovery after updating robust selectors');
  console.log('================================================================\n');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();

  await page.goto(BASE_URL, { waitUntil: 'networkidle' });

  // 1. Fixed Locator 1: Search Input (Updated to [data-testid="search-input"])
  console.log('--- TEST STEP 1: Using fixed robust locator for Search Input ---');
  console.log('Fixed locator: [data-testid="search-input"]');
  const t1 = performance.now();
  const input = page.locator('[data-testid="search-input"]');
  await input.fill('Mori Table Lamp');
  console.log(`  -> Status: PASS | Step Execution Time: ${Math.round(performance.now() - t1)}ms`);

  // 2. Fixed Locator 2: Category Dropdown (Updated to [data-testid="category-select"])
  console.log('\n--- TEST STEP 2: Using fixed robust locator for Category Dropdown ---');
  console.log('Fixed locator: [data-testid="category-select"]');
  const t2 = performance.now();
  const select = page.locator('[data-testid="category-select"]');
  await select.selectOption({ label: 'Lighting' });
  console.log(`  -> Status: PASS | Step Execution Time: ${Math.round(performance.now() - t2)}ms`);

  // 3. Fixed Locator 3: Search Button (Updated to [data-testid="btn-search"])
  console.log('\n--- TEST STEP 3: Using fixed robust locator for Submit Button ---');
  console.log('Fixed locator: [data-testid="btn-search"]');
  const t3 = performance.now();
  const button = page.locator('[data-testid="btn-search"]');
  await button.click();
  await page.waitForLoadState('networkidle');
  console.log(`  -> Status: PASS | Step Execution Time: ${Math.round(performance.now() - t3)}ms`);

  // Verification Assertion
  const resultHeading = page.locator('[data-testid="product-list"] h3', { hasText: 'Mori Table Lamp' });
  await resultHeading.waitFor({ state: 'visible', timeout: 5000 });
  const isFound = await resultHeading.isVisible();
  console.log('\n  -> Product verification result visible:', isFound);

  await browser.close();

  console.log('\n================================================================');
  console.log(' RESULT: 100% Steps Passed after updating locators.');
  console.log(' Maintenance effort verified and documented successfully.');
  console.log('================================================================');
}

testFixedLocators().catch(console.error);

