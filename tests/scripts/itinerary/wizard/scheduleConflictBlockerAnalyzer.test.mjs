import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleConflictBlockerAnalyzer } from '../../../../scripts/itinerary/wizard/scheduleConflictBlockerAnalyzer.js';
import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';

test('Test_TrimRangeAgainstBlocker_TestOverlapCases_ExpectTrimmedOrNull', () => {
   assert.deepEqual(
      ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(100, 200, 50, 80),
      { start: 100, end: 200 }
   );
   assert.equal(
      ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(100, 200, 90, 210),
      null
   );
   assert.deepEqual(
      ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(100, 200, 50, 150),
      { start: 150, end: 200 }
   );
   assert.deepEqual(
      ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(100, 200, 150, 250),
      { start: 100, end: 150 }
   );
   assert.deepEqual(
      ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(100, 200, 120, 160),
      { start: 160, end: 200 }
   );
});

test('Test_GetTrimmedGuardiansTalkMinutes_TestBlockers_ExpectTrimOrNull', () => {
   const originalParse = DayPlannerScheduleController.parseClockTimeMinutes;
   DayPlannerScheduleController.parseClockTimeMinutes = (value) => {
      const map = {
         '10:00 AM': 600,
         '11:00 AM': 660,
         '10:30 AM': 630,
         '10:45 AM': 645,
      };
      return map[value];
   };

   try {
      assert.deepEqual(
         ScheduleConflictBlockerAnalyzer.getTrimmedGuardiansTalkMinutes(
            { start_time: '10:00 AM', end_time: '11:00 AM' },
            [{ start_time: '10:00 AM', end_time: '10:30 AM' }]
         ),
         { start: 630, end: 660 }
      );
      assert.equal(
         ScheduleConflictBlockerAnalyzer.getTrimmedGuardiansTalkMinutes(
            { start_time: '10:00 AM', end_time: '11:00 AM' },
            [{ start_time: '10:00 AM', end_time: '11:00 AM' }]
         ),
         null
      );
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});

test('Test_IsGuardiansTalkFullyCoveredAndRequiresTrim_TestRanges_ExpectFlags', () => {
   const originalParse = DayPlannerScheduleController.parseClockTimeMinutes;
   DayPlannerScheduleController.parseClockTimeMinutes = (value) => ({
      '10:00 AM': 600,
      '11:00 AM': 660,
      '10:30 AM': 630,
   }[value]);

   try {
      assert.equal(
         ScheduleConflictBlockerAnalyzer.isGuardiansTalkFullyCoveredByBlockers(
            { start_time: '10:00 AM', end_time: '11:00 AM' },
            [{ start_time: '10:00 AM', end_time: '11:00 AM' }]
         ),
         true
      );
      assert.equal(
         ScheduleConflictBlockerAnalyzer.guardiansTalkRequiresTrimOverride(
            { start_time: '10:00 AM', end_time: '11:00 AM' },
            [{ start_time: '10:00 AM', end_time: '10:30 AM' }]
         ),
         true
      );
      assert.equal(
         ScheduleConflictBlockerAnalyzer.guardiansTalkRequiresTrimOverride(
            { start_time: '10:00 AM', end_time: '11:00 AM' },
            []
         ),
         false
      );
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});

test('Test_ConflictItemKeyAndSelectionBlockers_TestOrdering_ExpectWildAndTalks', () => {
   assert.equal(
      ScheduleConflictBlockerAnalyzer.conflictItemKey({ item_type: 'talk', name: 'Tiger' }),
      'talk::Tiger'
   );

   const originalIsWild = ScheduleConflictChecker.isWildEncounterConflictItem;
   const originalIsTalk = ScheduleConflictChecker.isGuardiansTalkConflictItem;
   const originalOverlap = ScheduleConflictChecker.scheduleTimesOverlap;
   ScheduleConflictChecker.isWildEncounterConflictItem = (item) => item.item_type === 'encounter';
   ScheduleConflictChecker.isGuardiansTalkConflictItem = (item) => item.item_type === 'talk';
   ScheduleConflictChecker.scheduleTimesOverlap = () => true;

   try {
      const selection = {
         items: [
            { item_type: 'encounter', name: 'Giraffe', start_time: '9:00 AM', end_time: '9:30 AM' },
            { item_type: 'talk', name: 'Tiger', start_time: '10:00 AM', end_time: '10:30 AM' },
            { item_type: 'talk', name: 'Lion', start_time: '10:15 AM', end_time: '10:45 AM' },
            { item_type: 'talk', name: 'Later', start_time: '11:00 AM', end_time: '11:30 AM' },
         ],
      };
      const blockers = ScheduleConflictBlockerAnalyzer.getSelectionBlockersForItem(
         selection,
         { item_type: 'talk', name: 'Lion' }
      );
      assert.deepEqual(
         blockers.map((item) => item.name),
         ['Giraffe', 'Tiger']
      );

      const withExtra = ScheduleConflictBlockerAnalyzer.getGuardiansTalkTrimBlockers(
         selection,
         { item_type: 'talk', name: 'Lion' },
         { item_type: 'encounter', name: 'Extra' }
      );
      assert.ok(withExtra.some((item) => item.name === 'Extra'));
   } finally {
      ScheduleConflictChecker.isWildEncounterConflictItem = originalIsWild;
      ScheduleConflictChecker.isGuardiansTalkConflictItem = originalIsTalk;
      ScheduleConflictChecker.scheduleTimesOverlap = originalOverlap;
   }
});

test('Test_EncounterHasScheduleExceptionWithSelectedTalks_TestTrimRequired_ExpectTrue', () => {
   const originalIsTalk = ScheduleConflictChecker.isGuardiansTalkConflictItem;
   const originalOverlap = ScheduleConflictChecker.scheduleTimesOverlap;
   const originalParse = DayPlannerScheduleController.parseClockTimeMinutes;

   ScheduleConflictChecker.isGuardiansTalkConflictItem = (item) => item.item_type === 'talk';
   ScheduleConflictChecker.scheduleTimesOverlap = () => true;
   DayPlannerScheduleController.parseClockTimeMinutes = (value) => ({
      '10:00 AM': 600,
      '11:00 AM': 660,
      '10:30 AM': 630,
   }[value]);

   try {
      const selection = {
         items: [
            {
               item_type: 'talk',
               name: 'Tiger',
               start_time: '10:00 AM',
               end_time: '11:00 AM',
            },
         ],
      };
      assert.equal(
         ScheduleConflictBlockerAnalyzer.encounterHasScheduleExceptionWithSelectedTalks(
            selection,
            {
               item_type: 'encounter',
               name: 'Giraffe',
               start_time: '10:00 AM',
               end_time: '10:30 AM',
            }
         ),
         true
      );
   } finally {
      ScheduleConflictChecker.isGuardiansTalkConflictItem = originalIsTalk;
      ScheduleConflictChecker.scheduleTimesOverlap = originalOverlap;
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});
