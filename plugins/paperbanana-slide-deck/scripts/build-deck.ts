import { existsSync, mkdirSync } from "node:fs";
import { basename, dirname, join, resolve } from "node:path";
import { buildImageDeck } from "./merge-to-pptx";
import { renderEditableDeck } from "./editable/render-editable-pptx";

export type DeckMode = "image" | "editable";

export interface BuildArgs {
  mode: DeckMode;
  deckDir: string;
  output?: string;
}

const USAGE = [
  "Usage:",
  "  bun scripts/build-deck.ts --mode image <deck-dir> [--output deck.pptx]",
  "  bun scripts/build-deck.ts --mode editable <deck-dir> [--output deck.pptx]",
].join("\n");

export function parseBuildArgs(argv: string[]): BuildArgs {
  let mode: string | undefined;
  let deckDir = "";
  let output: string | undefined;

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--mode") {
      mode = argv[++i];
    } else if (arg === "--output" || arg === "-o") {
      output = argv[++i];
    } else if (!arg.startsWith("-")) {
      deckDir = arg;
    } else {
      throw new Error(`unknown option ${arg}\n${USAGE}`);
    }
  }

  if (!mode) throw new Error(`--mode image|editable is required\n${USAGE}`);
  if (mode !== "image" && mode !== "editable") {
    throw new Error(`unsupported mode ${mode}: editable never falls back to image\n${USAGE}`);
  }
  if (!deckDir) throw new Error(`deck directory is required\n${USAGE}`);
  if (mode === "editable" && !existsSync(join(deckDir, "slide-spec.json"))) {
    throw new Error(`slide-spec.json not found in ${deckDir}: editable mode requires an explicit spec and never falls back to image mode`);
  }

  return { mode, deckDir, output };
}

function defaultOutput(deckDir: string): string {
  const dirName = basename(deckDir) === "slide-deck" ? basename(join(deckDir, "..")) : basename(deckDir);
  return join(deckDir, `${dirName}.pptx`);
}

if (import.meta.main) {
  try {
    const { mode, deckDir, output } = parseBuildArgs(process.argv.slice(2));
    const outputPath = output ?? defaultOutput(deckDir);
    if (mode === "image") {
      await buildImageDeck(deckDir, outputPath);
    } else {
      // The spec is validated in full before any output is written; on failure
      // we exit non-zero without touching old or partial artifacts and never
      // route to image mode.
      mkdirSync(dirname(resolve(outputPath)), { recursive: true });
      const written = await renderEditableDeck(join(deckDir, "slide-spec.json"), outputPath);
      console.log(`Created: ${written}`);
    }
  } catch (err) {
    console.error("Error:", (err as Error).message);
    process.exit(1);
  }
}
