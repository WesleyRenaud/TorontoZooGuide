import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleTimeConflictFragment } from '../../../../scripts/itinerary/panel/scheduleTimeConflictFragment.js';
import { ScheduleTimeConflictResolver } from '../../../../scripts/itinerary/panel/scheduleTimeConflictResolver.js';
import { ScheduleConflictChecker } from '../../../../scripts/itinerary/wizard/scheduleConflictChecker.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
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
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
};

function _cleanupPopups() {
   for (const popup of [
      ...document.querySelectorAll('.tzg-notice'),
      ...document.querySelectorAll('.tzg-confirm'),
   ]) {
      popup.__tzgPopupCleanup?.();
      popup.remove();
   }
}

installDomTestHooks({
   after: () => {
      _cleanupPopups();
   },
});


test('Test_ShowScheduleTimeConflictConfirmation_TestIssues_ExpectNoticePopup', () => {
   const issues = [{
      type: ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
      items: [firstEncounter, secondEncounter],
   }];

   ScheduleTimeConflictFragment.showScheduleTimeConflictConfirmation({ issues });

   const popup = document.querySelector('.tzg-notice');
   const title = popup?.querySelector('.itin-top-title');
   const confirmButton = popup?.querySelector('.tzg-popup-confirm');

   assert.ok(popup);
   assert.equal(title?.textContent, Strings.itinerary.confirmation.saveIssuesTitle);
   assert.equal(confirmButton?.textContent, Strings.itinerary.confirmation.saveIssuesButton);
   assert.ok(popup.querySelector('.itin-save-issues'));
});


test('Test_ShowScheduleTimeConflictConfirmation_TestClose_ExpectCancelled', () => {
   const cancelled = 'cancelled';
   const cancelCalls = [];
   const issues = [{
      type: ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
      items: [firstEncounter, secondEncounter],
   }];

   ScheduleTimeConflictFragment.showScheduleTimeConflictConfirmation({
      issues,
      onCancel: () => {
         cancelCalls.push(cancelled);
      },
   });
   const noticePopup = document.querySelector('.tzg-notice');
   noticePopup?.querySelector('.itin-close')?.click();
   const proceedPopup = document.querySelector('.tzg-confirm');
   const proceedButton = proceedPopup?.querySelector('.tzg-popup-confirm');

   proceedButton?.click();

   assert.equal(
      proceedPopup?.querySelector('.itin-top-title')?.textContent,
      Strings.itinerary.confirmation.closeSaveIssuesTitle
   );
   assert.deepEqual(cancelCalls, [cancelled]);
   assert.equal(document.querySelector('.tzg-notice'), null);
});


test('Test_ShowScheduleTimeConflictConfirmation_TestConfirm_ExpectSelectedItems', async () => {
   const confirmedItems = [];
   const issues = [{
      type: ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
      items: [firstEncounter, secondEncounter],
   }];

   ScheduleTimeConflictFragment.showScheduleTimeConflictConfirmation({
      issues,
      onConfirm: async (selectedItems) => {
         confirmedItems.push(selectedItems.map((item) => item.name));
      },
   });
   const noticePopup = document.querySelector('.tzg-notice');
   const addButtons = noticePopup?.querySelectorAll('.itin-save-issue-select-btn') ?? [];
   addButtons.at(Position.FIRST)?.click();
   addButtons.at(Position.SECOND)?.click();
   noticePopup?.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.deepEqual(confirmedItems, [[firstEncounter.name, secondEncounter.name]]);
   assert.equal(document.querySelector('.tzg-notice'), null);
});


test('Test_ConfirmSaveIssuesConflictSelection_TestSelected_ExpectResolved', async () => {
   const selection = ScheduleConflictChecker.createConflictSelection();
   selection.items.push(firstEncounter, secondEncounter);
   const resolvedItems = [];

   const resolved = await ScheduleTimeConflictFragment.confirmSaveIssuesConflictSelection(
      [{
         selection,
         items: [firstEncounter, secondEncounter],
      }],
      async (selectedItems) => {
         resolvedItems.push(selectedItems.map((item) => item.name));
      }
   );

   assert.equal(resolved, true);
   assert.deepEqual(resolvedItems, [[firstEncounter.name, secondEncounter.name]]);
});


test('Test_ShowScheduleTimeConflictConfirmation_TestUnresolvedSelection_ExpectKeepOpen', async () => {
   const originalResolve = ScheduleTimeConflictResolver.resolveScheduleTimeConflictSelection;
   ScheduleTimeConflictResolver.resolveScheduleTimeConflictSelection = async () => false;
   const issues = [{
      type: ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
      items: [firstEncounter, secondEncounter],
   }];

   try {
      ScheduleTimeConflictFragment.showScheduleTimeConflictConfirmation({
         issues,
         onConfirm: async () => {},
      });
      const noticePopup = document.querySelector('.tzg-notice');
      noticePopup?.querySelector('.tzg-popup-confirm')?.click();

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.ok(document.querySelector('.tzg-notice'));
   } finally {
      ScheduleTimeConflictResolver.resolveScheduleTimeConflictSelection = originalResolve;
   }
});
