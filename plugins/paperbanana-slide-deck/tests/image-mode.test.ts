import { afterEach, expect, test } from "bun:test";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { mkdtempSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { buildImageDeck } from "../scripts/merge-to-pptx";

const made: string[] = [];
afterEach(() => { for (const dir of made.splice(0)) rmSync(dir, { recursive: true, force: true }); });

test("legacy image mode emits one full-slide image and prompt notes", async () => {
  const dir = mkdtempSync(join(tmpdir(), "paperbanana-image-"));
  made.push(dir);
  mkdirSync(join(dir, "prompts"));
  const png = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Y9Zl1sAAAAASUVORK5CYII=", "base64");
  writeFileSync(join(dir, "01-slide-smoke.png"), png);
  writeFileSync(join(dir, "prompts/01-slide-smoke.md"), "# Smoke prompt\n");
  const out = join(dir, "legacy.pptx");
  await buildImageDeck(dir, out);
  expect(existsSync(out)).toBe(true);
  const xml = execFileSync("unzip", ["-p", out, "ppt/slides/slide1.xml"], { encoding: "utf8" });
  expect(xml.match(/<p:pic>/g)?.length).toBe(1);
  expect(xml).not.toContain("<a:t>Smoke prompt</a:t>");
  const listing = execFileSync("unzip", ["-Z1", out], { encoding: "utf8" });
  expect(listing).toContain("ppt/notesSlides/notesSlide1.xml");
});
