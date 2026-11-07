// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Capture & Replay Test Suite for Search Flow
 * Target Web: https://my-app-nextjs-xi.vercel.app/
 * Test Flow: Search Products (TC01 -> TC05)
 * Recorded via Playwright Codegen & refined with Assertions
 */

const BASE_URL = 'https://my-app-nextjs-xi.vercel.app/';

test.describe('Search Products - Capture and Replay Test Suite', () => {

  test.beforeEach(async ({ page }) => {
    // Navigate to homepage before each test
    await page.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
  });

  test('TC01 - Exact Name Search', async ({ page }) => {
    // 1. Locate search box & fill exact name
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.click();
    await searchInput.fill('Ripple Glass Set');

    // 2. Click Search button
    await page.locator('[data-testid="btn-search"]').click();

    // 3. Assert: Exactly "Ripple Glass Set" is displayed in product list
    const productHeading = page.locator('[data-testid="product-list"] h3', { hasText: 'Ripple Glass Set' });
    await expect(productHeading).toBeVisible();
    await expect(productHeading).toHaveText('Ripple Glass Set');
  });

  test('TC02 - Partial Name Search (Case-insensitive)', async ({ page }) => {
    // 1. Fill partial keyword with lowercase
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('lamp');

    // 2. Click Search button
    await page.locator('[data-testid="btn-search"]').click();

    // 3. Assert: "Mori Table Lamp" is found
    const productHeading = page.locator('[data-testid="product-list"] h3', { hasText: 'Mori Table Lamp' });
    await expect(productHeading).toBeVisible();
    await expect(productHeading).toContainText('Lamp');
  });

  test('TC03 - Search with Keyword and Category Filter', async ({ page }) => {
    // 1. Fill keyword "table"
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('table');

    // 2. Select Category "Lighting"
    const categorySelect = page.locator('[data-testid="category-select"]');
    await categorySelect.selectOption({ label: 'Lighting' });

    // 3. Click Search button
    await page.locator('[data-testid="btn-search"]').click();

    // 4. Assert: "Mori Table Lamp" is returned (matches "table" inside Lighting)
    const productHeading = page.locator('[data-testid="product-list"] h3', { hasText: 'Mori Table Lamp' });
    await expect(productHeading).toBeVisible();
  });

  test('TC04 - Search Non-Existent Product (No Results Found)', async ({ page }) => {
    // 1. Fill a non-existent keyword
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('Laptop Dell XPS');

    // 2. Click Search button
    await page.locator('[data-testid="btn-search"]').click();

    // 3. Assert: "No products found." message is displayed
    const noResultsMessage = page.locator('[data-testid="no-results"]');
    await expect(noResultsMessage).toBeVisible();
    await expect(noResultsMessage).toHaveText('No products found.');
  });

  test('TC05 - Empty Keyword and All Categories (Show All Products)', async ({ page }) => {
    // 1. Clear search input
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('');

    // 2. Select All category
    const categorySelect = page.locator('[data-testid="category-select"]');
    await categorySelect.selectOption({ value: '' });

    // 3. Click Search button
    await page.locator('[data-testid="btn-search"]').click();

    // 4. Assert: Product list contains all 6 products
    const productCards = page.locator('[data-testid="product-list"] article, [data-testid="product-list"] > div');
    await expect(page.locator('[data-testid="product-list"]')).toBeVisible();
    const count = await productCards.count();
    expect(count).toBeGreaterThanOrEqual(6);
  });

});

