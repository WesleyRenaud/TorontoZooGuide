import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryEventType } from '../../../../scripts/shared/enums/itineraryEventType.js';
import itineraryEventTypeValues from '../../../../shared/enums/itineraryEventType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_ItineraryEventType_TestConstants_ExpectWireValues', () => {
   assert.equal(ItineraryEventType.ARRIVAL, 'arrival');
   assert.equal(ItineraryEventType.DEPARTURE, 'departure');
   assert.equal(ItineraryEventType.LUNCH, 'lunch');
   assert.equal(ItineraryEventType.BREAK, 'break');
});

test('Test_ItineraryEventType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(itineraryEventTypeValues)) {
      assert.equal(ItineraryEventType[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryEventType.json'), 'utf8')
   );
   assert.deepEqual(itineraryEventTypeValues, diskValues);
});
