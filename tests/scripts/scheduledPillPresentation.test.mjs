import assert from 'node:assert/strict';
import { test } from 'node:test';

import { isExtendedScheduledPill } from '../../scripts/itinerary/panel/scheduledPillPresentation.js';
import { EXTENDED_SCHEDULED_PILL_MINUTES } from '../../scripts/shared/constants.js';

test('isExtendedScheduledPill uses the half-hour slot as the threshold', () => {
   assert.equal(EXTENDED_SCHEDULED_PILL_MINUTES, 30);
   assert.equal(isExtendedScheduledPill(29), false);
   assert.equal(isExtendedScheduledPill(30), true);
});
