import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ScheduleTimeConflictButtonState } from '../../../../scripts/itinerary/panel/scheduleTimeConflictButtonState.js';
import { ScheduleConflictCompatibility } from '../../../../scripts/itinerary/wizard/scheduleConflictCompatibility.js';
import { Strings } from '../../../../scripts/strings.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';

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

test('Test_GetConflictSelectionButtonState_TestUnselectedSelectable_ExpectAddAction', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   assert.deepEqual(
      ScheduleTimeConflictButtonState.getConflictSelectionButtonState(selection, greatBarrierReef),
      {
         selected: false,
         selectable: true,
         requiresTrimOverride: false,
         disabled: false,
         textContent: Strings.itinerary.actions.addSymbol,
         ariaLabel: Strings.itinerary.aria.addToItinerary,
      }
   );
});

test('Test_GetConflictSelectionButtonState_TestSelected_ExpectRemoveAction', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.deepEqual(
      ScheduleTimeConflictButtonState.getConflictSelectionButtonState(selection, greatBarrierReef),
      {
         selected: true,
         selectable: true,
         requiresTrimOverride: false,
         disabled: false,
         textContent: Strings.itinerary.actions.remove,
         ariaLabel: Strings.itinerary.aria.removeFromItinerary,
      }
   );
});

test('Test_GetConflictSelectionButtonState_TestBlockedAndTrim_ExpectDisabledAndOverride', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, grizzly);

   assert.equal(
      ScheduleTimeConflictButtonState.getConflictSelectionButtonState(selection, greatBarrierReef).disabled,
      true
   );
   assert.equal(
      ScheduleTimeConflictButtonState.getConflictSelectionButtonState(selection, africanLionTalk).requiresTrimOverride,
      ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(selection, africanLionTalk)
   );
   assert.equal(
      ScheduleTimeConflictButtonState.getConflictSelectionButtonState(selection, africanLionTalk).ariaLabel,
      Strings.itinerary.aria.addToItineraryWithScheduleOverride
   );
});

test('Test_ApplyConflictSelectionButtonState_TestToggle_ExpectAttributesAndClasses', () => {
   const selection = ScheduleConflictCompatibility.createConflictSelection();
   const button = createDomNode('button', 'itin-save-issue-select-btn');
   const state = ScheduleTimeConflictButtonState.getConflictSelectionButtonState(selection, greatBarrierReef);

   ScheduleTimeConflictButtonState.applyConflictSelectionButtonState(button, state);

   assert.equal(button.disabled, false);
   assert.equal(button.textContent, Strings.itinerary.actions.addSymbol);
   assert.equal(
      button.getAttribute('aria-label'),
      Strings.itinerary.aria.addToItinerary
   );
   assert.equal(button.classList.contains('is-added'), false);
   assert.equal(button.classList.contains('requires-trim-override'), false);

   ScheduleConflictCompatibility.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleTimeConflictButtonState.applyConflictSelectionButtonState(
      button,
      ScheduleTimeConflictButtonState.getConflictSelectionButtonState(selection, greatBarrierReef)
   );

   assert.equal(button.textContent, Strings.itinerary.actions.remove);
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
