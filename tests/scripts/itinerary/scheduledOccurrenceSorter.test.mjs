import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledOccurrenceSorter } from '../../../scripts/itinerary/scheduledOccurrenceSorter.js';

test('Test_SortScheduledOccurrencesByStartTime_TestRows_ExpectOrdered', () => {
   assert.deepEqual(
      ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime([
         { name: 'B', start_time: '13:00' },
         { name: 'A', start_time: '09:00' },
         { name: 'C', start_time: '' },
      ]).map((row) => row.name),
      ['A', 'B', 'C']
   );
   assert.deepEqual(ScheduledOccurrenceSorter.sortScheduledOccurrencesByStartTime(null), []);
});
