import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

function parseCustomProperties(block: string): Map<string, string> {
  const map = new Map<string, string>();
  const re = /--([a-z0-9-]+)\s*:\s*([^;]+);/gi;
  let match: RegExpExecArray | null;
  while ((match = re.exec(block))) {
    const name = `--${match[1]!.toLowerCase()}`;
    const value = match[2]!.replace(/\/\*[\s\S]*?\*\//g, "").trim().replace(/\s+/g, " ");
    map.set(name, value);
  }
  return map;
}

function extractBlock(css: string, header: RegExp): string {
  const start = css.search(header);
  if (start < 0) throw new Error(`Block not found: ${header}`);
  const open = css.indexOf("{", start);
  let depth = 0;
  for (let i = open; i < css.length; i++) {
    if (css[i] === "{") depth += 1;
    if (css[i] === "}") {
      depth -= 1;
      if (depth === 0) return css.slice(open + 1, i);
    }
  }
  throw new Error("Unclosed block");
}

describe("generated tokens.css vs original brand snapshot", () => {
  const original = readFileSync(join(ROOT, "fixtures/original-tokens.css"), "utf8");
  const generated = readFileSync(join(ROOT, "dist/tokens.css"), "utf8");

  it("preserves every :root custom property value", () => {
    const fromOriginal = parseCustomProperties(extractBlock(original, /:root\s*\{/));
    const fromGenerated = parseCustomProperties(extractBlock(generated, /:root\s*\{/));
    expect(fromOriginal.size).toBeGreaterThan(20);
    for (const [name, value] of fromOriginal) {
      expect(fromGenerated.get(name), name).toBe(value);
    }
  });

  it("preserves every .dark custom property value", () => {
    const fromOriginal = parseCustomProperties(extractBlock(original, /\.dark\s*\{/));
    const fromGenerated = parseCustomProperties(
      extractBlock(generated, /\.dark\s*,\s*\[data-theme=["']dark["']\]\s*\{/),
    );
    expect(fromOriginal.size).toBeGreaterThan(10);
    for (const [name, value] of fromOriginal) {
      expect(fromGenerated.get(name), name).toBe(value);
    }
  });

  it("preserves every @theme custom property value", () => {
    const fromOriginal = parseCustomProperties(extractBlock(original, /@theme\s*\{/));
    const fromGenerated = parseCustomProperties(extractBlock(generated, /@theme\s*\{/));
    expect(fromOriginal.size).toBeGreaterThan(20);
    for (const [name, value] of fromOriginal) {
      expect(fromGenerated.get(name), name).toBe(value);
    }
  });
});
