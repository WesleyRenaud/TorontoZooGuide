import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduledOccurrenceSort } from '../../../../scripts/itinerary/scheduledOccurrenceSort.js';

test('Test_ScheduledOccurrenceSort_TestScheduledOccurrenceSortSortScheduledOccurrencesByStartTimeSortsSelectorRowsByStartTime_ExpectOk', () => {
   const rows = [
      { name: 'Kangaroo', start_time: '3:30 PM' },
      { name: 'Guardians of White Rhinos', start_time: '2:00 PM' },
      { name: 'Capybara', start_time: '1:30 PM' },
      { name: 'Ballin\' with the Armadillos', start_time: '11:00 AM' },
      { name: 'From Howls to Honks', start_time: '1:00 PM' },
   ];

   assert.deepEqual(
      ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(rows).map((row) => row.name),
      [
         'Ballin\' with the Armadillos',
         'From Howls to Honks',
         'Capybara',
         'Guardians of White Rhinos',
         'Kangaroo',
      ]
   );
});

test('Test_ScheduledOccurrenceSort_TestScheduledOccurrenceSortSortScheduledOccurrencesByStartTimeSortsCustomTimeFieldsAndKeeps_ExpectOk', () => {
   const rows = [
      { name: 'Missing Time' },
      { name: 'Morning', time: '10:00' },
      { name: 'Bad Time', time: 'soon' },
      { name: 'Afternoon', time: '14:00' },
   ];

   assert.deepEqual(
      ScheduledOccurrenceSort.sortScheduledOccurrencesByStartTime(
         rows,
         (row) => row.time
      ).map((row) => row.name),
      [
         'Morning',
         'Afternoon',
         'Missing Time',
         'Bad Time',
      ]
   );
});
