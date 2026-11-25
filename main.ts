// G290-VISIT-HOUSE: a letter in one image inviting the AI judge to visit.
// The image is drawn by draw.py (PIL) and committed as entry.png;
// this entry point only copies it, so two runs produce identical bytes.
// Before copying it checks the gate's own conditions: a whole PNG,
// at most 1 MiB and at most 1024 by 1024 pixels.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const buf = readFileSync(src);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(PNG_MAGIC)) throw new Error("entry.png is not a PNG");
if (buf.length > 1_048_576) throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB gate`);
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 gate`);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")} (${width}x${height}, ${buf.length} bytes)`);
