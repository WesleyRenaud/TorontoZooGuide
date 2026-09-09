import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import itineraryErrorTypeValues from '../../../../shared/enums/itineraryErrorType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_ItineraryErrorType_TestConstants_ExpectWireValues', () => {
   assert.equal(ItineraryErrorType.SUCCESS, 'success');
   assert.equal(ItineraryErrorType.SAVE_FAILED, 'saveFailed');
   assert.equal(ItineraryErrorType.ITEM_NOT_ON_ITINERARY, 'itemNotOnItinerary');
   assert.equal(ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT, 'fixedTimeItemLongWait');
});

test('Test_ItineraryErrorType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(itineraryErrorTypeValues)) {
      assert.equal(ItineraryErrorType[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryErrorType.json'), 'utf8')
   );
   assert.deepEqual(itineraryErrorTypeValues, diskValues);
});
