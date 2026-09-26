import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleTimeConflictResolver } from '../../../../scripts/itinerary/panel/scheduleTimeConflictResolver.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

const firstEncounter = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
};

const secondEncounter = {
   name: 'Great Barrier Reef',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
};

const thirdEncounter = {
   name: 'Savanna Safari',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
};

const withoutSelectionCall = 'without-selection';
const unresolvedCall = 'unresolved';
const additionalCall = 'additional';
const confirmedCall = 'confirmed';

function _createConfirmationRecorder() {
   const calls = [];

   return {
      calls,
      confirmations: {
         showProceedWithoutSelection() {
            calls.push(withoutSelectionCall);
         },
         showProceedWithUnresolved({ onConfirm } = {}) {
            calls.push(unresolvedCall);
            return onConfirm?.();
         },
         showProceedWithAdditional({ onConfirm } = {}) {
            calls.push(additionalCall);
            return onConfirm?.();
         },
      },
   };
}

installDomTestHooks({
   after: () => {
      document.querySelector('.tzg-confirm')?.__tzgPopupCleanup?.();
      document.querySelector('.tzg-confirm')?.remove();
   },
});


test('Test_ResolveScheduleTimeConflictSelection_TestNothingSelected_ExpectPrompt', async () => {
   const { calls, confirmations } = _createConfirmationRecorder();
   const resolvedCalls = [];

   const resolved = await ScheduleTimeConflictResolver.resolveScheduleTimeConflictSelection(
      [{
         selection: ScheduleConflictChecker.createConflictSelection(),
         items: [firstEncounter, secondEncounter],
      }],
      async (selectedItems) => {
         resolvedCalls.push(selectedItems);
      },
      confirmations
   );

   assert.equal(resolved, false);
   assert.deepEqual(calls, [withoutSelectionCall]);
   assert.deepEqual(resolvedCalls, []);
});


test('Test_ResolveScheduleTimeConflictSelection_TestUnresolvedGroups_ExpectPrompt', async () => {
   const { calls, confirmations } = _createConfirmationRecorder();
   const resolvedCalls = [];
   const firstSelection = ScheduleConflictChecker.createConflictSelection();
   const secondSelection = ScheduleConflictChecker.createConflictSelection();
   firstSelection.items.push(firstEncounter);

   const resolved = await ScheduleTimeConflictResolver.resolveScheduleTimeConflictSelection(
      [
         {
            selection: firstSelection,
            items: [firstEncounter, secondEncounter],
         },
         {
            selection: secondSelection,
            items: [thirdEncounter],
         },
      ],
      async (selectedItems) => {
         resolvedCalls.push(selectedItems.map((item) => item.name));
      },
      confirmations
   );

   assert.equal(resolved, false);
   assert.deepEqual(calls, [unresolvedCall]);
   assert.deepEqual(resolvedCalls, [[firstEncounter.name]]);
});


test('Test_ResolveScheduleTimeConflictSelection_TestAdditionalActivities_ExpectPrompt', async () => {
   const { calls, confirmations } = _createConfirmationRecorder();
   const resolvedCalls = [];
   const selection = ScheduleConflictChecker.createConflictSelection();
   selection.items.push(firstEncounter);

   const resolved = await ScheduleTimeConflictResolver.resolveScheduleTimeConflictSelection(
      [{
         selection,
         items: [firstEncounter, thirdEncounter],
      }],
      async (selectedItems) => {
         resolvedCalls.push(selectedItems.map((item) => item.name));
      },
      confirmations
   );

   assert.equal(resolved, false);
   assert.deepEqual(calls, [additionalCall]);
   assert.deepEqual(resolvedCalls, [[firstEncounter.name]]);
});


