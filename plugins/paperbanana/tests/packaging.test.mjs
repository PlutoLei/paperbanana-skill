import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const root = new URL('../../../', import.meta.url);
const read = (path) => readFileSync(new URL(path, root), 'utf8');

test('root and packaged skill carry the same routing instructions', () => {
  assert.equal(read('SKILL.md'), read('plugins/paperbanana/skills/paperbanana/SKILL.md'));
  const guide = read('references/image-routing.md');
  assert.equal(guide, read('plugins/paperbanana/skills/paperbanana/references/image-routing.md'));
  assert.equal(guide, read('plugins/paperbanana-slide-deck/references/image-routing.md'));
});

test('marketplace versions match shipped plugin manifests', () => {
  const market = JSON.parse(read('.claude-plugin/marketplace.json'));
  for (const plugin of market.plugins) {
    assert.equal(plugin.version, JSON.parse(read(`plugins/${plugin.name}/.claude-plugin/plugin.json`)).version);
  }
});
