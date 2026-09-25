// CDP check: move the mouse to a rendered parcel and click it on the normal route.
const [debugPort, pageUrl] = process.argv.slice(2);
const pages = await (await fetch(`http://127.0.0.1:${debugPort}/json`)).json();
const page = pages.find((entry) => entry.type === "page");
if (!page) throw new Error("no browser page");

const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  ws.addEventListener("open", resolve, { once: true });
  ws.addEventListener("error", reject, { once: true });
});

let sequence = 0;
const pending = new Map();
ws.addEventListener("message", ({ data }) => {
  const message = JSON.parse(data);
  if (!message.id) return;
  const item = pending.get(message.id);
  if (!item) return;
  pending.delete(message.id);
  if (message.error) item.reject(new Error(message.error.message));
  else item.resolve(message.result);
});
function send(method, params = {}) {
  const id = ++sequence;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
}
async function evaluate(expression) {
  const result = await send("Runtime.evaluate", { expression, returnByValue: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
  return result.result.value;
}
async function until(expression) {
  for (let attempt = 0; attempt < 40; attempt++) {
    const value = await evaluate(expression);
    if (value) return value;
    await new Promise((resolve) => setTimeout(resolve, 50));
  }
  throw new Error(`page did not become ready: ${expression}`);
}

try {
  await send("Page.enable");
  await send("Runtime.enable");
  await send("Page.navigate", { url: pageUrl });
  await until("document.readyState === 'complete' && !!document.querySelector('[data-parcel-id=\"P-101\"]')");
  const before = await evaluate("document.querySelector('#details').hidden");
  const box = await evaluate(`(() => {
    const r = document.querySelector('[data-parcel-id="P-101"]').getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
  })()`);
  await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: box.x, y: box.y });
  await send("Input.dispatchMouseEvent", { type: "mousePressed", x: box.x, y: box.y, button: "left", clickCount: 1 });
  await send("Input.dispatchMouseEvent", { type: "mouseReleased", x: box.x, y: box.y, button: "left", clickCount: 1 });
  let after;
  try {
    after = await until(`(() => {
      const d = document.querySelector('#details');
      return !d.hidden && d.textContent.includes('P-101') && d.textContent.includes('12 River Lane');
    })()`);
  } catch {
    after = false;
  }
  await send("Page.navigate", { url: `${pageUrl}?fixture=P-101` });
  await until("document.readyState === 'complete' && !!document.querySelector('#details')");
  const fixture = await evaluate(`(() => {
    const d = document.querySelector('#details');
    return !d.hidden && d.textContent.includes('P-101') && d.textContent.includes('12 River Lane');
  })()`);
  console.log(JSON.stringify({ before, after, fixture,
    passed: before === true && after === true && fixture === true }));
} finally {
  ws.close();
}
