import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ScheduleConflictCompatibility } from '../../../../scripts/itinerary/wizard/scheduleConflictCompatibility.js';

const greatBarrierReef = {
   name: 'Great Barrier Reef',
   start_time: '13:00',
   end_time: '13:20',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
};

const grizzly = {
   name: 'Grizzly Bear',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
};

const capybara = {
   name: 'Capybara',
   start_time: '13:30',
   end_time: '14:00',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
};

const africanLionTalk = {
   name: 'African Lion',
   start_time: '13:30',
   end_time: '14:00',
   item_type: ItinerarySaveIssueItemType.guardiansTalk,
   location: 'Africa Savanna',
};

const amurTigerTalk = {
   name: 'Amur Tiger',
   start_time: '13:30',
   end_time: '14:00',
   item_type: ItinerarySaveIssueItemType.guardiansTalk,
   location: 'Eurasia Wilds',
};

test('Test_ScheduleTimesOverlap_TestHalfOpen_ExpectBackendRule', () => {
   assert.equal(ScheduleConflictCompatibility.scheduleTimesOverlap(greatBarrierReef, grizzly), true);
   assert.equal(ScheduleConflictCompatibility.scheduleTimesOverlap(greatBarrierReef, capybara), false);
   assert.equal(ScheduleConflictCompatibility.scheduleTimesOverlap(grizzly, capybara), true);
   assert.equal(ScheduleConflictCompatibility.scheduleTimesOverlap(capybara, grizzly), true);
});

const gibbonTalk = {
   name: 'White-Handed Gibbon',
   start_time: '13:10',
   end_time: '13:40',
   item_type: ItinerarySaveIssueItemType.guardiansTalk,
   location: 'Indo-Malaya',
};

test('Test_CanSelectConflictItem_TestPartialTalk_ExpectAllowed', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, grizzly);

   assert.equal(ScheduleConflictCompatibility.canSelectConflictItem(selection, africanLionTalk), true);
});

test('Test_ConflictItemRequiresTrimOverride_TestPartialTalk_ExpectTrue', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.equal(ScheduleConflictCompatibility.canSelectConflictItem(selection, gibbonTalk), true);
   assert.equal(ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, gibbonTalk), true);
});

const gibbonTalkAtOne = {
   ...gibbonTalk,
   start_time: '13:00',
   end_time: '13:30',
};

test('Test_ConflictItemRequiresTrimOverride_TestTalkThenEncounter_ExpectTrue', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, gibbonTalk);

   assert.equal(ScheduleConflictCompatibility.canSelectConflictItem(selection, greatBarrierReef), true);
   assert.equal(
      ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, greatBarrierReef),
      true
   );
});

test('Test_CanSelectConflictItem_TestFullCover_ExpectBlocked', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, gibbonTalkAtOne);

   assert.equal(ScheduleConflictCompatibility.canSelectConflictItem(selection, grizzly), false);
   assert.equal(ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, grizzly), false);
});

test('Test_ConflictItemRequiresTrimOverride_TestSelectedTrimmedTalk_ExpectTrue', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, gibbonTalk);

   assert.equal(
      ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, gibbonTalk),
      true
   );
});

test('Test_ConflictItemRequiresTrimOverride_TestTalkBeforeEncounter_ExpectTrue', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, gibbonTalk);
   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.equal(
      ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, gibbonTalk),
      true
   );
   assert.equal(
      ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, greatBarrierReef),
      true
   );
});

test('Test_ConflictItemRequiresTrimOverride_TestNoOverlap_ExpectFalse', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();
   const laterTalk = {
      ...africanLionTalk,
      start_time: '14:00',
      end_time: '14:30',
   };

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.equal(ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, laterTalk), false);
});

test('Test_ConflictItemRequiresTrimOverride_TestNonOverlapEncounter_ExpectFalse', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();
   const laterTalk = {
      ...africanLionTalk,
      start_time: '14:00',
      end_time: '14:30',
   };

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, laterTalk);

   assert.equal(
      ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, greatBarrierReef),
      false
   );
});

test('Test_CanSelectConflictItem_TestTalkFullyCovered_ExpectBlocked', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();
   const fullyCoveredTalk = {
      ...africanLionTalk,
      start_time: '13:15',
      end_time: '13:30',
   };

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, grizzly);

   assert.equal(ScheduleConflictCompatibility.canSelectConflictItem(selection, fullyCoveredTalk), false);
});

test('Test_CanSelectConflictItem_TestEarlierTalkPrecedence_ExpectLaterBlocked', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();
   const laterTalk = {
      ...amurTigerTalk,
      name: 'Later Tiger Talk',
      start_time: '13:45',
      end_time: '14:15',
   };

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, africanLionTalk);

   assert.equal(ScheduleConflictCompatibility.canSelectConflictItem(selection, amurTigerTalk), false);

   assert.equal(ScheduleConflictCompatibility.canSelectConflictItem(selection, laterTalk), true);

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, laterTalk);

   assert.equal(ScheduleConflictCompatibility.canSelectConflictItem(selection, amurTigerTalk), false);
});

test('Test_ToggleConflictItemSelection_TestNonOverlapEncounters_ExpectBothSelected', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, capybara);

   assert.deepEqual(selection.items, [greatBarrierReef, capybara]);
   assert.equal(ScheduleConflictCompatibility.canSelectConflictItem(selection, grizzly), false);
   assert.equal(ScheduleConflictCompatibility.isConflictItemSelected(selection, grizzly), false);
});

test('Test_HasAdditionalSelectableConflictItems_TestCompatible_ExpectTrue', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();
   const items = [greatBarrierReef, grizzly, capybara];

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, capybara);

   assert.equal(
      ScheduleConflictCompatibility.hasAdditionalSelectableConflictItems(items, selection),
      true
   );
   assert.equal(
      ScheduleConflictCompatibility.hasAnyAdditionalSelectableConflictItems([
         { items, selection },
      ]),
      true
   );
});

test('Test_HasAdditionalSelectableConflictItems_TestAllSelected_ExpectFalse', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();
   const items = [greatBarrierReef, grizzly, capybara];

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, capybara);

   assert.equal(
      ScheduleConflictCompatibility.hasAdditionalSelectableConflictItems(items, selection),
      false
   );
});

test('Test_HasAdditionalSelectableConflictItems_TestEmptySelection_ExpectFalse', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   assert.equal(
      ScheduleConflictCompatibility.hasAdditionalSelectableConflictItems(
         [greatBarrierReef, capybara],
         selection
      ),
      false
   );
});

test('Test_ToggleConflictItemSelection_TestToggleOff_ExpectRemoved', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.deepEqual(selection.items, []);
});
