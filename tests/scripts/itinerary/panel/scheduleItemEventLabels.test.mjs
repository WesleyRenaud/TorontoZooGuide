import test from 'node:test';
import assert from 'node:assert/strict';

import { ScheduleItemEventLabels } from '../../../../scripts/itinerary/panel/scheduleItemEventLabels.js';

test('Test_FormatItineraryEventTypeLabel_TestValues_ExpectTitleCase', () => {
   assert.equal(ScheduleItemEventLabels.formatItineraryEventTypeLabel('lunch'), 'Lunch');
   assert.equal(ScheduleItemEventLabels.formatItineraryEventTypeLabel('break'), 'Break');
   assert.equal(ScheduleItemEventLabels.formatItineraryEventTypeLabel(''), '');
   assert.equal(ScheduleItemEventLabels.formatItineraryEventTypeLabel('guardians_talk'), 'Guardians Talk');
});
