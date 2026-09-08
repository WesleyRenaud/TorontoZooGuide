import assert from 'node:assert/strict';
import { test } from 'node:test';

import { BulkScheduleItineraryNotEnoughTimeFragment } from '../../../../scripts/itinerary/panel/bulkScheduleItineraryNotEnoughTimeFragment.js';

test('Test_HasBulkScheduleItineraryNotEnoughTimeIssue_TestBackendIssueType_ExpectDetected', () => {
   assert.equal(
      BulkScheduleItineraryNotEnoughTimeFragment.hasBulkScheduleItineraryNotEnoughTimeIssue([]),
      false
   );
   assert.equal(
      BulkScheduleItineraryNotEnoughTimeFragment.hasBulkScheduleItineraryNotEnoughTimeIssue([
         {
            type: BulkScheduleItineraryNotEnoughTimeFragment
               .BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME_ISSUE,
            items: [],
         },
      ]),
      true
   );
   assert.equal(
      BulkScheduleItineraryNotEnoughTimeFragment.hasBulkScheduleItineraryNotEnoughTimeIssue([
         { type: 'otherIssue', items: [] },
      ]),
      false
   );
});
