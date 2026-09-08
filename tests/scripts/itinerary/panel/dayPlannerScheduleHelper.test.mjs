import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduleHelper } from '../../../../scripts/itinerary/panel/dayPlannerScheduleHelper.js';

test('Test_IsTimeWithinBounds_TestBounds_ExpectBoolean', () => {
   const bounds = { minMinutes: 9 * 60, maxMinutes: 17 * 60 };

   assert.equal(DayPlannerScheduleHelper.isTimeWithinBounds('10:00', bounds), true);
   assert.equal(DayPlannerScheduleHelper.isTimeWithinBounds('08:00', bounds), false);
   assert.equal(DayPlannerScheduleHelper.isTimeWithinBounds('', bounds), true);
   assert.equal(DayPlannerScheduleHelper.isTimeWithinBounds('10:00', null), true);
   assert.equal(DayPlannerScheduleHelper.isTimeWithinBounds('bad', bounds), false);
});
