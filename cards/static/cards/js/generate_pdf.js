const puppeteer = require('puppeteer');

(async () => {
  try {
    const url = process.argv[2];
    const output = process.argv[3];

    if (!url || !output) {
      console.error("❌ Missing arguments");
      process.exit(1);
    }

    console.log("🌐 Opening URL:", url);
    console.log("📄 Output:", output);

    const browser = await puppeteer.launch({
      headless: "new",
      args: ["--no-sandbox", "--disable-setuid-sandbox"]
    });

    const page = await browser.newPage();

    // 🔥 เพิ่ม timeout + debug
    await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: 60000
    });

    console.log("✅ Page loaded");

    await page.pdf({
      path: output,
      format: 'A4',
      printBackground: true
    });

    console.log("✅ PDF generated");

    await browser.close();
    process.exit(0);

  } catch (err) {
    console.error("❌ ERROR:", err);
    process.exit(1);
  }
})();