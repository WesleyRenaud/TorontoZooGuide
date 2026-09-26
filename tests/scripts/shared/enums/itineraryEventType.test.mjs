import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryEventType } from '../../../../scripts/shared/enums/itineraryEventType.js';
import itineraryEventTypeValues from '../../../../shared/enums/itineraryEventType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_ItineraryEventType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryEventType.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(itineraryEventTypeValues).map((key) => [key, ItineraryEventType[key]])
   );

   assert.deepEqual(mapped, itineraryEventTypeValues);
   assert.deepEqual(itineraryEventTypeValues, diskValues);
});
