import assert from 'node:assert/strict';
import { test } from 'node:test';

import { BulkScheduleItineraryNotEnoughTimeFragment } from '../../../../scripts/itinerary/panel/bulkScheduleItineraryNotEnoughTimeFragment.js';


test('Test_HasBulkScheduleItineraryNotEnoughTimeIssue_TestEmpty_ExpectFalse', () => {
   const issues = [];

   const hasIssue = BulkScheduleItineraryNotEnoughTimeFragment.hasBulkScheduleItineraryNotEnoughTimeIssue(
      issues
   );

   assert.equal(hasIssue, false);
});


test('Test_HasBulkScheduleItineraryNotEnoughTimeIssue_TestMatchingType_ExpectTrue', () => {
   const issues = [
      {
         type: BulkScheduleItineraryNotEnoughTimeFragment.BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME_ISSUE,
         items: [],
      },
   ];

   const hasIssue = BulkScheduleItineraryNotEnoughTimeFragment.hasBulkScheduleItineraryNotEnoughTimeIssue(
      issues
   );

   assert.equal(hasIssue, true);
});


test('Test_HasBulkScheduleItineraryNotEnoughTimeIssue_TestOtherType_ExpectFalse', () => {
   const issues = [{ type: 'otherIssue', items: [] }];

   const hasIssue = BulkScheduleItineraryNotEnoughTimeFragment.hasBulkScheduleItineraryNotEnoughTimeIssue(
      issues
   );

   assert.equal(hasIssue, false);
});
