import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { DayPlannerScheduleHelper } from '../../../../scripts/itinerary/panel/dayPlannerScheduleHelper.js';
import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ParseClockTimeMinutes_TestFormats_ExpectMinutes', () => {
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('09:30'), 9 * 60 + 30);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('09:30:30'), 9 * 60 + 30.5);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('1:00 PM'), 13 * 60);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('12:15 AM'), 15);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('25:00'), null);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('bad'), null);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes(''), null);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('1:99 PM'), null);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('0:00 AM'), null);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('1:00:99 PM'), null);
});

test('Test_FormatMinutesHelpers_TestKeysAndClock_ExpectStrings', () => {
   assert.equal(DayPlannerScheduleController.formatMinutesAsScheduleTimeKey(9 * 60 + 5), '09:05');
   assert.match(
      DayPlannerScheduleController.formatMinutesAsClockTime(13 * 60),
      /1:00\s*PM/i
   );
});

test('Test_CollectAndEarliestFixedZooScheduleStartMinutes_TestItems_ExpectMinutes', () => {
   const itinerary = {
      guardiansTalks: [
         { start_time: '11:00', is_deleted: true },
         { start_time: '1:00 PM' },
      ],
      wildEncounters: [
         { start_time: '10:30' },
         { start_time: 'bad' },
      ],
   };

   assert.deepEqual(
      DayPlannerScheduleController.collectFixedZooScheduleStartMinutes(itinerary).sort((a, b) => a - b),
      [10 * 60 + 30, 13 * 60]
   );
   assert.equal(
      DayPlannerScheduleController.earliestFixedZooScheduleStartMinutes(itinerary),
      10 * 60 + 30
   );
   assert.equal(DayPlannerScheduleController.earliestFixedZooScheduleStartMinutes({}), null);
});

test('Test_ResolveDayPlannerTimelineStartMinutes_TestCandidates_ExpectEarliest', () => {
   assert.equal(
      DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(
         { earlyAdmissionTime: '09:00', openTime: '09:30' },
         { arrivalTime: '10:00' }
      ),
      9 * 60
   );
   assert.equal(
      DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(
         { openTime: '09:30' },
         {
            arrivalTime: '10:00',
            guardiansTalks: [{ start_time: '08:45' }],
         }
      ),
      8 * 60 + 45
   );
   assert.equal(
      DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes({}, {}),
      null
   );
});

test('Test_BuildArrivalAndDepartureTimeBounds_TestHours_ExpectBoundsOrNull', () => {
   const arrival = DayPlannerScheduleController.buildArrivalTimeBounds({
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
   });
   assert.equal(arrival.minMinutes, 9 * 60);
   assert.equal(arrival.maxMinutes, 18 * 60);
   assert.equal(arrival.minScheduleTime, '09:00');
   assert.equal(arrival.maxScheduleTime, '18:00');

   assert.equal(
      DayPlannerScheduleController.buildArrivalTimeBounds({
         openTime: '10:00',
         lastAdmissionTime: '09:00',
      }),
      null
   );

   const departure = DayPlannerScheduleController.buildDepartureTimeBounds({
      openTime: '09:30',
      closeTime: '19:00',
   });
   assert.equal(departure.minMinutes, 9 * 60 + 30);
   assert.equal(departure.maxMinutes, 19 * 60);

   assert.equal(
      DayPlannerScheduleController.buildDepartureTimeBounds({
         openTime: '19:00',
         closeTime: '09:00',
      }),
      null
   );
});

test('Test_IsArrivalAndDepartureWithinBounds_TestDelegates_ExpectBoolean', () => {
   const original = DayPlannerScheduleHelper.isTimeWithinBounds;
   const calls = [];
   DayPlannerScheduleHelper.isTimeWithinBounds = (...args) => {
      calls.push(args);
      return true;
   };

   try {
      const bounds = { minMinutes: 540, maxMinutes: 1080 };
      assert.equal(DayPlannerScheduleController.isArrivalTimeWithinBounds('10:00', bounds), true);
      assert.equal(DayPlannerScheduleController.isDepartureTimeWithinBounds('16:00', bounds), true);
      assert.equal(calls.length, 2);
   } finally {
      DayPlannerScheduleHelper.isTimeWithinBounds = original;
   }
});

