import assert from 'node:assert/strict';
import test from 'node:test';

import { EnclosureType } from '../../../../scripts/shared/enums/enclosureType.js';

test('Test_NormalizeEnclosureType_TestValues_ExpectNormalizedOrNull', () => {
   assert.equal(EnclosureType.normalizeEnclosureType('Indoor'), EnclosureType.INDOOR);
   assert.equal(EnclosureType.normalizeEnclosureType(' Outdoor '), EnclosureType.OUTDOOR);
   assert.equal(EnclosureType.normalizeEnclosureType('Mixed'), null);
});

test('Test_IsEnclosureType_TestValues_ExpectBoolean', () => {
   assert.equal(EnclosureType.isEnclosureType('Indoor'), true);
   assert.equal(EnclosureType.isEnclosureType('Yard'), false);
});
