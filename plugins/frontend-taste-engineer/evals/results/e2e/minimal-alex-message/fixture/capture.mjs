import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import path from "node:path";

const root = process.cwd();
const output = path.join(root, "artifacts", "screenshots");
const chromePath = process.env.CHROME_PATH || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const chromeProfile = await mkdtemp(path.join(tmpdir(), "alex-capture-"));

await mkdir(output, { recursive: true });

const server = spawn("python3", ["-m", "http.server", "4173", "--directory", "dist"], {
  cwd: root,
  stdio: "ignore",
});

const chrome = spawn(chromePath, [
  "--headless=new",
  "--hide-scrollbars",
  "--disable-gpu",
  "--no-sandbox",
  "--remote-debugging-port=0",
  `--user-data-dir=${chromeProfile}`,
  "about:blank",
], { stdio: ["ignore", "ignore", "pipe"] });

function waitForDebuggerUrl(child) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error("Chrome debugging endpoint timed out")), 8000);

    child.stderr.setEncoding("utf8");
    child.stderr.on("data", chunk => {
      const match = chunk.match(/DevTools listening on (ws:\/\/[^\s]+)/);
      if (!match) return;
      clearTimeout(timeout);
      resolve(match[1]);
    });

    child.once("exit", code => {
      clearTimeout(timeout);
      reject(new Error(`Chrome exited before capture with code ${code}`));
    });
  });
}

