import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryAdjustmentType } from '../../../../scripts/shared/enums/itineraryAdjustmentType.js';
import itineraryAdjustmentTypeValues from '../../../../shared/enums/itineraryAdjustmentType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_ItineraryAdjustmentType_TestConstants_ExpectWireValues', () => {
   assert.equal(ItineraryAdjustmentType.ARRIVAL_TIME_ADJUSTED, 'arrivalTimeAdjusted');
   assert.equal(ItineraryAdjustmentType.DEPARTURE_TIME_ADJUSTED, 'departureTimeAdjusted');
});

test('Test_ItineraryAdjustmentType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(itineraryAdjustmentTypeValues)) {
      assert.equal(ItineraryAdjustmentType[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryAdjustmentType.json'), 'utf8')
   );
   assert.deepEqual(itineraryAdjustmentTypeValues, diskValues);
});
