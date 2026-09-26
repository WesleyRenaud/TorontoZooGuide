import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryAdjustmentType } from '../../../../scripts/shared/enums/itineraryAdjustmentType.js';
import itineraryAdjustmentTypeValues from '../../../../shared/enums/itineraryAdjustmentType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_Normalize_TestArrivalTimeAdjusted_ExpectMatched', () => {
   const adjustmentType = ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED;

   const normalized = ItineraryAdjustmentType.normalize(adjustmentType);

   assert.equal(normalized, adjustmentType);
});


test('Test_Normalize_TestDepartureWhitespace_ExpectTrimmed', () => {
   const adjustmentType = ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED;

   const normalized = ItineraryAdjustmentType.normalize(`  ${adjustmentType}  `);

   assert.equal(normalized, adjustmentType);
});


test('Test_Normalize_TestCustom_ExpectPassthrough', () => {
   const adjustmentType = 'custom';

   const normalized = ItineraryAdjustmentType.normalize(adjustmentType);

   assert.equal(normalized, adjustmentType);
});


test('Test_Normalize_TestEmpty_ExpectEmpty', () => {
   const adjustmentType = '';

   const normalized = ItineraryAdjustmentType.normalize(adjustmentType);

   assert.equal(normalized, adjustmentType);
});


test('Test_ItineraryAdjustmentType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryAdjustmentType.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(itineraryAdjustmentTypeValues).map((key) => [key, ItineraryAdjustmentType[key]])
   );

   assert.deepEqual(mapped, itineraryAdjustmentTypeValues);
   assert.deepEqual(itineraryAdjustmentTypeValues, diskValues);
});
