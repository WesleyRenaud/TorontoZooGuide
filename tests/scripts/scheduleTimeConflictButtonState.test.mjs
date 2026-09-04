import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import {
   applyConflictSelectionButtonState,
   getConflictSelectionButtonState,
} from '../../scripts/itinerary/panel/scheduleTimeConflictButtonState.js';
import { ScheduleConflictCompatibility } from '../../scripts/itinerary/wizard/scheduleConflictCompatibility.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';

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

const africanLionTalk = {
   name: 'African Lion',
   start_time: '13:30',
   end_time: '14:00',
   item_type: ItinerarySaveIssueItemType.guardiansTalk,
   location: 'Africa Savanna',
};

test('getConflictSelectionButtonState marks unselected selectable items as add actions', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   assert.deepEqual(
      getConflictSelectionButtonState(selection, greatBarrierReef),
      {
         selected: false,
         selectable: true,
         requiresTrimOverride: false,
         disabled: false,
         textContent: APP_STRINGS.itinerary.actions.addSymbol,
         ariaLabel: APP_STRINGS.itinerary.aria.addToItinerary,
      }
   );
});

test('getConflictSelectionButtonState marks selected items as remove actions', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.deepEqual(
      getConflictSelectionButtonState(selection, greatBarrierReef),
      {
         selected: true,
         selectable: true,
         requiresTrimOverride: false,
         disabled: false,
         textContent: APP_STRINGS.itinerary.actions.remove,
         ariaLabel: APP_STRINGS.itinerary.aria.removeFromItinerary,
      }
   );
});

test('getConflictSelectionButtonState disables blocked items and flags trim overrides', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, grizzly);

   assert.equal(
      getConflictSelectionButtonState(selection, greatBarrierReef).disabled,
      true
   );
   assert.equal(
      getConflictSelectionButtonState(selection, africanLionTalk).requiresTrimOverride,
      ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, africanLionTalk)
   );
   assert.equal(
      getConflictSelectionButtonState(selection, africanLionTalk).ariaLabel,
      APP_STRINGS.itinerary.aria.addToItineraryWithScheduleOverride
   );
});

test('applyConflictSelectionButtonState updates button attributes and classes', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();
   const button = createDomNode('button', 'itin-save-issue-select-btn');
   const state = getConflictSelectionButtonState(selection, greatBarrierReef);

   applyConflictSelectionButtonState(button, state);

   assert.equal(button.disabled, false);
   assert.equal(button.textContent, APP_STRINGS.itinerary.actions.addSymbol);
   assert.equal(
      button.getAttribute('aria-label'),
      APP_STRINGS.itinerary.aria.addToItinerary
   );
   assert.equal(button.classList.contains('is-added'), false);
   assert.equal(button.classList.contains('requires-trim-override'), false);

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);
   applyConflictSelectionButtonState(
      button,
      getConflictSelectionButtonState(selection, greatBarrierReef)
   );

   assert.equal(button.textContent, APP_STRINGS.itinerary.actions.remove);
   assert.equal(button.classList.contains('is-added'), true);
   assert.equal(
      ScheduleConflictCompatibility.isConflictItemSelected(selection, greatBarrierReef),
      true
   );
   assert.equal(
      ScheduleConflictCompatibility.canSelectConflictItem(selection, greatBarrierReef),
      true
   );
});
