const { chromium, firefox } = require("playwright");
const flags = "flag{flag_flag_flag_flag}";
const encodedFlagss = Buffer.from(flags).toString("base64");

async function getBrowserContext() {
  const browserArgs = {
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  };

  const browser = await chromium.launch(browserArgs);
  const context = await browser.newContext();
  return context;
}

module.exports = {
  async visitUrl(urlToVisit, encodedCreds) {
    const context = await getBrowserContext();

    try {
      const page = await context.newPage();

      await context.addCookies([
        {
          name: "uuid",
          value: encodedCreds,
          domain: new URL(urlToVisit).hostname,
          path: "/",
          expires: Math.floor(Date.now() / 1000) + 60 * 60,
          httpOnly: false,
          secure: urlToVisit.startsWith("https"),
        },
        {
          name: "flag",
          value: encodedFlagss,
          domain: new URL(urlToVisit).hostname,
          path: "/",
          expires: Math.floor(Date.now() / 1000) + 60 * 60,
          httpOnly: false,
          secure: urlToVisit.startsWith("https"),
        },
      ]);

      console.log(
        `Bot visiting: ${urlToVisit} with uuid cookie: ${encodedCreds}`
      );
      await page.goto(urlToVisit, { waitUntil: "load", timeout: 10000 });

      await page.waitForTimeout(10000);

      console.log("Browser closed.");
      return true;
    } catch (err) {
      console.error("Error during bot execution:", err);
      return false;
    } finally {
      await context.browser().close();
    }
  },
};
