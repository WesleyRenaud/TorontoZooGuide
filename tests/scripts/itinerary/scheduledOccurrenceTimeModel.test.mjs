import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledOccurrenceTimeModel } from '../../../scripts/itinerary/scheduledOccurrenceTimeModel.js';

test('Test_BuildScheduledOccurrenceTimeRange_TestStartOnlyAndRange_ExpectDisplay', () => {
   assert.equal(
      ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange({ start_time: '13:00' }),
      '1:00 PM'
   );
   assert.equal(
      ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange({
         start_time: '13:00',
         end_time: '13:30',
      }),
      '1:00 PM - 1:30 PM'
   );
   assert.equal(
      ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange({}),
      ''
   );
});
