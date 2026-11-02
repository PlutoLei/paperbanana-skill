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

for (const transparent of [true, false]) {
  const background = transparent ? 'transparent' : 'opaque';
  test(`native accepts transparent_background=${transparent}`, () => {
    const result = routeImage({ ...request, transparent_background: transparent });
    assert.equal(result.backend, 'codex-native');
    assert.deepEqual(result.tool_arguments, { prompt: request.prompt, transparent_background: transparent });
  });

  test(`${background} background alias becomes the native boolean control`, () => {
    const result = routeImage({ ...request, provider: 'codex-native', background });
    assert.equal(result.backend, 'codex-native');
    assert.equal(result.tool_arguments.transparent_background, transparent);
    assert.equal('background' in result.tool_arguments, false);
  });

  test(`matching ${background} controls are accepted without dropping the explicit value`, () => {
    const result = routeImage({ ...request, background, transparent_background: transparent });
    assert.equal(result.tool_arguments.transparent_background, transparent);
  });

  test(`API fallback translates transparent_background=${transparent} to background`, () => {
    for (const extra of [{ native_available: false }, { model: 'gpt-image-2.5-flare' },
      { quality: 'high' }, { size: '1536x864' }, { output_format: 'png' },
      { require_pipeline: true }, { provider: 'google_imagen' }, { provider: 'bedrock_imagen' }]) {
      const input = { ...request, ...extra, transparent_background: transparent };
      const result = routeImage(input);
      assert.equal(result.backend, 'paperbanana');
      assert.equal(result.request.background, background);
      assert.equal('transparent_background' in result.request, false);
      assert.equal(input.transparent_background, transparent);
      if (extra.provider) assert.equal(result.request.provider, extra.provider);
    }
  });
}

test('transparency is preserved in native local and conversation-image edits', () => {
  for (const refs of [{ reference_paths: ['/tmp/source.png'] }, { num_last_images_to_include: 1 }]) {
    const result = routeImage({ ...request, mode: 'edit', ...refs, transparent_background: true });
    assert.equal(result.backend, 'codex-native');
    assert.equal(result.tool_arguments.transparent_background, true);
  }
});

test('unsupported background modes retain the explicit API route', () => {
  const result = routeImage({ ...request, background: 'auto' });
  assert.equal(result.backend, 'paperbanana');
  assert.equal(result.request.background, 'auto');
  assert.throws(() => routeImage({ ...request, provider: 'codex-native', background: 'auto' }), /NATIVE_CANNOT/);
});

test('conflicting background controls fail before selecting a provider', () => {
  for (const extra of [{ background: 'transparent', transparent_background: false },
    { background: 'opaque', transparent_background: true },
    { background: 'auto', transparent_background: true }]) {
    assert.throws(() => routeImage({ ...request, ...extra }), /CONFLICTING_BACKGROUND_CONTROLS/);
    assert.throws(() => routeImage({ ...request, provider: 'google_imagen', ...extra }), /CONFLICTING_BACKGROUND_CONTROLS/);
  }
});

test('transparent_background must be a boolean', () => {
  for (const value of ['true', 'false', 1, 0, null, [], {}]) {
    assert.throws(() => routeImage({ ...request, transparent_background: value }), /INVALID_TRANSPARENT_BACKGROUND/);
  }
});
