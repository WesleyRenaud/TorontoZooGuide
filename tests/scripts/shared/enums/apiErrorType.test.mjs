import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ApiErrorType } from '../../../../scripts/shared/enums/apiErrorType.js';
import apiErrorTypeValues from '../../../../shared/enums/apiErrorType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');

test('Test_ApiErrorType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   for (const [key, value] of Object.entries(apiErrorTypeValues)) {
      assert.equal(ApiErrorType[key], value);
   }

   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/apiErrorType.json'), 'utf8')
   );
   assert.deepEqual(apiErrorTypeValues, diskValues);
});
