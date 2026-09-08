import test from 'node:test';
import assert from 'node:assert/strict';

import { ScheduleItemEventFormatter } from '../../../../scripts/itinerary/panel/scheduleItemEventFormatter.js';

test('Test_FormatItineraryEventTypeLabel_TestValues_ExpectTitleCase', () => {
   assert.equal(ScheduleItemEventFormatter.formatItineraryEventTypeLabel('lunch'), 'Lunch');
   assert.equal(ScheduleItemEventFormatter.formatItineraryEventTypeLabel('break'), 'Break');
   assert.equal(ScheduleItemEventFormatter.formatItineraryEventTypeLabel(''), '');
   assert.equal(ScheduleItemEventFormatter.formatItineraryEventTypeLabel('guardians_talk'), 'Guardians Talk');
});
