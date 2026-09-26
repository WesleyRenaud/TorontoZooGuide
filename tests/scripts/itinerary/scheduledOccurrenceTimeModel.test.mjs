import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledOccurrenceTimeModel } from '../../../scripts/itinerary/scheduledOccurrenceTimeModel.js';


test('Test_BuildScheduledOccurrenceTimeRange_TestStartOnly_ExpectDisplay', () => {
   const startTime = '13:00';
   const occurrence = { start_time: startTime };

   const display = ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange(occurrence);

   assert.equal(display, '1:00 PM');
});


test('Test_BuildScheduledOccurrenceTimeRange_TestRange_ExpectDisplay', () => {
   const startTime = '13:00';
   const endTime = '13:30';
   const occurrence = { start_time: startTime, end_time: endTime };

   const display = ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange(occurrence);

   assert.equal(display, '1:00 PM - 1:30 PM');
});


test('Test_BuildScheduledOccurrenceTimeRange_TestMissing_ExpectEmpty', () => {
   const occurrence = {};

   const display = ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange(occurrence);

   assert.equal(display, '');
});
