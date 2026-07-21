import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/arnavsrivastava/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/.pnpm/playwright@1.61.1/node_modules/playwright/index.js");

const [url, output, widthText, heightText] = process.argv.slice(2);
const width = Number(widthText);
const height = Number(heightText);
const browser = await chromium.launch({
  headless: true,
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
});
const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
const consoleErrors = [];
page.on("console", (message) => {
  if (message.type() === "error") consoleErrors.push(message.text());
});
page.on("pageerror", (error) => consoleErrors.push(String(error)));
await page.goto(url, { waitUntil: "load" });
await page.screenshot({ path: output, fullPage: false, animations: "disabled" });
await browser.close();
process.stdout.write(JSON.stringify({ width, height, consoleErrors }));
