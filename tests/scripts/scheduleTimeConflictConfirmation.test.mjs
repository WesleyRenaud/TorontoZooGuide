import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   confirmSaveIssuesConflictSelection,
   showScheduleTimeConflictConfirmation,
   WILD_ENCOUNTER_TIME_CONFLICT,
} from '../../scripts/itinerary/panel/scheduleTimeConflictConfirmation.js';
import { createConflictSelection } from '../../scripts/itinerary/wizard/scheduleConflictCompatibility.js';
import { ItinerarySaveIssueItemType } from '../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

const firstEncounter = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
};

const secondEncounter = {
   name: 'Great Barrier Reef',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
};

function cleanupPopups() {
   for (const popup of [
      ...document.querySelectorAll('.tzg-notice'),
      ...document.querySelectorAll('.tzg-confirm'),
   ]) {
      popup.__tzgPopupCleanup?.();
      popup.remove();
   }
}

test.describe('scheduleTimeConflictConfirmation', () => {
   installDomTestHooks({
      after: () => {
         cleanupPopups();
      },
   });

   test('showScheduleTimeConflictConfirmation renders the save issues notice popup', () => {
      showScheduleTimeConflictConfirmation({
         issues: [{
            type: WILD_ENCOUNTER_TIME_CONFLICT,
            items: [firstEncounter, secondEncounter],
         }],
      });

      const popup = document.querySelector('.tzg-notice');
      const title = popup?.querySelector('.itin-top-title');
      const confirmButton = popup?.querySelector('.tzg-popup-confirm');

      assert.ok(popup);
      assert.equal(
         title?.textContent,
         APP_STRINGS.itinerary.confirmation.saveIssuesTitle
      );
      assert.equal(
         confirmButton?.textContent,
         APP_STRINGS.itinerary.confirmation.saveIssuesButton
      );
      assert.ok(popup.querySelector('.itin-save-issues'));
   });

   test('showScheduleTimeConflictConfirmation confirms close through proceed confirmation', () => {
      const cancelCalls = [];

      showScheduleTimeConflictConfirmation({
         issues: [{
            type: WILD_ENCOUNTER_TIME_CONFLICT,
            items: [firstEncounter, secondEncounter],
         }],
         onCancel: () => {
            cancelCalls.push('cancelled');
         },
      });

      const noticePopup = document.querySelector('.tzg-notice');

      noticePopup?.querySelector('.itin-close')?.click();

      const proceedPopup = document.querySelector('.tzg-confirm');
      const proceedButton = proceedPopup?.querySelector('.tzg-popup-confirm');

      assert.equal(
         proceedPopup?.querySelector('.itin-top-title')?.textContent,
         APP_STRINGS.itinerary.confirmation.closeSaveIssuesTitle
      );

      proceedButton?.click();

      assert.deepEqual(cancelCalls, ['cancelled']);
      assert.equal(document.querySelector('.tzg-notice'), null);
   });

   test('showScheduleTimeConflictConfirmation resolves selected conflicts on confirm', async () => {
      const confirmedItems = [];

      showScheduleTimeConflictConfirmation({
         issues: [{
            type: WILD_ENCOUNTER_TIME_CONFLICT,
            items: [firstEncounter, secondEncounter],
         }],
         onConfirm: async (selectedItems) => {
            confirmedItems.push(selectedItems.map(item => item.name));
         },
      });

      const noticePopup = document.querySelector('.tzg-notice');
      const addButtons = noticePopup?.querySelectorAll('.itin-save-issue-select-btn') ?? [];

      addButtons[0]?.click();
      addButtons[1]?.click();
      noticePopup?.querySelector('.tzg-popup-confirm')?.click();

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.deepEqual(
         confirmedItems,
         [['From Howls to Honks', 'Great Barrier Reef']]
      );
      assert.equal(document.querySelector('.tzg-notice'), null);
   });

   test('confirmSaveIssuesConflictSelection delegates to the resolution helper', async () => {
      const selection = createConflictSelection();

      selection.items.push(firstEncounter, secondEncounter);

      const resolvedItems = [];

      const resolved = await confirmSaveIssuesConflictSelection(
         [{
            selection,
            items: [firstEncounter, secondEncounter],
         }],
         async (selectedItems) => {
            resolvedItems.push(selectedItems.map(item => item.name));
         }
      );

      assert.equal(resolved, true);
      assert.deepEqual(
         resolvedItems,
         [['From Howls to Honks', 'Great Barrier Reef']]
      );
   });
});
