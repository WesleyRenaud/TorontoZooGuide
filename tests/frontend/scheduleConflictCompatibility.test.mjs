import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import {
   canSelectConflictItem,
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

test('scheduleTimesOverlap matches backend half-open interval rule', () => {
   assert.equal(scheduleTimesOverlap(greatBarrierReef, grizzly), true);
   assert.equal(scheduleTimesOverlap(greatBarrierReef, capybara), false);
   assert.equal(scheduleTimesOverlap(grizzly, capybara), true);
   assert.equal(scheduleTimesOverlap(capybara, grizzly), true);
});

test('toggleConflictItemSelection allows multiple non-overlapping activities', () => {
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
