import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduledPillPresentation } from '../../../../scripts/itinerary/panel/scheduledPillPresentation.js';
import { Constants } from '../../../../scripts/shared/constants.js';

test('Test_IsExtendedScheduledPill_TestHalfHourThreshold_ExpectBoundary', () => {
   assert.equal(Constants.EXTENDED_SCHEDULED_PILL_MINUTES, 30);
   assert.equal(ScheduledPillPresentation.isExtendedScheduledPill(29), false);
   assert.equal(ScheduledPillPresentation.isExtendedScheduledPill(30), true);
});
