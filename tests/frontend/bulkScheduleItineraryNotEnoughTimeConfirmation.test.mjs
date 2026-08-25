import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME_ISSUE,
   hasBulkScheduleItineraryNotEnoughTimeIssue,
} from '../../scripts/itinerary/panel/bulkScheduleItineraryNotEnoughTimeConfirmation.js';

test('hasBulkScheduleItineraryNotEnoughTimeIssue detects backend issue type', () => {
   assert.equal(hasBulkScheduleItineraryNotEnoughTimeIssue([]), false);
   assert.equal(
      hasBulkScheduleItineraryNotEnoughTimeIssue([
         { type: BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME_ISSUE, items: [] },
      ]),
      true
   );
   assert.equal(
      hasBulkScheduleItineraryNotEnoughTimeIssue([{ type: 'otherIssue', items: [] }]),
      false
   );
});
