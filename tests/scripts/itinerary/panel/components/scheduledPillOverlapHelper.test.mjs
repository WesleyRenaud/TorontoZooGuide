import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledPillOverlapHelper } from '../../../../../scripts/itinerary/panel/components/scheduledPillOverlapHelper.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';

test('Test_MinutesPerSlotFromHeightPx_TestHeight_ExpectScaledMinutes', () => {
   assert.equal(
      ScheduledPillOverlapHelper.minutesPerSlotFromHeightPx(
         TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
      ),
      TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
   );
   assert.equal(
      ScheduledPillOverlapHelper.minutesPerSlotFromHeightPx(
         TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX / 2
      ),
      TimelineLayoutConstants.TIMELINE_SLOT_MINUTES / 2
   );
});
