import assert from 'node:assert/strict';
import test from 'node:test';

import { OpeningScheduleChecker } from '../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapErrorType } from '../../../../scripts/shared/enums/openingScheduleOverlapErrorType.js';
import { OpeningScheduleOverlapResolution } from '../../../../scripts/shared/enums/openingScheduleOverlapResolution.js';


test('Test_ResultHasOpeningScheduleOverlap_TestCamelErrorType_ExpectTrue', () => {
   const result = { errorType: OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE };

   const hasOverlap = OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result);

   assert.equal(hasOverlap, true);
});


test('Test_ResultHasOpeningScheduleOverlap_TestSnakeErrorType_ExpectTrue', () => {
   const result = { error_type: OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE };

   const hasOverlap = OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result);

   assert.equal(hasOverlap, true);
});


test('Test_ResultHasOpeningScheduleOverlap_TestNull_ExpectFalse', () => {
   const result = null;

   const hasOverlap = OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result);

   assert.equal(hasOverlap, false);
});


test('Test_ResultHasOpeningScheduleOverlap_TestEmptyObject_ExpectFalse', () => {
   const result = {};

   const hasOverlap = OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result);

   assert.equal(hasOverlap, false);
});


test('Test_ResultHasOpeningScheduleOverlap_TestOtherErrorType_ExpectFalse', () => {
   const result = { errorType: 'other' };

   const hasOverlap = OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result);

   assert.equal(hasOverlap, false);
});


test('Test_OpeningScheduleOverlapEnums_TestErrorType_ExpectSharedReference', () => {
   const errorType = OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_ERROR_TYPE;

   assert.equal(errorType, OpeningScheduleOverlapErrorType.OVERLAPPING_SCHEDULE);
});


test('Test_OpeningScheduleOverlapEnums_TestResolution_ExpectSharedReference', () => {
   const resolution = OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION;

   assert.equal(resolution, OpeningScheduleOverlapResolution);
});
