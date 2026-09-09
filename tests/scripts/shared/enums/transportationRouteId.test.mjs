import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { TransportationRouteId } from '../../../../scripts/shared/enums/transportationRouteId.js';
import transportationRouteIdValues from '../../../../shared/enums/transportationRouteId.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_TransportationRouteId_TestConstants_ExpectWireValues', () => {
   assert.equal(TransportationRouteId.SUMMER, 'summer');
   assert.equal(TransportationRouteId.WINTER, 'winter');
});

test('Test_TransportationRouteId_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(transportationRouteIdValues)) {
      assert.equal(TransportationRouteId[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/transportationRouteId.json'), 'utf8')
   );
   assert.deepEqual(transportationRouteIdValues, diskValues);
});
