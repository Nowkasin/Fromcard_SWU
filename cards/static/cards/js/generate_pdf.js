const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  let browser;
  try {
    const url = process.argv[2];
    let output = process.argv[3];

    if (!url) {
      console.error("❌ Missing URL argument");
      process.exit(1);
    }

    // default path เป็นโฟลเดอร์ node project
    if (!output) {
      output = path.join(__dirname, 'output.pdf');
    } else {
      output = path.resolve(output);
    }

    console.log("🌐 Opening URL:", url);
    console.log("📄 Output PDF path:", output);

    // ตรวจสอบว่า directory สำหรับ output มีอยู่
    const dir = path.dirname(output);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log("🗂 Created directory for PDF:", dir);
    }

    browser = await puppeteer.launch({
      headless: "new",
      args: ["--no-sandbox", "--disable-setuid-sandbox"]
      // executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" // สำหรับ Mac M1/M2
    });

    const page = await browser.newPage();

    console.log("⏳ Navigating to page...");
    await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: 60000
    });
    console.log("✅ Page loaded successfully");

    console.log("⏳ Generating PDF...");
    await page.pdf({
      path: output,
      format: 'A4',
      printBackground: true
    });
    console.log("✅ PDF generated successfully at", output);

    await browser.close();
    process.exit(0);

  } catch (err) {
    if (browser) {
      await browser.close();
    }
    console.error("❌ ERROR during PDF generation:");
    console.error(err);

    // เพิ่มรายละเอียด error สำหรับ debug
    if (err.message) console.error("Message:", err.message);
    if (err.stack) console.error("Stack:", err.stack);

    process.exit(1);
  }
})();