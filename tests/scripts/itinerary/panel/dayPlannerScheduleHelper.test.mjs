import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { DayPlannerScheduleHelper } from '../../../../scripts/itinerary/panel/dayPlannerScheduleHelper.js';


test('Test_IsTimeWithinBounds_TestInside_ExpectTrue', () => {
   const timeValue = '10:00';
   const bounds = { minMinutes: 9 * 60, maxMinutes: 17 * 60 };

   const isWithin = DayPlannerScheduleHelper.isTimeWithinBounds(timeValue, bounds);

   const timeMinutes = DayPlannerScheduleController.parseClockTimeMinutes(timeValue);
   assert.equal(isWithin, timeMinutes >= bounds.minMinutes && timeMinutes <= bounds.maxMinutes);
});


test('Test_IsTimeWithinBounds_TestBeforeMinimum_ExpectFalse', () => {
   const timeValue = '08:00';
   const bounds = { minMinutes: 9 * 60, maxMinutes: 17 * 60 };

   const isWithin = DayPlannerScheduleHelper.isTimeWithinBounds(timeValue, bounds);

   const timeMinutes = DayPlannerScheduleController.parseClockTimeMinutes(timeValue);
   assert.equal(isWithin, timeMinutes >= bounds.minMinutes && timeMinutes <= bounds.maxMinutes);
});


test('Test_IsTimeWithinBounds_TestBlank_ExpectTrue', () => {
   const timeValue = '';
   const bounds = { minMinutes: 9 * 60, maxMinutes: 17 * 60 };

   const isWithin = DayPlannerScheduleHelper.isTimeWithinBounds(timeValue, bounds);

   assert.equal(isWithin, true);
});


test('Test_IsTimeWithinBounds_TestNullBounds_ExpectTrue', () => {
   const timeValue = '10:00';
   const bounds = null;

   const isWithin = DayPlannerScheduleHelper.isTimeWithinBounds(timeValue, bounds);

   assert.equal(isWithin, true);
});


test('Test_IsTimeWithinBounds_TestInvalidTime_ExpectFalse', () => {
   const timeValue = 'bad';
   const bounds = { minMinutes: 9 * 60, maxMinutes: 17 * 60 };

   const isWithin = DayPlannerScheduleHelper.isTimeWithinBounds(timeValue, bounds);

   assert.equal(isWithin, false);
});
