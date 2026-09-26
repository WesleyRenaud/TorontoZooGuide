import test from 'node:test';
import assert from 'node:assert/strict';

import { ScheduleItemEventFormatter } from '../../../../scripts/itinerary/panel/scheduleItemEventFormatter.js';


test('Test_FormatItineraryEventTypeLabel_TestLunch_ExpectTitleCase', () => {
   const eventType = 'lunch';

   const label = ScheduleItemEventFormatter.formatItineraryEventTypeLabel(eventType);

   assert.equal(label, `${eventType.charAt(0).toUpperCase()}${eventType.slice(1)}`);
});


test('Test_FormatItineraryEventTypeLabel_TestBreak_ExpectTitleCase', () => {
   const eventType = 'break';

   const label = ScheduleItemEventFormatter.formatItineraryEventTypeLabel(eventType);

   assert.equal(label, `${eventType.charAt(0).toUpperCase()}${eventType.slice(1)}`);
});


test('Test_FormatItineraryEventTypeLabel_TestEmpty_ExpectEmpty', () => {
   const eventType = '';

   const label = ScheduleItemEventFormatter.formatItineraryEventTypeLabel(eventType);

   assert.equal(label, eventType);
});


test('Test_FormatItineraryEventTypeLabel_TestGuardiansTalk_ExpectSpacedTitleCase', () => {
   const firstWord = 'guardians';
   const secondWord = 'talk';
   const eventType = `${firstWord}_${secondWord}`;

   const label = ScheduleItemEventFormatter.formatItineraryEventTypeLabel(eventType);

   assert.equal(
      label,
      `${firstWord.charAt(0).toUpperCase()}${firstWord.slice(1)} ${secondWord.charAt(0).toUpperCase()}${secondWord.slice(1)}`
   );
});
