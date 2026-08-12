import { dirname, resolve } from "node:path";
import PptxGenJS from "pptxgenjs";
import { loadAndValidate, type SlideElement } from "./validate-slide-spec";

const THEMES = {
  "paperbanana-parchment": {
    background: "F7F2E6", ink: "25231F", muted: "6D6A64", rule: "C8C3B8",
    accent: "2A9D8F", accent2: "4A6FD4", headFont: "Charter", bodyFont: "Charter"
  },
  "paperbanana-clean": {
    background: "FFFFFF", ink: "1F2937", muted: "64748B", rule: "CBD5E1",
    accent: "0F766E", accent2: "4F46E5", headFont: "Aptos Display", bodyFont: "Aptos"
  }
} as const;

type Theme = (typeof THEMES)[keyof typeof THEMES];

function addElement(
  slide: ReturnType<PptxGenJS["addSlide"]>,
  pptx: PptxGenJS,
  el: SlideElement,
  baseDir: string,
  theme: Theme
): void {
  const box = { objectName: el.id, x: el.x, y: el.y, w: el.w, h: el.h };
  if (el.type === "text") {
    slide.addText(el.text ?? "", { ...box, fontFace: theme.bodyFont,
      fontSize: el.font_size ?? 18, color: el.color ?? theme.ink, margin: 0,
      align: el.align, valign: el.valign, bold: el.bold });
    return;
  }
  if (el.type === "shape") {
    slide.addShape((el.shape ?? pptx.ShapeType.rect) as Parameters<typeof slide.addShape>[0],
      { ...box, fill: { color: el.fill ?? "FFFFFF" }, line: { color: el.stroke ?? theme.rule } });
    return;
  }
  if (el.type === "line") {
    slide.addShape(pptx.ShapeType.line, { ...box, line: { color: el.stroke ?? theme.muted,
      width: 1.5, endArrowType: el.end_arrow ?? "none" } });
    return;
  }
  if (el.type === "table") {
    slide.addTable(el.rows as PptxGenJS.TableRow[], { ...box, fontFace: theme.bodyFont,
      fontSize: 16, border: { type: "solid", color: theme.rule, pt: 0.6 } });
    return;
  }
  if (el.type === "chart") {
    slide.addChart(pptx.ChartType[el.chart_type ?? "bar"], el.series as unknown[],
      { ...box, showLegend: true, legendPos: "b", showTitle: false, showValue: true,
        chartColors: [theme.accent], dataLabelFormatCode: "0.0000",
        catAxisLabelColor: theme.ink, catAxisLabelFontFace: theme.bodyFont,
        valAxisLabelColor: theme.ink, valAxisLabelFontFace: theme.bodyFont,
        dataLabelColor: theme.ink, dataLabelFontFace: theme.bodyFont,
        legendColor: theme.ink, legendFontFace: theme.bodyFont });
    return;
  }
  if (el.type === "image") {
    slide.addImage({ ...box, path: resolve(baseDir, el.path ?? ""), altText: el.alt_text });
    return;
  }
  if (el.type === "group") {
    // Layout-only container: PptxGenJS 4.0.1 exposes no native PowerPoint group
    // API, so the container itself is never emitted or rasterised. Children are
    // offset from group-relative to absolute slide coordinates and emitted as
    // native editable objects with their own stable objectName IDs.
    const children = el.children ?? [];
    const toAbsolute = (child: SlideElement): SlideElement =>
      ({ ...child, x: el.x + child.x, y: el.y + child.y });
    for (const child of children.filter((c) => c.type === "line")) {
      addElement(slide, pptx, toAbsolute(child), baseDir, theme);
    }
    for (const child of children.filter((c) => c.type !== "line")) {
      addElement(slide, pptx, toAbsolute(child), baseDir, theme);
    }
    return;
  }
  throw new Error(`unsupported element ${el.type}: ${el.id}`);
}

export async function renderEditableDeck(specPath: string, outputPath: string): Promise<string> {
  const { spec, absolute } = loadAndValidate(specPath);
  const theme = THEMES[spec.deck.theme as keyof typeof THEMES];
  if (!theme) throw new Error(`unsupported theme: ${spec.deck.theme}`);
  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "PaperBanana";
  pptx.subject = "Editable PaperBanana slide deck";
  const baseDir = dirname(absolute);
  for (const slideSpec of spec.slides) {
    const slide = pptx.addSlide();
    slide.background = { color: theme.background };
    for (const el of slideSpec.elements.filter((item) => item.type === "line")) addElement(slide, pptx, el, baseDir, theme);
    for (const el of slideSpec.elements.filter((item) => item.type !== "line")) addElement(slide, pptx, el, baseDir, theme);
    slide.addNotes(slideSpec.speaker_notes);
  }
  await pptx.writeFile({ fileName: resolve(outputPath) });
  return resolve(outputPath);
}

if (import.meta.main) {
  const [specPath, outputPath] = process.argv.slice(2);
  if (!specPath || !outputPath) {
    console.error("Usage: bun render-editable-pptx.ts <slide-spec.json> <output.pptx>");
    process.exit(1);
  }
  try {
    const written = await renderEditableDeck(specPath, outputPath);
    console.log(`Created: ${written}`);
  } catch (err) {
    console.error("Error:", (err as Error).message);
    process.exit(1);
  }
}
