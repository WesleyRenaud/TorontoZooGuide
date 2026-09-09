import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { ScheduleTimeConflictResolver } from '../../../../scripts/itinerary/panel/scheduleTimeConflictResolver.js';
import { Strings } from '../../../../scripts/strings.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';
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

function _createConfirmationRecorder() {
   const calls = [];

   return {
      calls,
      confirmations: {
         showProceedWithoutSelection() {
            calls.push('without-selection');
         },
         showProceedWithUnresolved({ onConfirm } = {}) {
            calls.push('unresolved');
            return onConfirm?.();
         },
         showProceedWithAdditional({ onConfirm } = {}) {
            calls.push('additional');
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
   assert.deepEqual(calls, ['without-selection']);
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
         resolvedCalls.push(selectedItems.map(item => item.name));
      },
      confirmations
   );

   assert.equal(resolved, false);
   assert.deepEqual(calls, ['unresolved']);
   assert.deepEqual(resolvedCalls, [['From Howls to Honks']]);
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
         resolvedCalls.push(selectedItems.map(item => item.name));
      },
      confirmations
   );

   assert.equal(resolved, false);
   assert.deepEqual(calls, ['additional']);
   assert.deepEqual(resolvedCalls, [['From Howls to Honks']]);
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
         resolvedCalls.push(selectedItems.map(item => item.name));
      },
      confirmations
   );

   assert.equal(resolved, true);
   assert.deepEqual(calls, []);
   assert.deepEqual(
      resolvedCalls,
      [['From Howls to Honks', 'Great Barrier Reef']]
   );
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
         confirmCalls.push('confirmed');
      },
   });

   const popup = document.querySelector('.tzg-confirm');
   const confirmButton = popup?.querySelector('.tzg-popup-confirm');

   assert.equal(
      popup?.querySelector('.itin-top-title')?.textContent,
      Strings.itinerary.confirmation.proceedWithoutConflictSelectionTitle
   );
   assert.equal(
      popup?.querySelector('.tzg-popup-message')?.textContent,
      Strings.itinerary.confirmation.proceedWithoutConflictSelectionMessage
   );

   confirmButton?.click();

   assert.deepEqual(confirmCalls, ['confirmed']);
});

test('Test_ShowProceedWithUnresolved_TestConfirm_ExpectConfirmation', () => {
   const confirmCalls = [];
   const confirmations = ScheduleTimeConflictResolver.createScheduleTimeConflictResolutionConfirmations();

   confirmations.showProceedWithUnresolved({
      onConfirm: () => {
         confirmCalls.push('confirmed');
      },
   });

   const popup = document.querySelector('.tzg-confirm');

   assert.equal(
      popup?.querySelector('.itin-top-title')?.textContent,
      Strings.itinerary.confirmation.proceedWithUnresolvedConflictsTitle
   );
   assert.equal(
      popup?.querySelector('.tzg-popup-message')?.textContent,
      Strings.itinerary.confirmation.proceedWithUnresolvedConflictsMessage
   );

   popup?.querySelector('.tzg-popup-confirm')?.click();

   assert.deepEqual(confirmCalls, ['confirmed']);
});

test('Test_ShowProceedWithAdditional_TestConfirm_ExpectConfirmation', () => {
   const confirmCalls = [];
   const confirmations = ScheduleTimeConflictResolver.createScheduleTimeConflictResolutionConfirmations();

   confirmations.showProceedWithAdditional({
      onConfirm: () => {
         confirmCalls.push('confirmed');
      },
   });

   const popup = document.querySelector('.tzg-confirm');

   assert.equal(
      popup?.querySelector('.itin-top-title')?.textContent,
      Strings.itinerary.confirmation.proceedWithAdditionalSelectableActivitiesTitle
   );
   assert.equal(
      popup?.querySelector('.tzg-popup-message')?.textContent,
      Strings.itinerary.confirmation.proceedWithAdditionalSelectableActivitiesMessage
   );

   popup?.querySelector('.tzg-popup-confirm')?.click();

   assert.deepEqual(confirmCalls, ['confirmed']);
});
