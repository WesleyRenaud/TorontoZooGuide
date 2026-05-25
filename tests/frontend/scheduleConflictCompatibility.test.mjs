import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import {
   canSelectConflictItem,
   conflictItemRequiresTrimOverride,
   createConflictSelection,
   hasAdditionalSelectableConflictItems,
   hasAnyAdditionalSelectableConflictItems,
   isConflictItemSelected,
   scheduleTimesOverlap,
   toggleConflictItemSelection,
} from '../../scripts/itinerary/wizard/scheduleConflictCompatibility.js';

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

test('scheduleTimesOverlap matches backend half-open interval rule', () => {
   assert.equal(scheduleTimesOverlap(greatBarrierReef, grizzly), true);
   assert.equal(scheduleTimesOverlap(greatBarrierReef, capybara), false);
   assert.equal(scheduleTimesOverlap(grizzly, capybara), true);
   assert.equal(scheduleTimesOverlap(capybara, grizzly), true);
});

const gibbonTalk = {
   name: 'White-Handed Gibbon',
   start_time: '13:10',
   end_time: '13:40',
   item_type: ItinerarySaveIssueItemType.guardiansTalk,
   location: 'Indo-Malaya',
};

test('canSelectConflictItem allows a talk that is not fully covered by an encounter', () => {
   const selection = createConflictSelection();

   toggleConflictItemSelection(selection, grizzly);

   assert.equal(canSelectConflictItem(selection, africanLionTalk), true);
});

test('conflictItemRequiresTrimOverride is true for a partially overlapping talk', () => {
   const selection = createConflictSelection();

   toggleConflictItemSelection(selection, greatBarrierReef);

   assert.equal(canSelectConflictItem(selection, gibbonTalk), true);
   assert.equal(conflictItemRequiresTrimOverride(selection, gibbonTalk), true);
});

const gibbonTalkAtOne = {
   ...gibbonTalk,
   start_time: '13:00',
   end_time: '13:30',
};

test('conflictItemRequiresTrimOverride is true for an overlapping encounter when a talk is selected first', () => {
   const selection = createConflictSelection();

   toggleConflictItemSelection(selection, gibbonTalk);

   assert.equal(canSelectConflictItem(selection, greatBarrierReef), true);
   assert.equal(
      conflictItemRequiresTrimOverride(selection, greatBarrierReef),
      true
   );
});

test('canSelectConflictItem blocks an encounter that fully covers a selected talk', () => {
   const selection = createConflictSelection();

   toggleConflictItemSelection(selection, gibbonTalkAtOne);

   assert.equal(canSelectConflictItem(selection, grizzly), false);
   assert.equal(conflictItemRequiresTrimOverride(selection, grizzly), false);
});

test('conflictItemRequiresTrimOverride stays true for a selected talk that will be trimmed', () => {
   const selection = createConflictSelection();

   toggleConflictItemSelection(selection, greatBarrierReef);
   toggleConflictItemSelection(selection, gibbonTalk);

   assert.equal(
      conflictItemRequiresTrimOverride(selection, gibbonTalk),
      true
   );
});

test('conflictItemRequiresTrimOverride stays true when a talk is selected before its overlapping encounter', () => {
   const selection = createConflictSelection();

   toggleConflictItemSelection(selection, gibbonTalk);
   toggleConflictItemSelection(selection, greatBarrierReef);

   assert.equal(
      conflictItemRequiresTrimOverride(selection, gibbonTalk),
      true
   );
   assert.equal(
      conflictItemRequiresTrimOverride(selection, greatBarrierReef),
      true
   );
});

test('conflictItemRequiresTrimOverride is false when a talk does not overlap selections', () => {
   const selection = createConflictSelection();
   const laterTalk = {
      ...africanLionTalk,
      start_time: '14:00',
      end_time: '14:30',
   };

   toggleConflictItemSelection(selection, greatBarrierReef);

   assert.equal(conflictItemRequiresTrimOverride(selection, laterTalk), false);
});

test('conflictItemRequiresTrimOverride is false for non-overlapping encounters', () => {
   const selection = createConflictSelection();
   const laterTalk = {
      ...africanLionTalk,
      start_time: '14:00',
      end_time: '14:30',
   };

   toggleConflictItemSelection(selection, laterTalk);

   assert.equal(
      conflictItemRequiresTrimOverride(selection, greatBarrierReef),
      false
   );
});

test('canSelectConflictItem blocks a talk fully covered by a selected encounter', () => {
   const selection = createConflictSelection();
   const fullyCoveredTalk = {
      ...africanLionTalk,
      start_time: '13:15',
      end_time: '13:30',
   };

   toggleConflictItemSelection(selection, grizzly);

   assert.equal(canSelectConflictItem(selection, fullyCoveredTalk), false);
});

test('canSelectConflictItem gives earlier selected talks precedence over later ones', () => {
   const selection = createConflictSelection();
   const laterTalk = {
      ...amurTigerTalk,
      name: 'Later Tiger Talk',
      start_time: '13:45',
      end_time: '14:15',
   };

   toggleConflictItemSelection(selection, africanLionTalk);

   assert.equal(canSelectConflictItem(selection, amurTigerTalk), false);

   assert.equal(canSelectConflictItem(selection, laterTalk), true);

   toggleConflictItemSelection(selection, laterTalk);

   assert.equal(canSelectConflictItem(selection, amurTigerTalk), false);
});

test('toggleConflictItemSelection allows multiple non-overlapping wild encounters', () => {
   const selection = createConflictSelection();

   toggleConflictItemSelection(selection, greatBarrierReef);
   toggleConflictItemSelection(selection, capybara);

   assert.deepEqual(selection.items, [greatBarrierReef, capybara]);
   assert.equal(canSelectConflictItem(selection, grizzly), false);
   assert.equal(isConflictItemSelected(selection, grizzly), false);
});

test('hasAdditionalSelectableConflictItems detects compatible unselected activities', () => {
   const selection = createConflictSelection();
   const items = [greatBarrierReef, grizzly, capybara];

   toggleConflictItemSelection(selection, capybara);

   assert.equal(
      hasAdditionalSelectableConflictItems(items, selection),
      true
   );
   assert.equal(
      hasAnyAdditionalSelectableConflictItems([
         { items, selection },
      ]),
      true
   );
});

test('hasAdditionalSelectableConflictItems is false when all compatible activities are selected', () => {
   const selection = createConflictSelection();
   const items = [greatBarrierReef, grizzly, capybara];

   toggleConflictItemSelection(selection, greatBarrierReef);
   toggleConflictItemSelection(selection, capybara);

   assert.equal(
      hasAdditionalSelectableConflictItems(items, selection),
      false
   );
});

test('hasAdditionalSelectableConflictItems is false with no current selection', () => {
   const selection = createConflictSelection();

   assert.equal(
      hasAdditionalSelectableConflictItems(
         [greatBarrierReef, capybara],
         selection
      ),
      false
   );
});

test('toggleConflictItemSelection removes a selected activity', () => {
   const selection = createConflictSelection();

   toggleConflictItemSelection(selection, greatBarrierReef);
   toggleConflictItemSelection(selection, greatBarrierReef);

   assert.deepEqual(selection.items, []);
});
