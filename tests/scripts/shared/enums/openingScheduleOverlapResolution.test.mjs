import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { OpeningScheduleOverlapResolution } from '../../../../scripts/shared/enums/openingScheduleOverlapResolution.js';
import openingScheduleOverlapResolutionValues from '../../../../shared/enums/openingScheduleOverlapResolution.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_OpeningScheduleOverlapResolution_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(openingScheduleOverlapResolutionValues)) {
      assert.equal(OpeningScheduleOverlapResolution[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/openingScheduleOverlapResolution.json'), 'utf8')
   );
   assert.deepEqual(openingScheduleOverlapResolutionValues, diskValues);
});
