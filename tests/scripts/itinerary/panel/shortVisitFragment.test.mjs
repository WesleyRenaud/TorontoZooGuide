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


test('Test_ShowShortVisitConfirmation_TestDefaults_ExpectPopup', () => {
   ShortVisitFragment.showShortVisitConfirmation({});

   const popup = document.querySelector('.tzg-confirm');
   const title = popup?.querySelector('.itin-top-title');
   const message = popup?.querySelector('.tzg-popup-message');

   assert.ok(popup);
   assert.equal(title?.textContent, Strings.itinerary.confirmation.shortVisitTitle);
   assert.equal(message?.textContent, Strings.itinerary.confirmation.shortVisitMessage);
   assert.ok(popup.querySelector('.tzg-popup-do-not-show-again'));
});


test('Test_ShowShortVisitConfirmation_TestCancel_ExpectCancelled', () => {
   const cancelled = 'cancelled';
   const cancelCalls = [];

   ShortVisitFragment.showShortVisitConfirmation({
      onCancel: () => {
         cancelCalls.push(cancelled);
      },
   });
   const cancelButton = document.querySelector('.tzg-popup-cancel');

   cancelButton?.click();

   assert.deepEqual(cancelCalls, [cancelled]);
});


test('Test_ShowShortVisitConfirmation_TestConfirm_ExpectConfirmed', () => {
   const confirmed = 'confirmed';
   const confirmCalls = [];

   ShortVisitFragment.showShortVisitConfirmation({
      onConfirm: () => {
         confirmCalls.push(confirmed);
      },
   });
   const confirmButton = document.querySelector('.tzg-popup-confirm');

   confirmButton?.click();

   assert.deepEqual(confirmCalls, [confirmed]);
});