test('Test_AreItineraryScheduleTimesOrdered_TestPairs_ExpectBoolean', () => {
   assert.equal(
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered('10:00', '16:00'),
      true
   );
   assert.equal(
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered('16:00', '10:00'),
      false
   );
   assert.equal(
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered('bad', '10:00'),
      true
   );
});

test('Test_ResolveArrivalAndDepartureTimeValidationError_TestMessages_ExpectErrors', () => {
   const originalArrival = DayPlannerScheduleController.isArrivalTimeWithinBounds;
   const originalDeparture = DayPlannerScheduleController.isDepartureTimeWithinBounds;
   const originalOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered;

   DayPlannerScheduleController.isArrivalTimeWithinBounds = () => false;
   DayPlannerScheduleController.isDepartureTimeWithinBounds = () => true;
   DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => true;

   try {
      assert.equal(
         DayPlannerScheduleController.resolveArrivalTimeValidationError(
            '08:00',
            {},
            '16:00',
            { arrivalTimeInvalid: 'arrival bad' }
         ),
         'arrival bad'
      );

      DayPlannerScheduleController.isArrivalTimeWithinBounds = () => true;
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => false;
      assert.equal(
         DayPlannerScheduleController.resolveArrivalTimeValidationError(
            '17:00',
            {},
            '16:00',
            { timeOrderInvalid: 'order bad' }
         ),
         'order bad'
      );

      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => true;
      assert.equal(
         DayPlannerScheduleController.resolveArrivalTimeValidationError(
            '10:00',
            {},
            '16:00',
            {}
         ),
         null
      );

      DayPlannerScheduleController.isDepartureTimeWithinBounds = () => false;
      assert.equal(
         DayPlannerScheduleController.resolveDepartureTimeValidationError(
            '20:00',
            {},
            '10:00',
            { departureTimeInvalid: 'departure bad' }
         ),
         'departure bad'
      );

      DayPlannerScheduleController.isDepartureTimeWithinBounds = () => true;
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => false;
      assert.equal(
         DayPlannerScheduleController.resolveDepartureTimeValidationError(
            '09:00',
            {},
            '10:00',
            { departureTimeAfterArrivalInvalid: 'after arrival' }
         ),
         'after arrival'
      );

      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = () => true;
      assert.equal(
         DayPlannerScheduleController.resolveDepartureTimeValidationError(
            '16:00',
            {},
            '10:00',
            {}
         ),
         null
      );
   } finally {
      DayPlannerScheduleController.isArrivalTimeWithinBounds = originalArrival;
      DayPlannerScheduleController.isDepartureTimeWithinBounds = originalDeparture;
      DayPlannerScheduleController.areItineraryScheduleTimesOrdered = originalOrdered;
   }
});

test('Test_BuildHalfHourSlotStarts_TestRange_ExpectSlots', () => {
   assert.deepEqual(DayPlannerScheduleController.buildHalfHourSlotStarts(null, 600), []);
   assert.deepEqual(DayPlannerScheduleController.buildHalfHourSlotStarts(600, 600), []);

   const slots = DayPlannerScheduleController.buildHalfHourSlotStarts(9 * 60 + 15, 11 * 60);
   assert.equal(slots[0], 9 * 60 + 15);
   assert.ok(slots.includes(9 * 60 + 30));
   assert.ok(slots.includes(10 * 60));
   assert.ok(slots.includes(10 * 60 + 30));
   assert.equal(
      slots.every((slot) => slot < 11 * 60 || slot === 9 * 60 + 15),
      true
   );
   assert.equal(
      slots.at(-1),
      Math.floor((11 * 60 - 1) / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES)
         * TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
   );

   // Open on a half-hour boundary so the first loop candidate equals openMinutes.
   assert.deepEqual(
      DayPlannerScheduleController.buildHalfHourSlotStarts(9 * 60, 10 * 60 + 30),
      [9 * 60, 9 * 60 + 30, 10 * 60]
   );
});
