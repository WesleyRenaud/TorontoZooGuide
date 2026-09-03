import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   sortScheduledOccurrencesByStartTime,
} from '../../scripts/itinerary/scheduledOccurrenceSort.js';

test('sortScheduledOccurrencesByStartTime sorts selector rows by start time', () => {
   const rows = [
      { name: 'Kangaroo', start_time: '3:30 PM' },
      { name: 'Guardians of White Rhinos', start_time: '2:00 PM' },
      { name: 'Capybara', start_time: '1:30 PM' },
      { name: 'Ballin\' with the Armadillos', start_time: '11:00 AM' },
      { name: 'From Howls to Honks', start_time: '1:00 PM' },
   ];

   assert.deepEqual(
      sortScheduledOccurrencesByStartTime(rows).map((row) => row.name),
      [
         'Ballin\' with the Armadillos',
         'From Howls to Honks',
         'Capybara',
         'Guardians of White Rhinos',
         'Kangaroo',
      ]
   );
});

test('sortScheduledOccurrencesByStartTime sorts custom time fields and keeps bad times last', () => {
   const rows = [
      { name: 'Missing Time' },
      { name: 'Morning', time: '10:00' },
      { name: 'Bad Time', time: 'soon' },
      { name: 'Afternoon', time: '14:00' },
   ];

   assert.deepEqual(
      sortScheduledOccurrencesByStartTime(
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
