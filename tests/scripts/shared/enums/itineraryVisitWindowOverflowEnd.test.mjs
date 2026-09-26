import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryVisitWindowOverflowEnd } from '../../../../scripts/shared/enums/itineraryVisitWindowOverflowEnd.js';
import itineraryVisitWindowOverflowEndValues from '../../../../shared/enums/itineraryVisitWindowOverflowEnd.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_ItineraryVisitWindowOverflowEnd_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryVisitWindowOverflowEnd.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(itineraryVisitWindowOverflowEndValues).map((key) => [
         key,
         ItineraryVisitWindowOverflowEnd[key],
      ])
   );

   assert.deepEqual(mapped, itineraryVisitWindowOverflowEndValues);
   assert.deepEqual(itineraryVisitWindowOverflowEndValues, diskValues);
});
