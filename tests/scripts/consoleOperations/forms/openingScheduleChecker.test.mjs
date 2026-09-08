import assert from 'node:assert/strict';
import test from 'node:test';

import { OpeningScheduleChecker } from '../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';

test('Test_ResultHasOpeningScheduleOverlap_TestCamelAndSnakeErrorType_ExpectTrue', () => {
   assert.equal(
      OpeningScheduleChecker.resultHasOpeningScheduleOverlap({
         errorType: OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE,
      }),
      true
   );
   assert.equal(
      OpeningScheduleChecker.resultHasOpeningScheduleOverlap({
         error_type: OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE,
      }),
      true
   );
});

test('Test_ResultHasOpeningScheduleOverlap_TestOtherResults_ExpectFalse', () => {
   assert.equal(OpeningScheduleChecker.resultHasOpeningScheduleOverlap(null), false);
   assert.equal(OpeningScheduleChecker.resultHasOpeningScheduleOverlap({}), false);
   assert.equal(
      OpeningScheduleChecker.resultHasOpeningScheduleOverlap({ errorType: 'other' }),
      false
   );
});

test('Test_OpeningScheduleOverlapResolution_TestConstants_ExpectFrozenValues', () => {
   assert.equal(OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE, 'replace');
   assert.equal(OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM, 'trim');
});
