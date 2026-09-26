import assert from 'node:assert/strict';
import test from 'node:test';

import { TimelineLayoutConstants } from '../../../scripts/shared/timelineLayoutConstants.js';
import { Strings } from '../../../scripts/strings.js';


test('Test_TimelineLayoutConstants_TestExtendedPillMinutes_ExpectSlotMinutes', () => {
   const minutes = TimelineLayoutConstants.EXTENDED_SCHEDULED_PILL_MINUTES;

   assert.equal(minutes, TimelineLayoutConstants.TIMELINE_SLOT_MINUTES);
});


test('Test_TimelineLayoutConstants_TestDetailSeparator_ExpectBulletSeparator', () => {
   const separator = TimelineLayoutConstants.DETAIL_SEPARATOR;

   assert.equal(separator, Strings.format.bulletSeparator);
});


test('Test_TimelineLayoutConstants_TestMinClusterHeight_ExpectScaledSlot', () => {
   const height = TimelineLayoutConstants.TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_HEIGHT_PX;

   assert.equal(
      height,
      Math.round(
         (TimelineLayoutConstants.TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_MINUTES
            / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES)
         * TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
      )
   );
});