test('Test_ResolveScheduleTimeConflictSelection_TestAllSettled_ExpectResolved', async () => {
   const { calls, confirmations } = _createConfirmationRecorder();
   const resolvedCalls = [];
   const selection = ScheduleConflictChecker.createConflictSelection();
   selection.items.push(firstEncounter, secondEncounter);

   const resolved = await ScheduleTimeConflictResolver.resolveScheduleTimeConflictSelection(
      [{
         selection,
         items: [firstEncounter, secondEncounter],
      }],
      async (selectedItems) => {
         resolvedCalls.push(selectedItems.map((item) => item.name));
      },
      confirmations
   );

   assert.equal(resolved, true);
   assert.deepEqual(calls, []);
   assert.deepEqual(resolvedCalls, [[firstEncounter.name, secondEncounter.name]]);
});


test('Test_ShowProceedWithoutSelection_TestDefaultHandler_ExpectNoOp', () => {
   const confirmations = ScheduleTimeConflictResolver.createScheduleTimeConflictResolutionConfirmations();

   confirmations.showProceedWithoutSelection();
   const popup = document.querySelector('.tzg-confirm');

   assert.doesNotThrow(() => {
      popup?.querySelector('.tzg-popup-confirm')?.click();
   });
});


test('Test_ShowProceedWithoutSelection_TestCustomHandler_ExpectConfirmation', () => {
   const confirmCalls = [];
   const confirmations = ScheduleTimeConflictResolver.createScheduleTimeConflictResolutionConfirmations();

   confirmations.showProceedWithoutSelection({
      onConfirm: () => {
         confirmCalls.push(confirmedCall);
      },
   });
   const popup = document.querySelector('.tzg-confirm');
   const confirmButton = popup?.querySelector('.tzg-popup-confirm');
   const title = popup?.querySelector('.itin-top-title')?.textContent;
   const message = popup?.querySelector('.tzg-popup-message')?.textContent;

   assert.equal(title, Strings.itinerary.confirmation.proceedWithoutConflictSelectionTitle);
   assert.equal(message, Strings.itinerary.confirmation.proceedWithoutConflictSelectionMessage);

   confirmButton?.click();

   assert.deepEqual(confirmCalls, [confirmedCall]);
});


test('Test_ShowProceedWithUnresolved_TestConfirm_ExpectConfirmation', () => {
   const confirmCalls = [];
   const confirmations = ScheduleTimeConflictResolver.createScheduleTimeConflictResolutionConfirmations();

   confirmations.showProceedWithUnresolved({
      onConfirm: () => {
         confirmCalls.push(confirmedCall);
      },
   });
   const popup = document.querySelector('.tzg-confirm');
   const title = popup?.querySelector('.itin-top-title')?.textContent;
   const message = popup?.querySelector('.tzg-popup-message')?.textContent;

   assert.equal(title, Strings.itinerary.confirmation.proceedWithUnresolvedConflictsTitle);
   assert.equal(message, Strings.itinerary.confirmation.proceedWithUnresolvedConflictsMessage);

   popup?.querySelector('.tzg-popup-confirm')?.click();

   assert.deepEqual(confirmCalls, [confirmedCall]);
});


test('Test_ShowProceedWithAdditional_TestConfirm_ExpectConfirmation', () => {
   const confirmCalls = [];
   const confirmations = ScheduleTimeConflictResolver.createScheduleTimeConflictResolutionConfirmations();

   confirmations.showProceedWithAdditional({
      onConfirm: () => {
         confirmCalls.push(confirmedCall);
      },
   });
   const popup = document.querySelector('.tzg-confirm');
   const title = popup?.querySelector('.itin-top-title')?.textContent;
   const message = popup?.querySelector('.tzg-popup-message')?.textContent;

   assert.equal(title, Strings.itinerary.confirmation.proceedWithAdditionalSelectableActivitiesTitle);
   assert.equal(message, Strings.itinerary.confirmation.proceedWithAdditionalSelectableActivitiesMessage);

   popup?.querySelector('.tzg-popup-confirm')?.click();

   assert.deepEqual(confirmCalls, [confirmedCall]);
});
