import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

describe("@chamuka/icons", () => {
  it("exports Daybreak mark, lockups, and product marks", () => {
    const index = readFileSync(join(ROOT, "src/generated/index.ts"), "utf8");
    for (const name of [
      "Mark",
      "MarkSimple",
      "LockupHorizontal",
      "LockupStacked",
      "LockupDrawIt",
      "LockupFormIt",
      "LockupPlay",
      "LockupWaypoint",
      "LockupVmette",
      "Wordmark",
      "AppIconDrawIt",
    ]) {
      expect(index).toContain(`export { default as ${name} }`);
    }
  });
});
