import assert from 'node:assert/strict';
import test from 'node:test';

import { AssetKeyNormalizer } from '../../../scripts/assets/assetKeyNormalizer.js';


test('Test_Normalize_TestArmadillos_ExpectAssetSafeKey', () => {
   const name = 'Ballin\' with the Armadillos';

   const key = AssetKeyNormalizer.normalize(name);

   assert.equal(key, 'ballin-with-the-armadillos');
});


test('Test_Normalize_TestScienceCentre_ExpectAndExpanded', () => {
   const name = 'Wildlife Health & Science Centre';

   const key = AssetKeyNormalizer.normalize(name);

   assert.equal(key, 'wildlife-health-and-science-centre');
});


test('Test_Normalize_TestVirtualRealityTheatre_ExpectStrippedPunctuation', () => {
   const name = 'Virtual Reality (VR) Theatre!';

   const key = AssetKeyNormalizer.normalize(name);

   assert.equal(key, 'virtual-reality-vr-theatre');
});


test('Test_Normalize_TestMantella_ExpectStrippedParens', () => {
   const name = 'Mantella (Poison Frog)';

   const key = AssetKeyNormalizer.normalize(name);

   assert.equal(key, 'mantella-poison-frog');
});


test('Test_Normalize_TestCafeWhitespace_ExpectCollapsedKey', () => {
   const name = '  Café   Zootique  ';

   const key = AssetKeyNormalizer.normalize(name);

   assert.equal(key, 'cafe-zootique');
});


test('Test_Normalize_TestGuardiansTalk_ExpectAssetSafeKey', () => {
   const name = 'Guardians of Snow Leopards';

   const key = AssetKeyNormalizer.normalize(name);

   assert.equal(key, 'guardians-of-snow-leopards');
});


test('Test_Normalize_TestNull_ExpectEmpty', () => {
   const name = null;

   const key = AssetKeyNormalizer.normalize(name);

   assert.equal(key, '');
});
