import assert from 'node:assert/strict';
import test from 'node:test';

import { TimelineLayoutConstants } from '../../../scripts/shared/timelineLayoutConstants.js';

test('Test_TimelineLayoutConstants_TestSlotMetrics_ExpectValues', () => {
   assert.equal(TimelineLayoutConstants.TIMELINE_SLOT_MINUTES, 30);
   assert.equal(TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES, 30);
   assert.equal(TimelineLayoutConstants.DETAIL_SEPARATOR, ' \u2022 ');
   assert.equal(TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX, 730);
   assert.equal(TimelineLayoutConstants.TIMELINE_PILL_STRIP_TOP_OFFSET_PX, 80);
   assert.equal(TimelineLayoutConstants.TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_MINUTES, 3);
   assert.equal(TimelineLayoutConstants.TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_HEIGHT_PX, 73);
   assert.equal(TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX, 153);
   assert.equal(TimelineLayoutConstants.MAX_TIMELINE_PILL_COLUMNS, 2);
   assert.equal(TimelineLayoutConstants.DAY_PLANNER_ACTION_FEEDBACK_DISMISS_MS, 2500);
});
