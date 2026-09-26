import assert from 'node:assert/strict';
import test from 'node:test';

import { EnclosureType } from '../../../../scripts/shared/enums/enclosureType.js';
import enclosureTypeValues from '../../../../shared/enums/enclosureType.json' with { type: 'json' };


test('Test_NormalizeEnclosureType_TestIndoor_ExpectIndoor', () => {
   const value = EnclosureType.INDOOR;

   const enclosureType = EnclosureType.normalizeEnclosureType(value);

   assert.equal(enclosureType, value);
});


test('Test_NormalizeEnclosureType_TestOutdoorWhitespace_ExpectTrimmed', () => {
   const value = EnclosureType.OUTDOOR;

   const enclosureType = EnclosureType.normalizeEnclosureType(` ${value} `);

   assert.equal(enclosureType, value);
});


test('Test_NormalizeEnclosureType_TestUnknown_ExpectNull', () => {
   const value = 'Mixed';

   const enclosureType = EnclosureType.normalizeEnclosureType(value);

   assert.equal(enclosureType, null);
});


test('Test_IsEnclosureType_TestIndoor_ExpectTrue', () => {
   const value = EnclosureType.INDOOR;

   const isEnclosureType = EnclosureType.isEnclosureType(value);

   assert.equal(isEnclosureType, true);
});


test('Test_IsEnclosureType_TestUnknown_ExpectFalse', () => {
   const value = 'Yard';

   const isEnclosureType = EnclosureType.isEnclosureType(value);

   assert.equal(isEnclosureType, false);
});


test('Test_EnclosureType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const mapped = Object.fromEntries(
      Object.keys(enclosureTypeValues).map((key) => [key, EnclosureType[key]])
   );

   assert.deepEqual(mapped, enclosureTypeValues);
});
