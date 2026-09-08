import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ShortVisitFragment } from '../../../../scripts/itinerary/panel/shortVisitFragment.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { cleanupConfirmPopup } from '../../helpers/confirmPopupTestSetup.mjs';

installDomTestHooks({
   after: () => {
      cleanupConfirmPopup();
   },
});

test('Test_ShowShortVisitConfirmation_TestDoNotShowAgain_ExpectConfirmPopup', () => {
   const confirmCalls = [];
   const cancelCalls = [];

   ShortVisitFragment.showShortVisitConfirmation({
      onConfirm: () => {
         confirmCalls.push('confirmed');
      },
      onCancel: () => {
         cancelCalls.push('cancelled');
      },
   });

   const popup = document.querySelector('.tzg-confirm');
   const title = popup?.querySelector('.itin-top-title');
   const message = popup?.querySelector('.tzg-popup-message');
   const confirmButton = popup?.querySelector('.tzg-popup-confirm');
   const cancelButton = popup?.querySelector('.tzg-popup-cancel');

   assert.ok(popup);
   assert.equal(title?.textContent, Strings.itinerary.confirmation.shortVisitTitle);
   assert.equal(message?.textContent, Strings.itinerary.confirmation.shortVisitMessage);
   assert.ok(popup.querySelector('.tzg-popup-do-not-show-again'));

   cancelButton?.click();
   confirmButton?.click();

   assert.deepEqual(cancelCalls, ['cancelled']);
   assert.deepEqual(confirmCalls, ['confirmed']);
});
