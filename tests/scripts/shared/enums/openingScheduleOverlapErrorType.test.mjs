import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { OpeningScheduleOverlapErrorType } from '../../../../scripts/shared/enums/openingScheduleOverlapErrorType.js';
import openingScheduleOverlapErrorTypeValues from '../../../../shared/enums/openingScheduleOverlapErrorType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_OpeningScheduleOverlapErrorType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(openingScheduleOverlapErrorTypeValues)) {
      assert.equal(OpeningScheduleOverlapErrorType[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/openingScheduleOverlapErrorType.json'), 'utf8')
   );
   assert.deepEqual(openingScheduleOverlapErrorTypeValues, diskValues);
});
