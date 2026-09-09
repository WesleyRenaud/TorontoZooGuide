import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ScheduleTimeConflictButtonStore } from '../../../../scripts/itinerary/panel/scheduleTimeConflictButtonStore.js';
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

   assert.deepEqual(
      ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(selection, greatBarrierReef),
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
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);

   assert.deepEqual(
      ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(selection, greatBarrierReef),
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
   const selection = ScheduleConflictChecker.createConflictSelection();

   ScheduleConflictChecker.toggleConflictItemSelection(selection, grizzly);

   assert.equal(
      ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(selection, greatBarrierReef).disabled,
      true
   );
   assert.equal(
      ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(selection, africanLionTalk).requiresTrimOverride,
      ScheduleConflictChecker.conflictItemRequiresTrimOverride(selection, africanLionTalk)
   );
   assert.equal(
      ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(selection, africanLionTalk).ariaLabel,
      Strings.itinerary.aria.addToItineraryWithScheduleOverride
   );
});

test('Test_ApplyConflictSelectionButtonState_TestToggle_ExpectAttributesAndClasses', () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   const button = createDomNode('button', 'itin-save-issue-select-btn');
   const state = ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(selection, greatBarrierReef);

   ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState(button, state);

   assert.equal(button.disabled, false);
   assert.equal(button.textContent, Strings.itinerary.actions.addSymbol);
   assert.equal(
      button.getAttribute('aria-label'),
      Strings.itinerary.aria.addToItinerary
   );
   assert.equal(button.classList.contains('is-added'), false);
   assert.equal(button.classList.contains('requires-trim-override'), false);

   ScheduleConflictChecker.toggleConflictItemSelection(selection, greatBarrierReef);
   ScheduleTimeConflictButtonStore.applyConflictSelectionButtonState(
      button,
      ScheduleTimeConflictButtonStore.getConflictSelectionButtonState(selection, greatBarrierReef)
   );

   assert.equal(button.textContent, Strings.itinerary.actions.remove);
   assert.equal(button.classList.contains('is-added'), true);
   assert.equal(
      ScheduleConflictChecker.isConflictItemSelected(selection, greatBarrierReef),
      true
   );
   assert.equal(
      ScheduleConflictChecker.canSelectConflictItem(selection, greatBarrierReef),
      true
   );
});
