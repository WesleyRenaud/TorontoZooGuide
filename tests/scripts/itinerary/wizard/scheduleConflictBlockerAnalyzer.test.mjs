import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleConflictBlockerAnalyzer } from '../../../../scripts/itinerary/wizard/scheduleConflictBlockerAnalyzer.js';
import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';
import { Position } from '../../../../scripts/shared/enums/position.js';

const _tenAm = '10:00 AM';
const _elevenAm = '11:00 AM';
const _tenThirtyAm = '10:30 AM';
const _tenFortyFiveAm = '10:45 AM';
const _tenAmMinutes = 600;
const _elevenAmMinutes = 660;
const _tenThirtyAmMinutes = 630;
const _tenFortyFiveAmMinutes = 645;
const _talkType = 'talk';
const _encounterType = 'encounter';

function _clockMinutes(overrides = {}) {
   return {
      [_tenAm]: _tenAmMinutes,
      [_elevenAm]: _elevenAmMinutes,
      [_tenThirtyAm]: _tenThirtyAmMinutes,
      [_tenFortyFiveAm]: _tenFortyFiveAmMinutes,
      ...overrides,
   };
}

function _stubParseClockMinutes(map) {
   const original = DayPlannerScheduleController.parseClockTimeMinutes;
   DayPlannerScheduleController.parseClockTimeMinutes = (value) => map[value];
   return original;
}

function _stubConflictItemTypes({ overlap = true } = {}) {
   const originals = {
      isWild: ScheduleConflictChecker.isWildEncounterConflictItem,
      isTalk: ScheduleConflictChecker.isGuardiansTalkConflictItem,
      overlap: ScheduleConflictChecker.scheduleTimesOverlap,
   };
   ScheduleConflictChecker.isWildEncounterConflictItem = (item) => item.item_type === _encounterType;
   ScheduleConflictChecker.isGuardiansTalkConflictItem = (item) => item.item_type === _talkType;
   ScheduleConflictChecker.scheduleTimesOverlap = () => overlap;
   return originals;
}

function _restoreConflictItemTypes(originals) {
   ScheduleConflictChecker.isWildEncounterConflictItem = originals.isWild;
   ScheduleConflictChecker.isGuardiansTalkConflictItem = originals.isTalk;
   ScheduleConflictChecker.scheduleTimesOverlap = originals.overlap;
}


test('Test_TrimRangeAgainstBlocker_TestNoOverlap_ExpectUnchanged', () => {
   const start = 100;
   const end = 200;
   const blockerStart = 50;
   const blockerEnd = 80;

   const trimmed = ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(
      start,
      end,
      blockerStart,
      blockerEnd
   );

   assert.deepEqual(trimmed, { start, end });
});


test('Test_TrimRangeAgainstBlocker_TestFullCover_ExpectNull', () => {
   const start = 100;
   const end = 200;
   const blockerStart = 90;
   const blockerEnd = 210;

   const trimmed = ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(
      start,
      end,
      blockerStart,
      blockerEnd
   );

   assert.equal(trimmed, null);
});


test('Test_TrimRangeAgainstBlocker_TestOverlapStart_ExpectTrimmedStart', () => {
   const start = 100;
   const end = 200;
   const blockerStart = 50;
   const blockerEnd = 150;

   const trimmed = ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(
      start,
      end,
      blockerStart,
      blockerEnd
   );

   assert.deepEqual(trimmed, { start: blockerEnd, end });
});


test('Test_TrimRangeAgainstBlocker_TestOverlapEnd_ExpectTrimmedEnd', () => {
   const start = 100;
   const end = 200;
   const blockerStart = 150;
   const blockerEnd = 250;

   const trimmed = ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(
      start,
      end,
      blockerStart,
      blockerEnd
   );

   assert.deepEqual(trimmed, { start, end: blockerStart });
});


test('Test_TrimRangeAgainstBlocker_TestInteriorOverlap_ExpectTrimmedStart', () => {
   const start = 100;
   const end = 200;
   const blockerStart = 120;
   const blockerEnd = 160;

   const trimmed = ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(
      start,
      end,
      blockerStart,
      blockerEnd
   );

   assert.deepEqual(trimmed, { start: blockerEnd, end });
});


test('Test_TrimRangeAgainstBlocker_TestNaN_ExpectNull', () => {
   const start = Number.NaN;
   const end = Number.NaN;
   const blockerStart = Number.NaN;
   const blockerEnd = Number.NaN;

   const trimmed = ScheduleConflictBlockerAnalyzer.trimRangeAgainstBlocker(
      start,
      end,
      blockerStart,
      blockerEnd
   );

   assert.equal(trimmed, null);
});


