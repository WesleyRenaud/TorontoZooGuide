import assert from 'node:assert/strict';
import test from 'node:test';

import { normalizeAssetKey } from '../../scripts/assets/normalizeAssetKey.js';

test('normalizes seeded names into asset-safe keys', () => {
   assert.equal(normalizeAssetKey('Ballin\' with the Armadillos'), 'ballin-with-the-armadillos');
   assert.equal(
      normalizeAssetKey('Wildlife Health & Science Centre'),
      'wildlife-health-and-science-centre'
   );
   assert.equal(
      normalizeAssetKey('Virtual Reality (VR) Theatre!'),
      'virtual-reality-vr-theatre'
   );
   assert.equal(
      normalizeAssetKey('Mantella (Poison Frog)'),
      'mantella-poison-frog'
   );
});

test('normalizes punctuation, accents, and repeated spacing', () => {
   assert.equal(normalizeAssetKey('  Café   Zootique  '), 'cafe-zootique');
   assert.equal(normalizeAssetKey('Guardians of Snow Leopards'), 'guardians-of-snow-leopards');
   assert.equal(normalizeAssetKey(null), '');
});
