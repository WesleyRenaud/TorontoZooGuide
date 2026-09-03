import assert from 'node:assert/strict';
import test from 'node:test';

import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';

test('normalizes seeded names into asset-safe keys', () => {
   assert.equal(AssetKeyNormalizer.normalize('Ballin\' with the Armadillos'), 'ballin-with-the-armadillos');
   assert.equal(
      AssetKeyNormalizer.normalize('Wildlife Health & Science Centre'),
      'wildlife-health-and-science-centre'
   );
   assert.equal(
      AssetKeyNormalizer.normalize('Virtual Reality (VR) Theatre!'),
      'virtual-reality-vr-theatre'
   );
   assert.equal(
      AssetKeyNormalizer.normalize('Mantella (Poison Frog)'),
      'mantella-poison-frog'
   );
});

test('normalizes punctuation, accents, and repeated spacing', () => {
   assert.equal(AssetKeyNormalizer.normalize('  Café   Zootique  '), 'cafe-zootique');
   assert.equal(AssetKeyNormalizer.normalize('Guardians of Snow Leopards'), 'guardians-of-snow-leopards');
   assert.equal(AssetKeyNormalizer.normalize(null), '');
});
