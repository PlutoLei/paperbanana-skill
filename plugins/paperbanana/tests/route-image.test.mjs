import test from 'node:test';
import assert from 'node:assert/strict';
import { routeImage } from '../skills/paperbanana/scripts/route-image.mjs';

const request = { prompt: 'Draw a labeled pipeline', mode: 'generate', native_available: true };
test('ordinary generation uses only supported native arguments without claiming a model', () => {
  const result = routeImage(request);
  assert.deepEqual(result.tool_arguments, { prompt: request.prompt });
  assert.equal(result.model, null);
  assert.equal(result.review_status, 'UNREVIEWED');
});
test('local edits preserve every reference and require inspection', () => {
  const references = ['/tmp/source.png', '/tmp/style.png'];
  const result = routeImage({ ...request, mode: 'edit', reference_paths: references });
  assert.deepEqual(result.tool_arguments.referenced_image_paths, references);
  assert.equal(result.inspect_local_references, true);
});
test('conversation-image editing uses its own channel', () => {
  const result = routeImage({ ...request, mode: 'edit', num_last_images_to_include: 2 });
  assert.equal(result.tool_arguments.num_last_images_to_include, 2);
  assert.equal('referenced_image_paths' in result.tool_arguments, false);
});
for (const model of ['gpt-image-2', 'gpt-image-2.5-sunburst', 'gpt-image-2.5-flare-2026-09-08']) {
  test(`explicit ${model} is not silently sent to an unselectable native model`, () => {
    const result = routeImage({ ...request, model });
    assert.equal(result.backend, 'paperbanana');
    assert.equal(result.request.model, model);
    assert.equal(result.requires_provider_access, true);
  });
}
test('pipeline selection and explicit non-OpenAI provider survive routing', () => {
  assert.equal(routeImage({ ...request, require_pipeline: true }).backend, 'paperbanana');
  assert.equal(routeImage({ ...request, provider: 'google_imagen' }).request.provider, 'google_imagen');
});
test('native cannot silently discard a strict size, quality, model or pipeline requirement', () => {
  for (const extra of [{ size: '1536x864' }, { quality: 'xhigh' }, { model: 'gpt-image-2.5-flare' }, { require_pipeline: true }]) {
    assert.throws(() => routeImage({ ...request, provider: 'codex-native', ...extra }), /NATIVE_CANNOT/);
  }
});
test('mask editing remains an explicit provider capability', () => {
  const result = routeImage({ ...request, mode: 'edit', reference_paths: ['/tmp/base.png'], mask_path: '/tmp/mask.png' });
  assert.equal(result.backend, 'paperbanana');
  assert.equal(result.request.mask_path, '/tmp/mask.png');
});
test('missing or mixed references, invalid modes and counts fail before routing', () => {
  for (const extra of [{ mode: 'edit' }, { mode: 'unknown' }, { reference_paths: ['relative.png'] },
    { reference_paths: ['/tmp/a.png'], num_last_images_to_include: 1 }, { num_last_images_to_include: 6 },
    { mask_path: '/tmp/mask.png' }, { unsupported: true }]) {
    assert.throws(() => routeImage({ ...request, ...extra }));
  }
});
test('missing native tool is reported and never starts an API call', () => {
  assert.equal(routeImage({ ...request, native_available: false }).verify_installed_capabilities, true);
  assert.throws(() => routeImage({ ...request, native_available: false, provider: 'codex-native' }), /UNAVAILABLE/);
  assert.throws(() => routeImage({ ...request, native_available: false, mode: 'edit', num_last_images_to_include: 1 }), /LOCAL_REFERENCES/);
});

test('Gemini-bound tasks stay on their existing backend even when native is available', () => {
  const result = routeImage({prompt: 'An existing slide', mode: 'generate', native_available: true,
    provider: 'google_imagen', model: 'gemini-3-pro-image'});
  assert.equal(result.backend, 'paperbanana');
  assert.equal(result.request.provider, 'google_imagen');
  assert.equal(result.request.model, 'gemini-3-pro-image');
});
