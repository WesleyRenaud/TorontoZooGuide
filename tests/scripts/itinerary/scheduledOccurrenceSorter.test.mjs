import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledOccurrenceSorter } from '../../../scripts/itinerary/scheduledOccurrenceSorter.js';


test('Test_SortScheduledOccurrencesByStartTime_TestRows_ExpectOrdered', () => {
   const first = { name: 'African Lion Talk', start_time: '09:00' };
   const second = { name: 'Zoomobile', start_time: '13:00' };
   const untimed = { name: 'Conservation Carousel', start_time: '' };
   const rows = [second, first, untimed];

   const sorted = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(rows);

   assert.deepEqual(
      sorted.map((row) => row.name),
      [first.name, second.name, untimed.name]
   );
});


test('Test_SortScheduledOccurrencesByStartTime_TestNull_ExpectEmpty', () => {
   const rows = null;

   const sorted = ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(rows);

   assert.deepEqual(sorted, []);
});
