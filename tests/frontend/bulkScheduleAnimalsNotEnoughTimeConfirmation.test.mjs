import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME_ISSUE,
   hasBulkScheduleAnimalsNotEnoughTimeIssue,
   showBulkScheduleAnimalsNotEnoughTimeNotice,
} from '../../scripts/itinerary/panel/bulkScheduleAnimalsNotEnoughTimeConfirmation.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

test('hasBulkScheduleAnimalsNotEnoughTimeIssue detects backend issue type', () => {
   assert.equal(hasBulkScheduleAnimalsNotEnoughTimeIssue([]), false);
   assert.equal(
      hasBulkScheduleAnimalsNotEnoughTimeIssue([
         { type: BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME_ISSUE, items: [] },
      ]),
      true
   );
   assert.equal(
      hasBulkScheduleAnimalsNotEnoughTimeIssue([{ type: 'otherIssue', items: [] }]),
      false
   );
});

test('showBulkScheduleAnimalsNotEnoughTimeNotice uses accept-only notice popup', () => {
   installTestWindow();
   installDocument();

   try {
      const confirmCalls = [];

      showBulkScheduleAnimalsNotEnoughTimeNotice({
         onConfirm: () => {
            confirmCalls.push('confirmed');
         },
      });

      const popup = document.querySelector('.tzg-notice');
      const strings = APP_STRINGS.itinerary.confirmation;
      const title = popup?.querySelector('.itin-top-title');
      const message = popup?.querySelector('.tzg-popup-message');
      const okButton = popup?.querySelector('.tzg-popup-confirm');
      const cancelButton = popup?.querySelector('.tzg-popup-cancel');

      assert.ok(popup);
      assert.equal(title?.textContent, strings.bulkScheduleAnimalsNotEnoughTimeTitle);
      assert.equal(message?.textContent, strings.bulkScheduleAnimalsNotEnoughTimeMessage);
      assert.equal(popup.querySelector('.tzg-bulk-schedule-animals-list'), null);
      assert.equal(okButton?.textContent, APP_STRINGS.itinerary.noItemsSelected.button);
      assert.equal(cancelButton, null);

      okButton?.click();

      assert.deepEqual(confirmCalls, ['confirmed']);
   }
   finally {
      document.querySelector('.tzg-notice')?.__tzgPopupCleanup?.();
      document.querySelector('.tzg-notice')?.remove();
      teardownDocument();
   }
});
