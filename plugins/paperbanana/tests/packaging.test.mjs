import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const root = new URL('../../../', import.meta.url);
const read = (path) => readFileSync(new URL(path, root), 'utf8');

test('discovery wrappers resolve to canonical skills with packaged routing references', () => {
  assert.match(read('SKILL.md'), /plugins\/paperbanana\/skills\/paperbanana\/SKILL\.md/);
  assert.match(read('plugins/paperbanana/skills/paperbanana/SKILL.md'), /references\/image-routing\.md/);
  assert.match(read('plugins/paperbanana-slide-deck/SKILL.md'), /references\/image-routing\.md/);
  assert.match(read('plugins/paperbanana-slide-deck/skills/paperbanana-slide-deck/SKILL.md'), /\.\.\/\.\.\/SKILL\.md/);
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
