import { cp, mkdir, readdir, rm, stat } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const dist = path.join(root, "dist");
await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });

const required = path.join(root, "index.html");
try { await stat(required); } catch { throw new Error("index.html is required for the production build"); }

for (const name of await readdir(root)) {
  if (["dist", "artifacts", "node_modules", "build.mjs", "capture.mjs", "package.json", "DESIGN.md"].includes(name)) continue;
  const source = path.join(root, name);
  const info = await stat(source);
  if (info.isDirectory() && name !== "assets") continue;
  if (info.isFile() && !/[.](html|css|js|json|svg|png|jpg|jpeg|webp|ico)$/i.test(name)) continue;
  await cp(source, path.join(dist, name), { recursive: true });
}
console.log(JSON.stringify({ built: true, output: dist }));
