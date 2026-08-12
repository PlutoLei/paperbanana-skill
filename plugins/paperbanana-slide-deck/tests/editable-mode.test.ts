import { expect, test } from "bun:test";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { execFileSync } from "node:child_process";
import { renderEditableDeck } from "../scripts/editable/render-editable-pptx";
import { validateSlideSpec } from "../scripts/editable/validate-slide-spec";

test("invalid element type fails instead of becoming a raster slide", () => {
  const bad = { schema_version: "1", deck: { layout: "LAYOUT_WIDE", language: "en", theme: "paperbanana-parchment" },
    slides: [{ id: "s1", title: "Claim", sources: ["local:test"], speaker_notes: "[Sources]\\n- local:test",
      elements: [{ id: "x", type: "smartart", x: 1, y: 1, w: 2, h: 1 }] }] };
  const result = validateSlideSpec(bad, { baseDir: process.cwd(), checkAssets: false });
  expect(result.ok).toBe(false);
  expect(result.errors.join("\n")).toContain("allowed values");
});

test("layout groups validate children in absolute slide coordinates", () => {
  const grouped = JSON.parse(readFileSync(resolve("tests/fixtures/editable/slide-spec.json"), "utf8"));
  grouped.slides[0].elements = [{ id: "group", type: "group", x: 1, y: 1, w: 4, h: 2,
    children: [{ id: "group-label", type: "text", x: 0.2, y: 0.2, w: 3, h: 0.5,
      text: "Grouped label", font_size: 20 }] }];
  expect(validateSlideSpec(grouped, { baseDir: process.cwd(), checkAssets: false }).ok).toBe(true);
  grouped.slides[0].elements[0].children[0].x = 3.8;
  const invalid = validateSlideSpec(grouped, { baseDir: process.cwd(), checkAssets: false });
  expect(invalid.ok).toBe(false);
  expect(invalid.errors.join("\n")).toContain("outside group bounds");
});

test("editable mode writes native text table chart shapes and notes", async () => {
  const dir = mkdtempSync(join(tmpdir(), "paperbanana-editable-"));
  try {
    const out = join(dir, "editable.pptx");
    await renderEditableDeck(resolve("tests/fixtures/editable/slide-spec.json"), out);
    const listing = execFileSync("unzip", ["-Z1", out], { encoding: "utf8" });
    expect(listing).toContain("ppt/charts/chart1.xml");
    expect(listing).toContain("ppt/notesSlides/notesSlide1.xml");
    const xml = execFileSync("unzip", ["-p", out, "ppt/slides/slide1.xml"], { encoding: "utf8" });
    expect(xml).toContain("Editable conclusion");
    expect(xml).toContain("Native table");
    expect(xml).toContain("title-text");
    expect(xml.match(/<p:pic>/g)?.length ?? 0).toBeLessThan(2);
  } finally { rmSync(dir, { recursive: true, force: true }); }
});
