import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';
import { Position } from '../../../../scripts/shared/enums/position.js';

const greatBarrierReef = {
   name: 'Great Barrier Reef',
   start_time: '13:00',
   end_time: '13:20',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
};

const grizzly = {
   name: 'Grizzly Bear',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
};

const capybara = {
   name: 'Capybara',
   start_time: '13:30',
   end_time: '14:00',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
};

const africanLionTalk = {
   name: 'African Lion',
   start_time: '13:30',
   end_time: '14:00',
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   location: 'Africa Savanna',
};

const amurTigerTalk = {
   name: 'Amur Tiger',
   start_time: '13:30',
   end_time: '14:00',
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   location: 'Eurasia Wilds',
};

const gibbonTalk = {
   name: 'White-Handed Gibbon',
   start_time: '13:10',
   end_time: '13:40',
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   location: 'Indo-Malaya',
};

const gibbonTalkAtOne = {
   ...gibbonTalk,
   start_time: '13:00',
   end_time: '13:30',
};


test('Test_ScheduleTimesOverlap_TestOverlappingEncounters_ExpectTrue', () => {
   const overlaps = ScheduleConflictChecker.scheduleTimesOverlap(greatBarrierReef, grizzly);

   assert.equal(overlaps, true);
});


test('Test_ScheduleTimesOverlap_TestAdjacentEncounters_ExpectFalse', () => {
   const overlaps = ScheduleConflictChecker.scheduleTimesOverlap(greatBarrierReef, capybara);

   assert.equal(overlaps, false);
});


test('Test_ScheduleTimesOverlap_TestPartialOverlap_ExpectTrue', () => {
   const overlaps = ScheduleConflictChecker.scheduleTimesOverlap(grizzly, capybara);

   assert.equal(overlaps, true);
});


test('Test_ScheduleTimesOverlap_TestPartialOverlapReversed_ExpectTrue', () => {
   const overlaps = ScheduleConflictChecker.scheduleTimesOverlap(capybara, grizzly);

   assert.equal(overlaps, true);
});


test('Test_CanSelectConflictItem_TestPartialTalk_ExpectAllowed', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, grizzly);

   const allowed = ScheduleConflictChecker.canSelectConflictItem(selection, africanLionTalk);

   assert.equal(allowed, true);
});


test('Test_ConflictItemRequiresTrimOverride_TestPartialTalk_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   const allowed = ScheduleConflictChecker.canSelectConflictItem(selection, gibbonTalk);
   const requiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      gibbonTalk
   );

   assert.equal(allowed, true);
   assert.equal(requiresTrim, true);
});


test('Test_ConflictItemRequiresTrimOverride_TestTalkThenEncounter_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, gibbonTalk);

   const allowed = ScheduleConflictChecker.canSelectConflictItem(selection, greatBarrierReef);
   const requiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      greatBarrierReef
   );

   assert.equal(allowed, true);
   assert.equal(requiresTrim, true);
});


test('Test_CanSelectConflictItem_TestFullCover_ExpectBlocked', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, gibbonTalkAtOne);

   const allowed = ScheduleConflictChecker.canSelectConflictItem(selection, grizzly);
   const requiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      grizzly
   );

   assert.equal(allowed, false);
   assert.equal(requiresTrim, false);
});


test('Test_ConflictItemRequiresTrimOverride_TestSelectedTrimmedTalk_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, gibbonTalk);

   const requiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      gibbonTalk
   );

   assert.equal(requiresTrim, true);
});


test('Test_ConflictItemRequiresTrimOverride_TestTalkBeforeEncounter_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, gibbonTalk);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   const talkRequiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      gibbonTalk
   );
   const encounterRequiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      greatBarrierReef
   );

   assert.equal(talkRequiresTrim, true);
   assert.equal(encounterRequiresTrim, true);
});


test('Test_ConflictItemRequiresTrimOverride_TestNoOverlap_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const laterTalk = {
      ...africanLionTalk,
      start_time: '14:00',
      end_time: '14:30',
   };
   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   const requiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      laterTalk
   );

   assert.equal(requiresTrim, false);
});


test('Test_ConflictItemRequiresTrimOverride_TestNonOverlapEncounter_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const laterTalk = {
      ...africanLionTalk,
      start_time: '14:00',
      end_time: '14:30',
   };
   ScheduleConflictChecker.toggleConflictItemSelection(selection, laterTalk);

   const requiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      greatBarrierReef
   );

   assert.equal(requiresTrim, false);
});


test('Test_CanSelectConflictItem_TestTalkFullyCovered_ExpectBlocked', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const fullyCoveredTalk = {
      ...africanLionTalk,
      start_time: '13:15',
      end_time: '13:30',
   };
   ScheduleConflictChecker.toggleConflictItemSelection(selection, grizzly);

   const allowed = ScheduleConflictChecker.canSelectConflictItem(selection, fullyCoveredTalk);

   assert.equal(allowed, false);
});


