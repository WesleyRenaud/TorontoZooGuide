import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   formatScheduledPillTimeRange,
   isExtendedScheduledPill,
} from '../../scripts/itinerary/panel/scheduledPillPresentation.js';
import { EXTENDED_SCHEDULED_PILL_MINUTES } from '../../scripts/shared/constants.js';

test('isExtendedScheduledPill uses the half-hour slot as the threshold', () => {
   assert.equal(EXTENDED_SCHEDULED_PILL_MINUTES, 30);
   assert.equal(isExtendedScheduledPill(29), false);
   assert.equal(isExtendedScheduledPill(30), true);
});

test('formatScheduledPillTimeRange formats start and end labels', () => {
   assert.equal(
      formatScheduledPillTimeRange('12:00', '12:40'),
      '12:00 PM – 12:40 PM'
   );
   assert.equal(formatScheduledPillTimeRange('12:00', ''), '');
});
