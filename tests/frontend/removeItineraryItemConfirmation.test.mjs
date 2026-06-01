import assert from 'node:assert/strict';
import { test } from 'node:test';

import { showRemoveItineraryItemConfirmation } from '../../scripts/itinerary/panel/removeItineraryItemConfirmation.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

test('showRemoveItineraryItemConfirmation uses confirm popup without do-not-show-again', () => {
   installTestWindow();
   installDocument();

   try {
      const confirmCalls = [];

      showRemoveItineraryItemConfirmation({
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
      assert.equal(title?.textContent, strings.removeItemTitle);
      assert.equal(message?.textContent, strings.removeItemMessage);
      assert.equal(popup.querySelector('.tzg-popup-do-not-show-again'), null);
      assert.equal(confirmButton?.textContent, APP_STRINGS.itinerary.dayPlanner.remove);

      confirmButton?.click();

      assert.deepEqual(confirmCalls, ['confirmed']);
   }
   finally {
      document.querySelector('.tzg-confirm')?.__tzgPopupCleanup?.();
      document.querySelector('.tzg-confirm')?.remove();
      teardownDocument();
   }
});
