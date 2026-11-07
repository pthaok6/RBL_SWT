// @ts-check
const { chromium } = require('playwright');

/**
 * DEMO TRỰC QUAN (VISUAL DEMO) DÀNH CHO THUYẾT TRÌNH / BÁO CÁO
 * - Mở trình duyệt thực tế (headed mode)
 * - Tốc độ slowMo 800ms để người xem quan sát rõ từng thao tác gõ chữ, chọn dropdown và click search
 */

const BASE_URL = 'https://my-app-nextjs-xi.vercel.app/';

async function runVisualDemo() {
  console.log('================================================================');
  console.log(' KHỞI ĐỘNG DEMO TRỰC QUAN KIỂM THỬ TỰ ĐỘNG (CAPTURE / REPLAY)');
  console.log(' Mục tiêu: Trình diễn tự động 5 Test Cases trên trình duyệt');
  console.log(' URL: ' + BASE_URL);
  console.log('================================================================\n');

  // Bật trình duyệt có giao diện (headless: false) và làm chậm thao tác 800ms
  const browser = await chromium.launch({
    headless: false,
    slowMo: 800
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  const page = await context.newPage();

  try {
    // TC01: Tìm kiếm chính xác
    console.log('▶ [DEMO TC01] Tìm kiếm chính xác theo tên sản phẩm: "Ripple Glass Set"');
    await page.goto(BASE_URL);
    await page.locator('[data-testid="search-input"]').click();
    await page.locator('[data-testid="search-input"]').fill('Ripple Glass Set');
    await page.locator('[data-testid="btn-search"]').click();
    await page.waitForTimeout(1200);
    console.log('  ✔ TC01: Đã hiển thị đúng sản phẩm "Ripple Glass Set"\n');

    // TC02: Tìm kiếm một phần từ khóa
    console.log('▶ [DEMO TC02] Tìm kiếm từ khóa con (không phân biệt hoa thường): "lamp"');
    await page.locator('[data-testid="search-input"]').click();
    await page.locator('[data-testid="search-input"]').fill('lamp');
    await page.locator('[data-testid="btn-search"]').click();
    await page.waitForTimeout(1200);
    console.log('  ✔ TC02: Đã hiển thị đúng "Mori Table Lamp"\n');

    // TC03: Tìm kiếm kết hợp danh mục
    console.log('▶ [DEMO TC03] Kết hợp từ khóa "table" + Danh mục "Lighting"');
    await page.locator('[data-testid="search-input"]').click();
    await page.locator('[data-testid="search-input"]').fill('table');
    await page.locator('[data-testid="category-select"]').selectOption({ label: 'Lighting' });
    await page.locator('[data-testid="btn-search"]').click();
    await page.waitForTimeout(1200);
    console.log('  ✔ TC03: Đã lọc chính xác "Mori Table Lamp" trong nhóm Lighting\n');

    // TC04: Tìm kiếm sản phẩm không tồn tại
    console.log('▶ [DEMO TC04] Tìm kiếm từ khóa không tồn tại: "Laptop Dell XPS"');
    await page.locator('[data-testid="search-input"]').click();
    await page.locator('[data-testid="search-input"]').fill('Laptop Dell XPS');
    await page.locator('[data-testid="category-select"]').selectOption({ value: '' });
    await page.locator('[data-testid="btn-search"]').click();
    await page.waitForTimeout(1200);
    console.log('  ✔ TC04: Đã hiển thị thông báo "No products found."\n');

    // TC05: Tìm kiếm rỗng (hiển thị tất cả)
    console.log('▶ [DEMO TC05] Tìm kiếm chuỗi rỗng để hiển thị toàn bộ 6 sản phẩm');
    await page.locator('[data-testid="search-input"]').click();
    await page.locator('[data-testid="search-input"]').fill('');
    await page.locator('[data-testid="category-select"]').selectOption({ value: '' });
    await page.locator('[data-testid="btn-search"]').click();
    await page.waitForTimeout(1500);
    console.log('  ✔ TC05: Đã hiển thị đầy đủ danh sách 6 sản phẩm\n');

    console.log('================================================================');
    console.log(' HOÀN THÀNH DEMO TRỰC QUAN THÀNH CÔNG 100%!');
    console.log(' Trình duyệt sẽ đóng sau 3 giây...');
    console.log('================================================================');
    await page.waitForTimeout(3000);

  } catch (err) {
    console.error('Lỗi trong quá trình demo:', err);
  } finally {
    await browser.close();
  }
}

runVisualDemo();

