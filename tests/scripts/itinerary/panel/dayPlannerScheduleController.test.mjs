import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { DayPlannerScheduleHelper } from '../../../../scripts/itinerary/panel/dayPlannerScheduleHelper.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ParseClockTimeMinutes_TestHoursMinutes_ExpectMinutes', () => {
   const hour = 9;
   const minute = 30;
   const clockTime = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, hour * 60 + minute);
});


test('Test_ParseClockTimeMinutes_TestHoursMinutesSeconds_ExpectFractionalMinutes', () => {
   const hour = 9;
   const minute = 30;
   const second = 30;
   const clockTime = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}:${String(second).padStart(2, '0')}`;

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, hour * 60 + minute + second / 60);
});


test('Test_ParseClockTimeMinutes_TestAfternoon_ExpectMinutes', () => {
   const clockTime = '1:00 PM';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, 13 * 60);
});


test('Test_ParseClockTimeMinutes_TestMidnightMinutes_ExpectMinutes', () => {
   const clockTime = '12:15 AM';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, 15);
});


test('Test_ParseClockTimeMinutes_TestInvalidHour_ExpectNull', () => {
   const clockTime = '25:00';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, null);
});


test('Test_ParseClockTimeMinutes_TestNonClock_ExpectNull', () => {
   const clockTime = 'bad';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, null);
});


test('Test_ParseClockTimeMinutes_TestEmpty_ExpectNull', () => {
   const clockTime = '';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, null);
});


test('Test_ParseClockTimeMinutes_TestInvalidMinute_ExpectNull', () => {
   const clockTime = '1:99 PM';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, null);
});


test('Test_ParseClockTimeMinutes_TestZeroHourAm_ExpectNull', () => {
   const clockTime = '0:00 AM';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, null);
});


test('Test_ParseClockTimeMinutes_TestInvalidSecond_ExpectNull', () => {
   const clockTime = '1:00:99 PM';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, null);
});


test('Test_FormatMinutesAsScheduleTimeKey_TestMinutes_ExpectKey', () => {
   const hour = 9;
   const minute = 5;
   const minutes = hour * 60 + minute;

   const key = DayPlannerScheduleController.formatMinutesAsScheduleTimeKey(minutes);

   assert.equal(key, `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`);
});


test('Test_FormatMinutesAsClockTime_TestAfternoon_ExpectClock', () => {
   const minutes = 13 * 60;

   const clockTime = DayPlannerScheduleController.formatMinutesAsClockTime(minutes);

   assert.match(clockTime, /1:00\s*PM/i);
});


test('Test_CollectFixedZooScheduleStartMinutes_TestItems_ExpectMinutes', () => {
   const talkTime = '1:00 PM';
   const encounterTime = '10:30';
   const itinerary = {
      guardiansTalks: [
         { start_time: '11:00', is_deleted: true },
         { start_time: talkTime },
      ],
      wildEncounters: [
         { start_time: encounterTime },
         { start_time: 'bad' },
      ],
   };

   const minutes = DayPlannerScheduleController.collectFixedZooScheduleStartMinutes(itinerary);

   assert.deepEqual(
      minutes.sort((left, right) => left - right),
      [
         DayPlannerScheduleController.parseClockTimeMinutes(encounterTime),
         DayPlannerScheduleController.parseClockTimeMinutes(talkTime),
      ]
   );
});


test('Test_EarliestFixedZooScheduleStartMinutes_TestItems_ExpectEarliest', () => {
   const encounterTime = '10:30';
   const itinerary = {
      guardiansTalks: [
         { start_time: '11:00', is_deleted: true },
         { start_time: '1:00 PM' },
      ],
      wildEncounters: [
         { start_time: encounterTime },
         { start_time: 'bad' },
      ],
   };

   const minutes = DayPlannerScheduleController.earliestFixedZooScheduleStartMinutes(itinerary);

   assert.equal(minutes, DayPlannerScheduleController.parseClockTimeMinutes(encounterTime));
});


test('Test_EarliestFixedZooScheduleStartMinutes_TestEmpty_ExpectNull', () => {
   const itinerary = {};

   const minutes = DayPlannerScheduleController.earliestFixedZooScheduleStartMinutes(itinerary);

   assert.equal(minutes, null);
});


test('Test_ResolveDayPlannerTimelineStartMinutes_TestEarlyAdmission_ExpectEarly', () => {
   const earlyAdmissionTime = '09:00';
   const hours = { earlyAdmissionTime, openTime: '09:30' };
   const itinerary = { arrivalTime: '10:00' };

   const minutes = DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(hours, itinerary);

   assert.equal(minutes, DayPlannerScheduleController.parseClockTimeMinutes(earlyAdmissionTime));
});


test('Test_ResolveDayPlannerTimelineStartMinutes_TestEarlierTalk_ExpectTalk', () => {
   const talkTime = '08:45';
   const hours = { openTime: '09:30' };
   const itinerary = {
      arrivalTime: '10:00',
      guardiansTalks: [{ start_time: talkTime }],
   };

   const minutes = DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(hours, itinerary);

   assert.equal(minutes, DayPlannerScheduleController.parseClockTimeMinutes(talkTime));
});


test('Test_ResolveDayPlannerTimelineStartMinutes_TestEmpty_ExpectNull', () => {
   const hours = {};
   const itinerary = {};

   const minutes = DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(hours, itinerary);

   assert.equal(minutes, null);
});


test('Test_BuildArrivalTimeBounds_TestHours_ExpectBounds', () => {
   const earlyAdmissionTime = '09:00';
   const lastAdmissionTime = '18:00';
   const hours = {
      earlyAdmissionTime,
      openTime: '09:30',
      lastAdmissionTime,
   };

   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);

   assert.equal(bounds.minMinutes, DayPlannerScheduleController.parseClockTimeMinutes(earlyAdmissionTime));
   assert.equal(bounds.maxMinutes, DayPlannerScheduleController.parseClockTimeMinutes(lastAdmissionTime));
   assert.equal(bounds.minScheduleTime, earlyAdmissionTime);
   assert.equal(bounds.maxScheduleTime, lastAdmissionTime);
});


test('Test_BuildArrivalTimeBounds_TestInvertedHours_ExpectNull', () => {
   const hours = {
      openTime: '10:00',
      lastAdmissionTime: '09:00',
   };

   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);

   assert.equal(bounds, null);
});


test('Test_BuildDepartureTimeBounds_TestHours_ExpectBounds', () => {
   const openTime = '09:30';
   const closeTime = '19:00';
   const hours = { openTime, closeTime };

   const bounds = DayPlannerScheduleController.buildDepartureTimeBounds(hours);

   assert.equal(bounds.minMinutes, DayPlannerScheduleController.parseClockTimeMinutes(openTime));
   assert.equal(bounds.maxMinutes, DayPlannerScheduleController.parseClockTimeMinutes(closeTime));
});


test('Test_BuildDepartureTimeBounds_TestInvertedHours_ExpectNull', () => {
   const hours = {
      openTime: '19:00',
      closeTime: '09:00',
   };

   const bounds = DayPlannerScheduleController.buildDepartureTimeBounds(hours);

   assert.equal(bounds, null);
});


test('Test_IsArrivalTimeWithinBounds_TestDelegates_ExpectTrue', () => {
   const original = DayPlannerScheduleHelper.isTimeWithinBounds;
   const calls = [];
   const timeValue = '10:00';
   const bounds = { minMinutes: 9 * 60, maxMinutes: 18 * 60 };
   DayPlannerScheduleHelper.isTimeWithinBounds = (...args) => {
      calls.push(args);
      return true;
   };

   try {
      const isWithin = DayPlannerScheduleController.isArrivalTimeWithinBounds(timeValue, bounds);

      assert.equal(isWithin, true);
      assert.deepEqual(calls.at(Position.FIRST), [timeValue, bounds]);
   } finally {
      DayPlannerScheduleHelper.isTimeWithinBounds = original;
   }
});


test('Test_IsDepartureTimeWithinBounds_TestDelegates_ExpectTrue', () => {
   const original = DayPlannerScheduleHelper.isTimeWithinBounds;
   const timeValue = '16:00';
   const bounds = { minMinutes: 9 * 60, maxMinutes: 18 * 60 };
   DayPlannerScheduleHelper.isTimeWithinBounds = () => true;

   try {
      const isWithin = DayPlannerScheduleController.isDepartureTimeWithinBounds(timeValue, bounds);

      assert.equal(isWithin, true);
   } finally {
      DayPlannerScheduleHelper.isTimeWithinBounds = original;
   }
});


test('Test_AreItineraryScheduleTimesOrdered_TestArrivalBeforeDeparture_ExpectTrue', () => {
   const arrivalTime = '10:00';
   const departureTime = '16:00';

   const isOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered(
      arrivalTime,
      departureTime
   );

   assert.equal(isOrdered, true);
});


test('Test_AreItineraryScheduleTimesOrdered_TestArrivalAfterDeparture_ExpectFalse', () => {
   const arrivalTime = '16:00';
   const departureTime = '10:00';

   const isOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered(
      arrivalTime,
      departureTime
   );

   assert.equal(isOrdered, false);
});


test('Test_AreItineraryScheduleTimesOrdered_TestInvalidArrival_ExpectTrue', () => {
   const arrivalTime = 'bad';
   const departureTime = '10:00';

   const isOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered(
      arrivalTime,
      departureTime
   );

   assert.equal(isOrdered, true);
});


test('Test_ResolveArrivalTimeValidationError_TestOutOfBounds_ExpectArrivalError', () => {
   const originalArrival = DayPlannerScheduleController.isArrivalTimeWithinBounds;
   const originalOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered;
   const arrivalTimeInvalid = 'arrival bad';
   DayPlannerScheduleController.isArrivalTimeWithinBounds = () => false;
   DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => true;

   try {
      const error = DayPlannerScheduleController.resolveArrivalTimeValidationError(
         '08:00',
         {},
         '16:00',
         { arrivalTimeInvalid }
      );

      assert.equal(error, arrivalTimeInvalid);
   } finally {
      DayPlannerScheduleController.isArrivalTimeWithinBounds = originalArrival;
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = originalOrdered;
   }
});


test('Test_ResolveArrivalTimeValidationError_TestOrder_ExpectOrderError', () => {
   const originalArrival = DayPlannerScheduleController.isArrivalTimeWithinBounds;
   const originalOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered;
   const timeOrderInvalid = 'order bad';
   DayPlannerScheduleController.isArrivalTimeWithinBounds = () => true;
   DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => false;

   try {
      const error = DayPlannerScheduleController.resolveArrivalTimeValidationError(
         '17:00',
         {},
         '16:00',
         { timeOrderInvalid }
      );

      assert.equal(error, timeOrderInvalid);
   } finally {
      DayPlannerScheduleController.isArrivalTimeWithinBounds = originalArrival;
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = originalOrdered;
   }
});


test('Test_ResolveArrivalTimeValidationError_TestValid_ExpectNull', () => {
   const originalArrival = DayPlannerScheduleController.isArrivalTimeWithinBounds;
   const originalOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered;
   DayPlannerScheduleController.isArrivalTimeWithinBounds = () => true;
   DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => true;

   try {
      const error = DayPlannerScheduleController.resolveArrivalTimeValidationError(
         '10:00',
         {},
         '16:00',
         {}
      );

      assert.equal(error, null);
   } finally {
      DayPlannerScheduleController.isArrivalTimeWithinBounds = originalArrival;
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = originalOrdered;
   }
});


test('Test_ResolveDepartureTimeValidationError_TestOutOfBounds_ExpectDepartureError', () => {
   const originalDeparture = DayPlannerScheduleController.isDepartureTimeWithinBounds;
   const originalOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered;
   const departureTimeInvalid = 'departure bad';
   DayPlannerScheduleController.isDepartureTimeWithinBounds = () => false;
   DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => true;

   try {
      const error = DayPlannerScheduleController.resolveDepartureTimeValidationError(
         '20:00',
         {},
         '10:00',
         { departureTimeInvalid }
      );

      assert.equal(error, departureTimeInvalid);
   } finally {
      DayPlannerScheduleController.isDepartureTimeWithinBounds = originalDeparture;
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = originalOrdered;
   }
});


test('Test_ResolveDepartureTimeValidationError_TestOrder_ExpectAfterArrivalError', () => {
   const originalDeparture = DayPlannerScheduleController.isDepartureTimeWithinBounds;
   const originalOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered;
   const departureTimeAfterArrivalInvalid = 'after arrival';
   DayPlannerScheduleController.isDepartureTimeWithinBounds = () => true;
   DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => false;

   try {
      const error = DayPlannerScheduleController.resolveDepartureTimeValidationError(
         '09:00',
         {},
         '10:00',
         { departureTimeAfterArrivalInvalid }
      );

      assert.equal(error, departureTimeAfterArrivalInvalid);
   } finally {
      DayPlannerScheduleController.isDepartureTimeWithinBounds = originalDeparture;
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = originalOrdered;
   }
});


test('Test_ResolveDepartureTimeValidationError_TestValid_ExpectNull', () => {
   const originalDeparture = DayPlannerScheduleController.isDepartureTimeWithinBounds;
   const originalOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered;
   DayPlannerScheduleController.isDepartureTimeWithinBounds = () => true;
   DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => true;

   try {
      const error = DayPlannerScheduleController.resolveDepartureTimeValidationError(
         '16:00',
         {},
         '10:00',
         {}
      );

      assert.equal(error, null);
   } finally {
      DayPlannerScheduleController.isDepartureTimeWithinBounds = originalDeparture;
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = originalOrdered;
   }
});


test('Test_BuildHalfHourSlotStarts_TestNullStart_ExpectEmpty', () => {
   const startMinutes = null;
   const endMinutes = 10 * 60;

   const slots = DayPlannerScheduleController.buildHalfHourSlotStarts(startMinutes, endMinutes);

   assert.deepEqual(slots, []);
});


test('Test_BuildHalfHourSlotStarts_TestEqualRange_ExpectEmpty', () => {
   const minutes = 10 * 60;

   const slots = DayPlannerScheduleController.buildHalfHourSlotStarts(minutes, minutes);

   assert.deepEqual(slots, []);
});


test('Test_BuildHalfHourSlotStarts_TestOffsetOpen_ExpectSlots', () => {
   const startMinutes = 9 * 60 + 15;
   const endMinutes = 11 * 60;

   const slots = DayPlannerScheduleController.buildHalfHourSlotStarts(startMinutes, endMinutes);

   assert.equal(slots.at(Position.FIRST), startMinutes);
   assert.ok(slots.includes(9 * 60 + 30));
   assert.ok(slots.includes(10 * 60));
   assert.ok(slots.includes(10 * 60 + 30));
   assert.equal(
      slots.every((slot) => slot < endMinutes || slot === startMinutes),
      true
   );
   assert.equal(
      slots.at(Position.LAST),
      Math.floor((endMinutes - 1) / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES)
         * TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
   );
});


test('Test_BuildHalfHourSlotStarts_TestHalfHourOpen_ExpectSlots', () => {
   const startMinutes = 9 * 60;
   const endMinutes = 10 * 60 + 30;

   const slots = DayPlannerScheduleController.buildHalfHourSlotStarts(startMinutes, endMinutes);

   assert.deepEqual(slots, [startMinutes, startMinutes + TimelineLayoutConstants.TIMELINE_SLOT_MINUTES, 10 * 60]);
});
