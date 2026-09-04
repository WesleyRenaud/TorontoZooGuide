import assert from 'node:assert/strict';
import { test } from 'node:test';

import { BulkScheduleItineraryNotEnoughTimeConfirmation } from '../../../../scripts/itinerary/panel/bulkScheduleItineraryNotEnoughTimeConfirmation.js';

test('Test_HasBulkScheduleItineraryNotEnoughTimeIssue_TestBackendIssueType_ExpectDetected', () => {
   assert.equal(
      BulkScheduleItineraryNotEnoughTimeConfirmation.hasBulkScheduleItineraryNotEnoughTimeIssue([]),
      false
   );
   assert.equal(
      BulkScheduleItineraryNotEnoughTimeConfirmation.hasBulkScheduleItineraryNotEnoughTimeIssue([
         {
            type: BulkScheduleItineraryNotEnoughTimeConfirmation
               .BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME_ISSUE,
            items: [],
         },
      ]),
      true
   );
   assert.equal(
      BulkScheduleItineraryNotEnoughTimeConfirmation.hasBulkScheduleItineraryNotEnoughTimeIssue([
         { type: 'otherIssue', items: [] },
      ]),
      false
   );
});
