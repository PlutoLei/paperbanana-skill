#!/usr/bin/env node
// Routing only. This helper never calls a provider, reads credentials, or generates an image.
import { readFileSync } from 'node:fs';
import { isAbsolute, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const allowed = new Set(['prompt', 'mode', 'native_available', 'provider', 'model',
  'reference_paths', 'num_last_images_to_include', 'mask_path', 'size', 'quality',
  'output_format', 'background', 'require_pipeline']);
const text = (x) => typeof x === 'string' && x.trim().length > 0;

export function routeImage(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)
      || Object.keys(input).some((key) => !allowed.has(key))) throw new Error('INVALID_REQUEST');
  if (!text(input.prompt) || !['generate', 'edit'].includes(input.mode)
      || typeof input.native_available !== 'boolean') throw new Error('INVALID_REQUEST');
  if (input.require_pipeline !== undefined && typeof input.require_pipeline !== 'boolean') {
    throw new Error('INVALID_PIPELINE_REQUIREMENT');
  }
  for (const key of ['provider', 'model', 'size', 'quality', 'output_format', 'background']) {
    if (input[key] !== undefined && !text(input[key])) throw new Error(`INVALID_${key.toUpperCase()}`);
  }
  const paths = input.reference_paths ?? [];
  if (!Array.isArray(paths) || paths.some((p) => !text(p) || !isAbsolute(p))) throw new Error('INVALID_REFERENCE_PATHS');
  const count = input.num_last_images_to_include;
  if (count !== undefined && (!Number.isInteger(count) || count < 1 || count > 5)) throw new Error('INVALID_IMAGE_COUNT');
  if (paths.length && count !== undefined) throw new Error('MIXED_REFERENCE_CHANNELS');
  if (input.mask_path !== undefined && (!text(input.mask_path) || !isAbsolute(input.mask_path))) throw new Error('INVALID_MASK_PATH');
  if (input.mode === 'edit' && !paths.length && count === undefined) throw new Error('EDIT_REQUIRES_REFERENCE');
  if (input.mask_path && (input.mode !== 'edit' || !paths.length)) throw new Error('MASK_REQUIRES_LOCAL_EDIT');

  const explicitApi = input.model !== undefined
    || (input.provider !== undefined && input.provider !== 'codex-native')
    || ['size', 'quality', 'output_format', 'background', 'mask_path'].some((key) => input[key] !== undefined);
  if (input.provider === 'codex-native' && (explicitApi || input.require_pipeline)) {
    throw new Error('NATIVE_CANNOT_GUARANTEE_REQUESTED_CONTROLS');
  }
  if (input.native_available && !explicitApi && !input.require_pipeline) {
    const args = { prompt: input.prompt };
    if (paths.length) args.referenced_image_paths = paths;
    if (count !== undefined) args.num_last_images_to_include = count;
    return { backend: 'codex-native', tool_arguments: args, model: null,
      review_status: 'UNREVIEWED', inspect_local_references: paths.length > 0 };
  }
  if (input.provider === 'codex-native') throw new Error('NATIVE_TOOL_UNAVAILABLE');
  if (count !== undefined) throw new Error('API_REQUIRES_LOCAL_REFERENCES');
  return { backend: 'paperbanana', reason: explicitApi ? 'explicit-provider-or-controls'
    : input.require_pipeline ? 'pipeline-requested' : 'native-tool-unavailable',
    request: { ...input, reference_paths: paths }, requires_provider_access: true,
    verify_installed_capabilities: true, review_status: 'UNREVIEWED' };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    if (process.argv.length !== 3) throw new Error('USAGE: route-image.mjs request.json');
    console.log(JSON.stringify(routeImage(JSON.parse(readFileSync(process.argv[2], 'utf8'))), null, 2));
  } catch (error) {
    console.error(error instanceof SyntaxError ? 'INVALID_JSON' : error.message);
    process.exitCode = 1;
  }
}
