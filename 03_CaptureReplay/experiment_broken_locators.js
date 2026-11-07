// @ts-check
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://my-app-nextjs-xi.vercel.app/';

async function testBrokenLocators() {
  console.log('================================================================');
  console.log(' EXPERIMENT: TESTING WITH 3 CHANGED / OUTDATED LOCATORS');
  console.log(' Demonstrating Capture/Replay script fragility when UI changes');
  console.log('================================================================\n');

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await context.newPage();

  await page.goto(BASE_URL, { waitUntil: 'networkidle' });

  // 1. Changed Locator 1: Search Input (Simulating UI update from old CSS class to new structure)
  console.log('--- TEST STEP 1: Using outdated locator for Search Input ---');
  console.log('Outdated locator: input.legacy-search-field');
  try {
    const input = page.locator('input.legacy-search-field');
    await input.fill('Ripple Glass Set', { timeout: 3000 });
    console.log('  -> Status: UNEXPECTED PASS');
  } catch (err) {
    console.log('  -> Status: FAILED AS EXPECTED!');
    console.log('  -> Error Message:', err.name + ' - ' + err.message.split('\n')[0]);
  }

  // 2. Changed Locator 2: Category Dropdown (Simulating select element id change)
  console.log('\n--- TEST STEP 2: Using outdated locator for Category Dropdown ---');
  console.log('Outdated locator: select#old-filter-category');
  try {
    const select = page.locator('select#old-filter-category');
    await select.selectOption({ label: 'Lighting' }, { timeout: 3000 });
    console.log('  -> Status: UNEXPECTED PASS');
  } catch (err) {
    console.log('  -> Status: FAILED AS EXPECTED!');
    console.log('  -> Error Message:', err.name + ' - ' + err.message.split('\n')[0]);
  }

  // 3. Changed Locator 3: Search Button (Simulating button class rename)
  console.log('\n--- TEST STEP 3: Using outdated locator for Submit Button ---');
  console.log('Outdated locator: button.btn-submit-search-v1');
  try {
    const button = page.locator('button.btn-submit-search-v1');
    await button.click({ timeout: 3000 });
    console.log('  -> Status: UNEXPECTED PASS');
  } catch (err) {
    console.log('  -> Status: FAILED AS EXPECTED!');
    console.log('  -> Error Message:', err.name + ' - ' + err.message.split('\n')[0]);
  }

  await browser.close();
  console.log('\n================================================================');
  console.log(' CONCLUSION: When 3 locators changed on the UI, 100% of related');
  console.log(' recorded steps failed due to element not found timeouts.');
  console.log(' Script requires manual inspection and re-recording/updating.');
  console.log('================================================================');
}

testBrokenLocators().catch(console.error);

