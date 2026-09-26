import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleTimeConflictButtonStore } from '../../../../scripts/itinerary/panel/scheduleTimeConflictButtonStore.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';
import { Strings } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';

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

const africanLionTalk = {
   name: 'African Lion',
   start_time: '13:30',
   end_time: '14:00',
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   location: 'Africa Savanna',
};


test('Test_GetConflictSelectionButtonState_TestUnselectedSelectable_ExpectAddAction', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();

   const state = ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(
      selection,
      greatBarrierReef
   );

   assert.deepEqual(state, {
      selected: false,
      selectable: true,
      requiresTrimOverride: false,
      disabled: false,
      textContent: Strings.itinerary.actions.addSymbol,
      ariaLabel: Strings.itinerary.aria.addToItinerary,
   });
});


test('Test_GetConflictSelectionButtonState_TestSelected_ExpectRemoveAction', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   const state = ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(
      selection,
      greatBarrierReef
   );

   assert.deepEqual(state, {
      selected: true,
      selectable: true,
      requiresTrimOverride: false,
      disabled: false,
      textContent: Strings.itinerary.actions.remove,
      ariaLabel: Strings.itinerary.aria.removeFromItinerary,
   });
});


test('Test_GetConflictSelectionButtonState_TestBlocked_ExpectDisabled', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, grizzly);

   const state = ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(
      selection,
      greatBarrierReef
   );

   assert.equal(state.disabled, true);
});


test('Test_GetConflictSelectionButtonState_TestTrimOverride_ExpectOverrideAria', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   ScheduleConflictChecker.toggleConflictItemSelection(selection, grizzly);

   const state = ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(
      selection,
      africanLionTalk
   );

   assert.equal(
      state.requiresTrimOverride,
      ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, africanLionTalk)
   );
   assert.equal(state.ariaLabel, Strings.itinerary.aria.addToItineraryWithScheduleOverride);
});


test('Test_ApplyConflictSelectionButtonState_TestUnselected_ExpectAddAttributes', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const button = createDomNode('button', 'itin-save-issue-select-btn');
   const state = ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(
      selection,
      greatBarrierReef
   );

   ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState(button, state);

   assert.equal(button.disabled, state.disabled);
   assert.equal(button.textContent, state.textContent);
   assert.equal(button.getAttribute('aria-label'), state.ariaLabel);
   assert.equal(button.classList.contains('is-added'), state.selected);
   assert.equal(button.classList.contains('requires-trim-override'), state.requiresTrimOverride);
});


test('Test_ApplyConflictSelectionButtonState_TestSelected_ExpectRemoveAttributes', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const button = createDomNode('button', 'itin-save-issue-select-btn');
   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);
   const state = ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(
      selection,
      greatBarrierReef
   );

   ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState(button, state);

   assert.equal(button.textContent, Strings.itinerary.actions.remove);
   assert.equal(button.classList.contains('is-added'), true);
   assert.equal(ScheduleConflictChecker.isConflictItemSelected(selection, greatBarrierReef), true);
   assert.equal(ScheduleConflictChecker.canSelectConflictItem(selection, greatBarrierReef), true);
});
