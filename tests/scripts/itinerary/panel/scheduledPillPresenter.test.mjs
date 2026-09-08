import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduledPillPresenter } from '../../../../scripts/itinerary/panel/scheduledPillPresenter.js';
import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';

test('Test_IsExtendedScheduledPill_TestHalfHourThreshold_ExpectBoundary', () => {
   assert.equal(TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES, 30);
   assert.equal(ScheduledPillPresenter.isExtendedScheduledPill(29), false);
   assert.equal(ScheduledPillPresenter.isExtendedScheduledPill(30), true);
});
