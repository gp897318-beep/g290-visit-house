// G290-VISIT-HOUSE: a letter in one image inviting the AI judge to visit.
// The image is drawn by draw.py (PIL) and committed as entry.png;
// this entry point only copies it, so two runs produce identical bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
