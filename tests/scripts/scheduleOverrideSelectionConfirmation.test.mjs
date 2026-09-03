import assert from 'node:assert/strict';
import { test } from 'node:test';

import { showScheduleOverrideSelectionConfirmation } from '../../scripts/itinerary/wizard/scheduleOverrideSelectionConfirmation.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { cleanupConfirmPopup } from './helpers/confirmPopupTestSetup.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

test('schedule override selection confirmation copy is defined', () => {
   assert.equal(
      APP_STRINGS.itinerary.confirmation.scheduleOverrideSelectionTitle,
      'Adjust Activity Times?'
   );
   assert.match(
      APP_STRINGS.itinerary.confirmation.scheduleOverrideSelectionMessage,
      /overlap in time/
   );
   assert.match(
      APP_STRINGS.itinerary.confirmation.scheduleOverrideSelectionMessage,
      /Wild Encounters taking priority/
   );
});

test.describe('showScheduleOverrideSelectionConfirmation', () => {
   installDomTestHooks({
      after: () => {
         cleanupConfirmPopup();
      },
   });

   test('showScheduleOverrideSelectionConfirmation uses schedule override confirm popup', () => {
      const confirmCalls = [];

      showScheduleOverrideSelectionConfirmation({
         onConfirm: () => {
            confirmCalls.push('confirmed');
         },
      });

      const popup = document.querySelector('.tzg-confirm');
      const strings = APP_STRINGS.itinerary.confirmation;
      const title = popup?.querySelector('.itin-top-title');
      const message = popup?.querySelector('.tzg-popup-message');
      const confirmButton = popup?.querySelector('.tzg-popup-confirm');

      assert.ok(popup);
      assert.equal(title?.textContent, strings.scheduleOverrideSelectionTitle);
      assert.equal(message?.textContent, strings.scheduleOverrideSelectionMessage);
      assert.equal(confirmButton?.textContent, strings.saveIssuesButton);
      assert.equal(popup.querySelector('.tzg-popup-do-not-show-again'), null);

      confirmButton?.click();

      assert.deepEqual(confirmCalls, ['confirmed']);
   });
});
