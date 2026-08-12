import { existsSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, resolve } from "node:path";
import AjvModule from "ajv/dist/2020.js";

// ajv ships CJS with an __esModule marker; normalize so the constructor
// resolves identically under Bun and Node interop.
const Ajv2020 = ((AjvModule as { default?: unknown }).default ?? AjvModule) as new (
  opts: Record<string, unknown>
) => { compile(schema: unknown): SchemaValidator };

interface SchemaValidator {
  (data: unknown): boolean;
  errors?: Array<{ instancePath: string; message?: string }> | null;
}

export interface SlideElement {
  id: string;
  type: string;
  x: number;
  y: number;
  w: number;
  h: number;
  text?: string;
  font_size?: number;
  color?: string;
  align?: "left" | "center" | "right";
  valign?: "top" | "middle" | "bottom";
  bold?: boolean;
  shape?: string;
  fill?: string;
  stroke?: string;
  rows?: unknown[];
  chart_type?: "bar" | "line" | "scatter";
  series?: unknown[];
  path?: string;
  sha256?: string;
  alt_text?: string;
  end_arrow?: "none" | "triangle" | "stealth" | "arrow";
  children?: SlideElement[];
}

export interface SlideSpecSlide {
  id: string;
  title: string;
  speaker_notes: string;
  sources: string[];
  elements: SlideElement[];
}

export interface SlideSpec {
  schema_version: string;
  deck: { layout: string; language: string; theme: string };
  slides: SlideSpecSlide[];
}

export interface ValidateOptions {
  baseDir?: string;
  checkAssets?: boolean;
}

export interface ValidationResult {
  ok: boolean;
  errors: string[];
}

const schema = JSON.parse(
  readFileSync(new URL("./slide-spec.schema.json", import.meta.url), "utf8")
);
const validateSchema = new Ajv2020({ allErrors: true, strict: true }).compile(schema);

const W = 13.333;
const H = 7.5;
const EPS = 1e-6;

function checkElement(
  slideId: string,
  el: SlideElement,
  elementIds: Set<string>,
  errors: string[],
  baseDir: string,
  checkAssets: boolean,
  group?: SlideElement
): void {
  if (elementIds.has(el.id)) errors.push(`${slideId} duplicate element id ${el.id}`);
  elementIds.add(el.id);
  // A connector may be a pure horizontal/vertical line (w or h of 0); everything else needs area.
  if (el.type !== "line" && (!(el.w > 0) || !(el.h > 0))) {
    errors.push(`${slideId}/${el.id} requires positive width and height`);
  }
  if (group) {
    // Group children use group-relative coordinates and must stay inside the group box.
    if (el.x + el.w > group.w + EPS || el.y + el.h > group.h + EPS) {
      errors.push(`${slideId}/${el.id} outside group bounds of ${group.id}`);
    }
  } else if (el.x + el.w > W + EPS || el.y + el.h > H + EPS) {
    errors.push(`${slideId}/${el.id} outside slide bounds`);
  }
  if (el.type === "text" && (!el.text || !el.font_size)) {
    errors.push(`${slideId}/${el.id} text requires text and font_size`);
  }
  if (el.type === "table" && (!Array.isArray(el.rows) || el.rows.length === 0)) {
    errors.push(`${slideId}/${el.id} table requires non-empty rows`);
  }
  if (el.type === "chart" && (!Array.isArray(el.series) || el.series.length === 0)) {
    errors.push(`${slideId}/${el.id} chart requires non-empty series`);
  }
  if (el.type === "image" && (!el.sha256 || !el.alt_text)) {
    errors.push(`${slideId}/${el.id} image requires sha256 and alt_text`);
  }
  if (el.type === "image" && checkAssets) {
    const asset = resolve(baseDir, el.path ?? "");
    if (!existsSync(asset)) {
      errors.push(`${slideId}/${el.id} missing asset ${asset}`);
    } else if (el.sha256) {
      const actual = createHash("sha256").update(readFileSync(asset)).digest("hex");
      if (actual !== el.sha256) {
        errors.push(`${slideId}/${el.id} asset sha256 mismatch: pinned ${el.sha256}, actual ${actual}`);
      }
    }
  }
  if (el.type === "group") {
    if (!Array.isArray(el.children) || el.children.length === 0) {
      errors.push(`${slideId}/${el.id} group requires non-empty children`);
    } else {
      for (const child of el.children) {
        checkElement(slideId, child, elementIds, errors, baseDir, checkAssets, el);
      }
    }
  }
}

export function validateSlideSpec(
  spec: unknown,
  { baseDir = process.cwd(), checkAssets = true }: ValidateOptions = {}
): ValidationResult {
  const errors: string[] = [];
  if (!validateSchema(spec)) {
    errors.push(...(validateSchema.errors ?? []).map((e) => `${e.instancePath} ${e.message}`));
  }
  const parsed = spec as SlideSpec;
  const slideIds = new Set<string>();
  for (const slide of parsed.slides ?? []) {
    if (slideIds.has(slide.id)) errors.push(`duplicate slide id ${slide.id}`);
    slideIds.add(slide.id);
    if (!slide.speaker_notes?.includes("[Sources]")) {
      errors.push(`${slide.id} missing [Sources] notes block`);
    }
    const elementIds = new Set<string>();
    for (const el of slide.elements ?? []) {
      checkElement(slide.id, el, elementIds, errors, baseDir, checkAssets);
    }
  }
  return { ok: errors.length === 0, errors };
}

export function loadAndValidate(specPath: string): { spec: SlideSpec; absolute: string } {
  const absolute = resolve(specPath);
  const spec = JSON.parse(readFileSync(absolute, "utf8")) as SlideSpec;
  const result = validateSlideSpec(spec, { baseDir: dirname(absolute), checkAssets: true });
  if (!result.ok) throw new Error(result.errors.join("\n"));
  return { spec, absolute };
}

if (import.meta.main) {
  const specPath = process.argv[2];
  if (!specPath) {
    console.error("Usage: bun validate-slide-spec.ts <slide-spec.json>");
    process.exit(1);
  }
  loadAndValidate(specPath);
  process.stdout.write("slide spec valid\n");
}
