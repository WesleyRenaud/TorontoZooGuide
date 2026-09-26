import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduledPillPresenter } from '../../../../scripts/itinerary/panel/scheduledPillPresenter.js';
import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';


test('Test_IsExtendedScheduledPill_TestBelowThreshold_ExpectFalse', () => {
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES - 1;

   const isExtended = ScheduledPillPresenter.isExtendedScheduledPill(durationMinutes);

   assert.equal(isExtended, false);
});


test('Test_IsExtendedScheduledPill_TestAtThreshold_ExpectTrue', () => {
   const durationMinutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES;

   const isExtended = ScheduledPillPresenter.isExtendedScheduledPill(durationMinutes);

   assert.equal(isExtended, true);
});
