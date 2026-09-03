import assert from 'node:assert/strict';
import { test } from 'node:test';

import { showShortVisitConfirmation } from '../../scripts/itinerary/panel/shortVisitConfirmation.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { cleanupConfirmPopup } from './helpers/confirmPopupTestSetup.mjs';

test.describe('shortVisitConfirmation', () => {
   installDomTestHooks({
      after: () => {
         cleanupConfirmPopup();
      },
   });

   test('showShortVisitConfirmation uses do-not-show-again confirm popup on itinerary panel', () => {
      const confirmCalls = [];
      const cancelCalls = [];

      showShortVisitConfirmation({
         onConfirm: () => {
            confirmCalls.push('confirmed');
         },
         onCancel: () => {
            cancelCalls.push('cancelled');
         },
      });

      const popup = document.querySelector('.tzg-confirm');
      const strings = APP_STRINGS.itinerary.confirmation;
      const title = popup?.querySelector('.itin-top-title');
      const message = popup?.querySelector('.tzg-popup-message');
      const confirmButton = popup?.querySelector('.tzg-popup-confirm');
      const cancelButton = popup?.querySelector('.tzg-popup-cancel');

      assert.ok(popup);
      assert.equal(title?.textContent, strings.shortVisitTitle);
      assert.equal(message?.textContent, strings.shortVisitMessage);
      assert.ok(popup.querySelector('.tzg-popup-do-not-show-again'));

      cancelButton?.click();
      confirmButton?.click();

      assert.deepEqual(cancelCalls, ['cancelled']);
      assert.deepEqual(confirmCalls, ['confirmed']);
   });
});
