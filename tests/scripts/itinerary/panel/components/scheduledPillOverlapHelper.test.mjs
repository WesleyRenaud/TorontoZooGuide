import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledPillOverlapHelper } from '../../../../../scripts/itinerary/panel/components/scheduledPillOverlapHelper.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';


test('Test_MinutesPerSlotFromHeightPx_TestSlotHeight_ExpectSlotMinutes', () => {
   const heightPx = TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX;

   const minutes = ScheduledPillOverlapHelper.minutesPerSlotFromHeightPx(heightPx);

   assert.equal(minutes, TimelineLayoutConstants.TIMELINE_SLOT_MINUTES);
});


test('Test_MinutesPerSlotFromHeightPx_TestHalfSlotHeight_ExpectHalfSlotMinutes', () => {
   const heightPx = TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX / 2;

   const minutes = ScheduledPillOverlapHelper.minutesPerSlotFromHeightPx(heightPx);

   assert.equal(minutes, TimelineLayoutConstants.TIMELINE_SLOT_MINUTES / 2);
});