async function connectToPage(browserDebuggerUrl) {
  const debuggerUrl = new URL(browserDebuggerUrl);
  const targets = await fetch(`http://${debuggerUrl.host}/json/list`).then(response => response.json());
  const pageTarget = targets.find(target => target.type === "page");
  if (!pageTarget) throw new Error("Chrome did not expose a page target");

  const socket = new WebSocket(pageTarget.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    socket.addEventListener("open", resolve, { once: true });
    socket.addEventListener("error", reject, { once: true });
  });

  let requestId = 0;
  const pending = new Map();
  const eventWaiters = new Map();
  const eventListeners = new Map();

  socket.addEventListener("message", event => {
    const message = JSON.parse(event.data);

    if (message.id) {
      const waiter = pending.get(message.id);
      if (!waiter) return;
      pending.delete(message.id);
      if (message.error) waiter.reject(new Error(message.error.message));
      else waiter.resolve(message.result);
      return;
    }

    const waiters = eventWaiters.get(message.method);
    if (waiters?.length) {
      eventWaiters.delete(message.method);
      waiters.forEach(resolve => resolve(message.params));
    }

    const listeners = eventListeners.get(message.method);
    listeners?.forEach(listener => listener(message.params));
  });

  const call = (method, params = {}) => new Promise((resolve, reject) => {
    const id = ++requestId;
    pending.set(id, { resolve, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });

  const once = method => new Promise(resolve => {
    const waiters = eventWaiters.get(method) || [];
    waiters.push(resolve);
    eventWaiters.set(method, waiters);
  });

  const on = (method, listener) => {
    const listeners = eventListeners.get(method) || [];
    listeners.push(listener);
    eventListeners.set(method, listeners);
  };

  return { call, once, on, close: () => socket.close() };
}

const browserDebuggerUrlPromise = waitForDebuggerUrl(chrome);
await new Promise(resolve => setTimeout(resolve, 700));

try {
  const browserDebuggerUrl = await browserDebuggerUrlPromise;
  const client = await connectToPage(browserDebuggerUrl);

  await client.call("Page.enable");
  await client.call("Runtime.enable");
  await client.call("Log.enable");
  await client.call("Network.enable");

  const runtimeErrors = [];
  const failedRequests = [];

  client.on("Runtime.exceptionThrown", event => {
    runtimeErrors.push(event.exceptionDetails.text);
  });
  client.on("Log.entryAdded", event => {
    if (event.entry.level === "error") runtimeErrors.push(event.entry.text);
  });
  client.on("Network.responseReceived", event => {
    if (event.response.status >= 400) {
      failedRequests.push({ status: event.response.status, url: event.response.url });
    }
  });

  for (const [name, width, height] of [
    ["desktop", 1440, 1000],
    ["mobile", 390, 844],
    ["mobile-long", 390, 1200],
  ]) {
    await client.call("Emulation.setDeviceMetricsOverride", {
      width,
      height,
      deviceScaleFactor: 1,
      mobile: width < 600,
      screenWidth: width,
      screenHeight: height,
    });

    const loaded = client.once("Page.loadEventFired");
    await client.call("Page.navigate", { url: "http://127.0.0.1:4173/" });
    await loaded;
    await client.call("Runtime.evaluate", {
      expression: "new Promise(resolve => setTimeout(resolve, 1700))",
      awaitPromise: true,
    });

    const metrics = await client.call("Runtime.evaluate", {
      expression: `JSON.stringify({
        innerWidth,
        innerHeight,
        scrollWidth: document.documentElement.scrollWidth,
        scrollHeight: document.documentElement.scrollHeight,
        title: document.title,
        message: document.querySelector('#message-title')?.textContent.trim(),
        replayDisabled: document.querySelector('.replay')?.disabled
      })`,
      returnByValue: true,
    });

    const screenshot = await client.call("Page.captureScreenshot", {
      format: "png",
      captureBeyondViewport: false,
      fromSurface: true,
    });

    const target = path.join(output, `${name}.png`);
    await writeFile(target, screenshot.data, "base64");
    console.log(JSON.stringify({
      captured: name,
      size: `${width},${height}`,
      target,
      metrics: JSON.parse(metrics.result.value),
    }));
  }

  await client.call("Input.dispatchKeyEvent", { type: "keyDown", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 });
  await client.call("Input.dispatchKeyEvent", { type: "keyUp", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 });
  await client.call("Input.dispatchKeyEvent", { type: "keyDown", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 });
  await client.call("Input.dispatchKeyEvent", { type: "keyUp", key: "Tab", code: "Tab", windowsVirtualKeyCode: 9 });

  const focusState = await client.call("Runtime.evaluate", {
    expression: "JSON.stringify({ tag: document.activeElement?.tagName, className: document.activeElement?.className })",
    returnByValue: true,
  });

  await client.call("Input.dispatchKeyEvent", {
    type: "keyDown",
    key: " ",
    code: "Space",
    text: " ",
    unmodifiedText: " ",
    windowsVirtualKeyCode: 32,
    nativeVirtualKeyCode: 32,
  });
  await client.call("Input.dispatchKeyEvent", { type: "keyUp", key: " ", code: "Space", windowsVirtualKeyCode: 32 });
  await new Promise(resolve => setTimeout(resolve, 50));

  const replayStarted = await client.call("Runtime.evaluate", {
    expression: "JSON.stringify({ disabled: document.querySelector('.replay').disabled, status: document.querySelector('#replay-status').textContent })",
    returnByValue: true,
  });

  await client.call("Runtime.evaluate", {
    expression: "new Promise(resolve => setTimeout(resolve, 1700))",
    awaitPromise: true,
  });

  const replayFinished = await client.call("Runtime.evaluate", {
    expression: "JSON.stringify({ disabled: document.querySelector('.replay').disabled, status: document.querySelector('#replay-status').textContent, focusRestored: document.activeElement === document.querySelector('.replay') })",
    returnByValue: true,
  });

  await client.call("Emulation.setEmulatedMedia", {
    media: "screen",
    features: [{ name: "prefers-reduced-motion", value: "reduce" }],
  });
  const reducedMotion = await client.call("Runtime.evaluate", {
    expression: `document.querySelector('.replay').click(); JSON.stringify({
      disabled: document.querySelector('.replay').disabled,
      status: document.querySelector('#replay-status').textContent,
      preference: matchMedia('(prefers-reduced-motion: reduce)').matches
    })`,
    returnByValue: true,
  });
  await client.call("Emulation.setEmulatedMedia", { media: "screen", features: [] });

  console.log(JSON.stringify({
    verification: {
      focusAfterTwoTabs: JSON.parse(focusState.result.value),
      replayStarted: JSON.parse(replayStarted.result.value),
      replayFinished: JSON.parse(replayFinished.result.value),
      reducedMotion: JSON.parse(reducedMotion.result.value),
      runtimeErrors,
      failedRequests,
    },
  }));

  client.close();
} finally {
  server.kill("SIGTERM");
  chrome.kill("SIGTERM");
  if (chrome.exitCode === null) {
    await Promise.race([
      new Promise(resolve => chrome.once("exit", resolve)),
      new Promise(resolve => setTimeout(resolve, 2500)),
    ]);
  }
  await rm(chromeProfile, { recursive: true, force: true });
}
