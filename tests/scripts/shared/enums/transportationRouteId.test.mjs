import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { TransportationRouteId } from '../../../../scripts/shared/enums/transportationRouteId.js';
import transportationRouteIdValues from '../../../../shared/enums/transportationRouteId.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_TransportationRouteId_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/transportationRouteId.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(transportationRouteIdValues).map((key) => [key, TransportationRouteId[key]])
   );

   assert.deepEqual(mapped, transportationRouteIdValues);
   assert.deepEqual(transportationRouteIdValues, diskValues);
});
