import test from 'node:test';
import assert from 'node:assert/strict';

import { formatItineraryEventTypeLabel } from '../../scripts/itinerary/panel/scheduleItemEventLabels.js';

test('formatItineraryEventTypeLabel title-cases event type values', () => {
   assert.equal(formatItineraryEventTypeLabel('lunch'), 'Lunch');
   assert.equal(formatItineraryEventTypeLabel('break'), 'Break');
});
