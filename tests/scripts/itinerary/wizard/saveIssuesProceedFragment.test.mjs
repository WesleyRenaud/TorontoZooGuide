import assert from 'node:assert/strict';
import { test } from 'node:test';

import { SaveIssuesProceedFragment } from '../../../../scripts/itinerary/wizard/saveIssuesProceedFragment.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { cleanupConfirmPopup } from '../../helpers/confirmPopupTestSetup.mjs';

installDomTestHooks({
   after: () => {
      cleanupConfirmPopup();
   },
});


test('Test_ShowSaveIssuesProceedConfirmation_TestProceed_ExpectConfirmPopup', () => {
   const confirmCalls = [];
   const titleText = 'Save issues title';
   const messageText = 'Save issues message';
   const confirmed = 'confirmed';

   SaveIssuesProceedFragment.showSaveIssuesProceedConfirmation({
      title: titleText,
      message: messageText,
      onConfirm: () => {
         confirmCalls.push(confirmed);
      },
   });

   const popup = document.querySelector('.tzg-confirm');
   const title = popup?.querySelector('.itin-top-title');
   const message = popup?.querySelector('.tzg-popup-message');
   const confirmButton = popup?.querySelector('.tzg-popup-confirm');

   assert.ok(popup);
   assert.equal(title?.textContent, titleText);
   assert.equal(message?.textContent, messageText);
   assert.equal(
      confirmButton?.textContent,
      Strings.itinerary.confirmation.proceedAnyway
   );
   assert.equal(popup.querySelector('.tzg-popup-do-not-show-again'), null);

   confirmButton?.click();

   assert.deepEqual(confirmCalls, [confirmed]);
});
