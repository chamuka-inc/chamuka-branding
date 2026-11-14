import { readFileSync, writeFileSync } from "node:fs";

for (const file of process.argv.slice(2)) {
  const source = readFileSync(file, "utf8");
  if (source.startsWith('"use client"') || source.startsWith("'use client'")) continue;
  writeFileSync(file, `"use client";\n${source}`);
}
