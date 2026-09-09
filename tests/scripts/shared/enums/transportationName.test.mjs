import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { TransportationName } from '../../../../scripts/shared/enums/transportationName.js';
import transportationNameValues from '../../../../shared/enums/transportationName.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_TransportationName_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(transportationNameValues)) {
      assert.equal(TransportationName[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/transportationName.json'), 'utf8')
   );
   assert.deepEqual(transportationNameValues, diskValues);
});