test('Test_CanSelectConflictItem_TestEarlierTalkPrecedence_ExpectLaterBlocked', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const laterTalk = {
      ...amurTigerTalk,
      name: 'Later Tiger Talk',
      start_time: '13:45',
      end_time: '14:15',
   };
   ScheduleConflictChecker.toggleConflictItemSelection(selection, africanLionTalk);

   const sameTimeAllowed = ScheduleConflictChecker.canSelectConflictItem(selection, amurTigerTalk);
   const laterAllowed = ScheduleConflictChecker.canSelectConflictItem(selection, laterTalk);

   assert.equal(sameTimeAllowed, false);
   assert.equal(laterAllowed, true);
});


test('Test_CanSelectConflictItem_TestLaterTalkSelected_ExpectSameTimeBlocked', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const laterTalk = {
      ...amurTigerTalk,
      name: 'Later Tiger Talk',
      start_time: '13:45',
      end_time: '14:15',
   };
   ScheduleConflictChecker.toggleConflictItemSelection(selection, africanLionTalk);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, laterTalk);

   const sameTimeAllowed = ScheduleConflictChecker.canSelectConflictItem(selection, amurTigerTalk);

   assert.equal(sameTimeAllowed, false);
});


test('Test_ToggleConflictItemSelection_TestNonOverlapEncounters_ExpectBothSelected', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, capybara);

   assert.deepEqual(selection.items, [greatBarrierReef, capybara]);
   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, grizzly), false);
   assert.equal(ScheduleConflictChecker.isConflictItemSelected(selection, grizzly), false);
   assert.equal(selection.items[Position.FIRST], greatBarrierReef);
   assert.equal(selection.items[Position.SECOND], capybara);
});


test('Test_HasAdditionalSelectableConflictItems_TestCompatible_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const items = [greatBarrierReef, grizzly, capybara];
   ScheduleConflictChecker.toggleConflictItemSelection(selection, capybara);

   const hasAdditional = ScheduleConflictChecker.hasAdditionalSelectableConflictItems(
      items,
      selection
   );

   assert.equal(hasAdditional, true);
});


test('Test_HasAnyAdditionalSelectableConflictItems_TestCompatible_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const items = [greatBarrierReef, grizzly, capybara];
   ScheduleConflictChecker.toggleConflictItemSelection(selection, capybara);
   const groups = [{ items, selection }];

   const hasAdditional = ScheduleConflictChecker.hasAnyAdditionalSelectableConflictItems(groups);

   assert.equal(hasAdditional, true);
});


test('Test_HasAdditionalSelectableConflictItems_TestAllSelected_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const items = [greatBarrierReef, grizzly, capybara];
   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, capybara);

   const hasAdditional = ScheduleConflictChecker.hasAdditionalSelectableConflictItems(
      items,
      selection
   );

   assert.equal(hasAdditional, false);
});


test('Test_HasAdditionalSelectableConflictItems_TestEmptySelection_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const items = [greatBarrierReef, capybara];

   const hasAdditional = ScheduleConflictChecker.hasAdditionalSelectableConflictItems(
      items,
      selection
   );

   assert.equal(hasAdditional, false);
});


test('Test_ToggleConflictItemSelection_TestToggleOff_ExpectRemoved', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.deepEqual(selection.items, []);
});


test('Test_ConflictItemRequiresTrimOverride_TestUnselectableTalk_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const fullyCoveredTalk = {
      ...africanLionTalk,
      start_time: '13:15',
      end_time: '13:30',
   };
   ScheduleConflictChecker.toggleConflictItemSelection(selection, grizzly);

   const allowed = ScheduleConflictChecker.canSelectConflictItem(selection, fullyCoveredTalk);
   const requiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      fullyCoveredTalk
   );

   assert.equal(allowed, false);
   assert.equal(requiresTrim, false);
});


test('Test_ConflictItemRequiresTrimOverride_TestUnknownItemType_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const event = {
      name: 'Lunch',
      item_type: 'event',
   };

   const requiresTrim = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
      selection,
      event
   );

   assert.equal(requiresTrim, false);
});


test('Test_ToggleConflictItemSelection_TestCannotSelect_ExpectUnchanged', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, grizzly);
   const blocked = {
      name: 'Blocked Encounter',
      start_time: '13:00',
      end_time: '13:20',
      item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   };

   const allowed = ScheduleConflictChecker.canSelectConflictItem(selection, blocked);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, blocked);

   assert.equal(allowed, false);
   assert.deepEqual(selection.items, [grizzly]);
});
