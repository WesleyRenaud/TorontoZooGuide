import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { OpeningScheduleOverlapErrorType } from '../../../../scripts/shared/enums/openingScheduleOverlapErrorType.js';
import openingScheduleOverlapErrorTypeValues from '../../../../shared/enums/openingScheduleOverlapErrorType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_OpeningScheduleOverlapErrorType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/openingScheduleOverlapErrorType.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(openingScheduleOverlapErrorTypeValues).map((key) => [
         key,
         OpeningScheduleOverlapErrorType[key],
      ])
   );

   assert.deepEqual(mapped, openingScheduleOverlapErrorTypeValues);
   assert.deepEqual(openingScheduleOverlapErrorTypeValues, diskValues);
});
