import assert from 'node:assert/strict';
import test from 'node:test';

import { showSaveIssuesProceedConfirmation } from '../../scripts/itinerary/wizard/saveIssuesProceedConfirmation.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

test('showSaveIssuesProceedConfirmation uses proceed-anyway confirm popup', () => {
   installTestWindow();
   installDocument();

   try {
      const confirmCalls = [];

      showSaveIssuesProceedConfirmation({
         title: 'Save issues title',
         message: 'Save issues message',
         onConfirm: () => {
            confirmCalls.push('confirmed');
         },
      });

      const popup = document.querySelector('.tzg-confirm');
      const title = popup?.querySelector('.itin-top-title');
      const message = popup?.querySelector('.tzg-popup-message');
      const confirmButton = popup?.querySelector('.tzg-popup-confirm');

      assert.ok(popup);
      assert.equal(title?.textContent, 'Save issues title');
      assert.equal(message?.textContent, 'Save issues message');
      assert.equal(
         confirmButton?.textContent,
         APP_STRINGS.itinerary.confirmation.proceedAnyway
      );
      assert.equal(popup.querySelector('.tzg-popup-do-not-show-again'), null);

      confirmButton?.click();

      assert.deepEqual(confirmCalls, ['confirmed']);
   }
   finally {
      document.querySelector('.tzg-confirm')?.__tzgPopupCleanup?.();
      document.querySelector('.tzg-confirm')?.remove();
      teardownDocument();
   }
});
