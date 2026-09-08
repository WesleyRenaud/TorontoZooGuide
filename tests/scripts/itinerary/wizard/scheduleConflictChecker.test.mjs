import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';

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

test('Test_ScheduleTimesOverlap_TestHalfOpen_ExpectBackendRule', () => {
   assert.equal(ScheduleConflictChecker.scheduleTimesOverlap(greatBarrierReef, grizzly), true);
   assert.equal(ScheduleConflictChecker.scheduleTimesOverlap(greatBarrierReef, capybara), false);
   assert.equal(ScheduleConflictChecker.scheduleTimesOverlap(grizzly, capybara), true);
   assert.equal(ScheduleConflictChecker.scheduleTimesOverlap(capybara, grizzly), true);
});

test('Test_CanSelectConflictItem_TestPartialTalk_ExpectAllowed', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, grizzly);

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, africanLionTalk), true);
});

test('Test_ConflictItemRequiresTrimOverride_TestPartialTalk_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, gibbonTalk), true);
   assert.equal(ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, gibbonTalk), true);
});

test('Test_ConflictItemRequiresTrimOverride_TestTalkThenEncounter_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, gibbonTalk);

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, greatBarrierReef), true);
   assert.equal(
      ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, greatBarrierReef),
      true
   );
});

test('Test_CanSelectConflictItem_TestFullCover_ExpectBlocked', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, gibbonTalkAtOne);

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, grizzly), false);
   assert.equal(ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, grizzly), false);
});

test('Test_ConflictItemRequiresTrimOverride_TestSelectedTrimmedTalk_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, gibbonTalk);

   assert.equal(
      ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, gibbonTalk),
      true
   );
});

test('Test_ConflictItemRequiresTrimOverride_TestTalkBeforeEncounter_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, gibbonTalk);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.equal(
      ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, gibbonTalk),
      true
   );
   assert.equal(
      ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, greatBarrierReef),
      true
   );
});

test('Test_ConflictItemRequiresTrimOverride_TestNoOverlap_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const laterTalk = {
      ...africanLionTalk,
      start_time: '14:00',
      end_time: '14:30',
   };

   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.equal(ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, laterTalk), false);
});

test('Test_ConflictItemRequiresTrimOverride_TestNonOverlapEncounter_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const laterTalk = {
      ...africanLionTalk,
      start_time: '14:00',
      end_time: '14:30',
   };

   ScheduleConflictChecker.toggleConflictItemSelection(selection, laterTalk);

   assert.equal(
      ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, greatBarrierReef),
      false
   );
});

test('Test_CanSelectConflictItem_TestTalkFullyCovered_ExpectBlocked', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const fullyCoveredTalk = {
      ...africanLionTalk,
      start_time: '13:15',
      end_time: '13:30',
   };

   ScheduleConflictChecker.toggleConflictItemSelection(selection, grizzly);

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, fullyCoveredTalk), false);
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

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, amurTigerTalk), false);

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, laterTalk), true);

   ScheduleConflictChecker.toggleConflictItemSelection(selection, laterTalk);

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, amurTigerTalk), false);
});

test('Test_ToggleConflictItemSelection_TestNonOverlapEncounters_ExpectBothSelected', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, capybara);

   assert.deepEqual(selection.items, [greatBarrierReef, capybara]);
   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, grizzly), false);
   assert.equal(ScheduleConflictChecker.isConflictItemSelected(selection, grizzly), false);
});

test('Test_HasAdditionalSelectableConflictItems_TestCompatible_ExpectTrue', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const items = [greatBarrierReef, grizzly, capybara];

   ScheduleConflictChecker.toggleConflictItemSelection(selection, capybara);

   assert.equal(
      ScheduleConflictChecker.hasAdditionalSelectableConflictItems(items, selection),
      true
   );
   assert.equal(
      ScheduleConflictChecker.hasAnyAdditionalSelectableConflictItems([
         { items, selection },
      ]),
      true
   );
});

test('Test_HasAdditionalSelectableConflictItems_TestAllSelected_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const items = [greatBarrierReef, grizzly, capybara];

   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, capybara);

   assert.equal(
      ScheduleConflictChecker.hasAdditionalSelectableConflictItems(items, selection),
      false
   );
});

test('Test_HasAdditionalSelectableConflictItems_TestEmptySelection_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   assert.equal(
      ScheduleConflictChecker.hasAdditionalSelectableConflictItems(
         [greatBarrierReef, capybara],
         selection
      ),
      false
   );
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

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, fullyCoveredTalk), false);
   assert.equal(
      ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, fullyCoveredTalk),
      false
   );
});

test('Test_ConflictItemRequiresTrimOverride_TestUnknownItemType_ExpectFalse', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   assert.equal(
      ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, {
         name: 'Lunch',
         item_type: 'event',
      }),
      false
   );
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

   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, blocked), false);
   ScheduleConflictChecker.toggleConflictItemSelection(selection, blocked);
   assert.deepEqual(selection.items, [grizzly]);
});
