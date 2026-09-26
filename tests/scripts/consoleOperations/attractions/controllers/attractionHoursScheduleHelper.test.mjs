import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionHoursScheduleHelper } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionHoursScheduleHelper.js';
import { DayPlannerScheduleController } from '../../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';


test('Test_TimePairIsOrdered_TestOrderedTimes_ExpectTrue', () => {
   const startTime = '09:00';
   const endTime = '17:00';

   const isOrdered = AttractionHoursScheduleHelper.timePairIsOrdered(startTime, endTime);

   assert.equal(
      isOrdered,
      DayPlannerScheduleController.parseClockTimeMinutes(startTime)
         < DayPlannerScheduleController.parseClockTimeMinutes(endTime)
   );
});


test('Test_TimePairIsOrdered_TestReversedTimes_ExpectFalse', () => {
   const startTime = '17:00';
   const endTime = '09:00';

   const isOrdered = AttractionHoursScheduleHelper.timePairIsOrdered(startTime, endTime);

   assert.equal(isOrdered, false);
});


test('Test_TimePairIsOrdered_TestInvalidStart_ExpectFalse', () => {
   const startTime = 'bad';
   const endTime = '17:00';

   const isOrdered = AttractionHoursScheduleHelper.timePairIsOrdered(startTime, endTime);

   assert.equal(isOrdered, false);
});
