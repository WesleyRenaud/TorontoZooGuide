import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import itineraryErrorTypeValues from '../../../../shared/enums/itineraryErrorType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_ItineraryErrorType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itineraryErrorType.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(itineraryErrorTypeValues).map((key) => [key, ItineraryErrorType[key]])
   );

   assert.deepEqual(mapped, itineraryErrorTypeValues);
   assert.deepEqual(itineraryErrorTypeValues, diskValues);
});
