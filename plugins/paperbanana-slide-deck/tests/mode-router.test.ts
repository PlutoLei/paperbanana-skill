import { expect, test } from "bun:test";
import { parseBuildArgs } from "../scripts/build-deck";

test("requires an explicit image or editable mode", () => {
  expect(() => parseBuildArgs(["deck"])).toThrow("--mode image|editable is required");
  expect(() => parseBuildArgs(["--mode", "auto", "deck"])).toThrow("unsupported mode auto");
});

test("editable requires slide-spec.json and never falls back", () => {
  expect(() => parseBuildArgs(["--mode", "editable", "/missing/deck"])).toThrow("slide-spec.json not found");
});
