import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME_ISSUE,
   hasBulkScheduleAnimalsNotEnoughTimeIssue,
} from '../../scripts/itinerary/panel/bulkScheduleAnimalsNotEnoughTimeConfirmation.js';

test('hasBulkScheduleAnimalsNotEnoughTimeIssue detects backend issue type', () => {
   assert.equal(hasBulkScheduleAnimalsNotEnoughTimeIssue([]), false);
   assert.equal(
      hasBulkScheduleAnimalsNotEnoughTimeIssue([
         { type: BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME_ISSUE, items: [] },
      ]),
      true
   );
   assert.equal(
      hasBulkScheduleAnimalsNotEnoughTimeIssue([{ type: 'otherIssue', items: [] }]),
      false
   );
});