test('Test_GetTrimmedGuardiansTalkMinutes_TestPartialBlocker_ExpectTrimmed', () => {
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const talk = { start_time: _tenAm, end_time: _elevenAm };
   const blockers = [{ start_time: _tenAm, end_time: _tenThirtyAm }];

   try {
      const trimmed = ScheduleConflictBlockerAnalyzer.getTrimmedGuardiansTalkMinutes(
         talk,
         blockers
      );

      assert.deepEqual(trimmed, { start: _tenThirtyAmMinutes, end: _elevenAmMinutes });
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_GetTrimmedGuardiansTalkMinutes_TestFullCover_ExpectNull', () => {
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const talk = { start_time: _tenAm, end_time: _elevenAm };
   const blockers = [{ start_time: _tenAm, end_time: _elevenAm }];

   try {
      const trimmed = ScheduleConflictBlockerAnalyzer.getTrimmedGuardiansTalkMinutes(
         talk,
         blockers
      );

      assert.equal(trimmed, null);
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_IsGuardiansTalkFullyCoveredByBlockers_TestFullCover_ExpectTrue', () => {
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const talk = { start_time: _tenAm, end_time: _elevenAm };
   const blockers = [{ start_time: _tenAm, end_time: _elevenAm }];

   try {
      const covered = ScheduleConflictBlockerAnalyzer.isGuardiansTalkFullyCoveredByBlockers(
         talk,
         blockers
      );

      assert.equal(covered, true);
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_IsGuardiansTalkFullyCoveredByBlockers_TestZeroDuration_ExpectTrue', () => {
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const talk = { start_time: _tenAm, end_time: _tenAm };

   try {
      const covered = ScheduleConflictBlockerAnalyzer.isGuardiansTalkFullyCoveredByBlockers(
         talk,
         []
      );

      assert.equal(covered, true);
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_GuardiansTalkRequiresTrimOverride_TestPartialBlocker_ExpectTrue', () => {
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const talk = { start_time: _tenAm, end_time: _elevenAm };
   const blockers = [{ start_time: _tenAm, end_time: _tenThirtyAm }];

   try {
      const requiresTrim = ScheduleConflictBlockerAnalyzer.guardiansTalkRequiresTrimOverride(
         talk,
         blockers
      );

      assert.equal(requiresTrim, true);
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_GuardiansTalkRequiresTrimOverride_TestNoBlockers_ExpectFalse', () => {
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const talk = { start_time: _tenAm, end_time: _elevenAm };

   try {
      const requiresTrim = ScheduleConflictBlockerAnalyzer.guardiansTalkRequiresTrimOverride(
         talk,
         []
      );

      assert.equal(requiresTrim, false);
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_GuardiansTalkRequiresTrimOverride_TestFullCover_ExpectFalse', () => {
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const talk = { start_time: _tenAm, end_time: _elevenAm };
   const blockers = [{ start_time: _tenAm, end_time: _elevenAm }];

   try {
      const requiresTrim = ScheduleConflictBlockerAnalyzer.guardiansTalkRequiresTrimOverride(
         talk,
         blockers
      );

      assert.equal(requiresTrim, false);
   } finally {
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_ConflictItemKey_TestTalk_ExpectTypedName', () => {
   const name = 'Tiger';
   const item = { item_type: _talkType, name };

   const key = ScheduleConflictBlockerAnalyzer.conflictItemKey(item);

   assert.equal(key, `${_talkType}::${name}`);
});


test('Test_GetSelectionBlockersForItem_TestOrdering_ExpectWildAndTalks', () => {
   const originals = _stubConflictItemTypes();
   const giraffe = {
      item_type: _encounterType,
      name: 'Giraffe',
      start_time: '9:00 AM',
      end_time: '9:30 AM',
   };
   const tiger = {
      item_type: _talkType,
      name: 'Tiger',
      start_time: _tenAm,
      end_time: _tenThirtyAm,
   };
   const lion = {
      item_type: _talkType,
      name: 'Lion',
      start_time: '10:15 AM',
      end_time: _tenFortyFiveAm,
   };
   const later = {
      item_type: _talkType,
      name: 'Later',
      start_time: _elevenAm,
      end_time: '11:30 AM',
   };
   const selection = {
      items: [giraffe, tiger, lion, later],
   };

   try {
      const blockers = ScheduleConflictBlockerAnalyzer.getSelectionBlockersForItem(
         selection,
         lion
      );

      assert.deepEqual(
         blockers.map((item) => item.name),
         [giraffe.name, tiger.name]
      );
      assert.equal(blockers[Position.FIRST], giraffe);
      assert.equal(blockers[Position.SECOND], tiger);
   } finally {
      _restoreConflictItemTypes(originals);
   }
});


test('Test_GetGuardiansTalkTrimBlockers_TestExtraEncounter_ExpectIncluded', () => {
   const originals = _stubConflictItemTypes();
   const giraffe = {
      item_type: _encounterType,
      name: 'Giraffe',
      start_time: '9:00 AM',
      end_time: '9:30 AM',
   };
   const tiger = {
      item_type: _talkType,
      name: 'Tiger',
      start_time: _tenAm,
      end_time: _tenThirtyAm,
   };
   const lion = {
      item_type: _talkType,
      name: 'Lion',
      start_time: '10:15 AM',
      end_time: _tenFortyFiveAm,
   };
   const later = {
      item_type: _talkType,
      name: 'Later',
      start_time: _elevenAm,
      end_time: '11:30 AM',
   };
   const extra = { item_type: _encounterType, name: 'Extra' };
   const selection = {
      items: [giraffe, tiger, lion, later],
   };

   try {
      const blockers = ScheduleConflictBlockerAnalyzer.getGuardiansTalkTrimBlockers(
         selection,
         lion,
         extra
      );

      assert.ok(blockers.some((item) => item.name === extra.name));
   } finally {
      _restoreConflictItemTypes(originals);
   }
});


test('Test_EncounterHasScheduleExceptionWithSelectedTalks_TestTrimRequired_ExpectTrue', () => {
   const originals = _stubConflictItemTypes();
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const tiger = {
      item_type: _talkType,
      name: 'Tiger',
      start_time: _tenAm,
      end_time: _elevenAm,
   };
   const encounter = {
      item_type: _encounterType,
      name: 'Giraffe',
      start_time: _tenAm,
      end_time: _tenThirtyAm,
   };
   const selection = {
      items: [tiger],
   };

   try {
      const hasException = ScheduleConflictBlockerAnalyzer.encounterHasScheduleExceptionWithSelectedTalks(
         selection,
         encounter
      );

      assert.equal(hasException, true);
   } finally {
      _restoreConflictItemTypes(originals);
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_EncounterHasScheduleExceptionWithSelectedTalks_TestNoTalks_ExpectFalse', () => {
   const originals = _stubConflictItemTypes();
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const otherEncounter = { item_type: _encounterType, name: 'Other' };
   const encounter = {
      item_type: _encounterType,
      name: 'Giraffe',
      start_time: _tenAm,
      end_time: _tenThirtyAm,
   };
   const selection = {
      items: [otherEncounter],
   };

   try {
      const hasException = ScheduleConflictBlockerAnalyzer.encounterHasScheduleExceptionWithSelectedTalks(
         selection,
         encounter
      );

      assert.equal(hasException, false);
   } finally {
      _restoreConflictItemTypes(originals);
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_EncounterHasScheduleExceptionWithSelectedTalks_TestNoOverlap_ExpectFalse', () => {
   const originals = _stubConflictItemTypes({ overlap: false });
   const originalParse = _stubParseClockMinutes(_clockMinutes());
   const tiger = {
      item_type: _talkType,
      name: 'Tiger',
      start_time: _tenAm,
      end_time: _elevenAm,
   };
   const encounter = {
      item_type: _encounterType,
      name: 'Giraffe',
      start_time: _tenAm,
      end_time: _tenThirtyAm,
   };
   const selection = {
      items: [tiger],
   };

   try {
      const hasException = ScheduleConflictBlockerAnalyzer.encounterHasScheduleExceptionWithSelectedTalks(
         selection,
         encounter
      );

      assert.equal(hasException, false);
   } finally {
      _restoreConflictItemTypes(originals);
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});


test('Test_EncounterHasScheduleExceptionWithSelectedTalks_TestFullyCoveredTrim_ExpectTrue', () => {
   const originals = _stubConflictItemTypes();
   const coveredEndMinutes = 700;
   const originalParse = _stubParseClockMinutes(_clockMinutes({
      [_tenThirtyAm]: coveredEndMinutes,
   }));
   const tiger = {
      item_type: _talkType,
      name: 'Tiger',
      start_time: _tenAm,
      end_time: _elevenAm,
   };
   const encounter = {
      item_type: _encounterType,
      name: 'Giraffe',
      start_time: _tenAm,
      end_time: _tenThirtyAm,
   };
   const selection = {
      items: [tiger],
   };

   try {
      const hasException = ScheduleConflictBlockerAnalyzer.encounterHasScheduleExceptionWithSelectedTalks(
         selection,
         encounter
      );

      assert.equal(hasException, true);
   } finally {
      _restoreConflictItemTypes(originals);
      DayPlannerScheduleController.parseClockTimeMinutes = originalParse;
   }
});
