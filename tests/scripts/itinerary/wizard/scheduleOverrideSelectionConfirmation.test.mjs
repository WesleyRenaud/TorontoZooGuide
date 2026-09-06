import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleOverrideSelectionConfirmation } from '../../../../scripts/itinerary/wizard/scheduleOverrideSelectionConfirmation.js';
import { Strings } from '../../../../scripts/strings.js';
import { cleanupConfirmPopup } from '../../helpers/confirmPopupTestSetup.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

test('Test_ScheduleOverrideSelectionConfirmation_TestCopy_ExpectDefined', () => {
   assert.equal(
      Strings.itinerary.confirmation.scheduleOverrideSelectionTitle,
      'Adjust Activity Times?'
   );
   assert.match(
      Strings.itinerary.confirmation.scheduleOverrideSelectionMessage,
      /overlap in time/
   );
   assert.match(
      Strings.itinerary.confirmation.scheduleOverrideSelectionMessage,
      /Wild Encounters taking priority/
   );
});

test.describe('showScheduleOverrideSelectionConfirmation', () => {
   installDomTestHooks({
      after: () => {
         cleanupConfirmPopup();
      },
   });

   test('Test_ShowScheduleOverrideSelectionConfirmation_TestOverride_ExpectConfirmPopup', () => {
      const confirmCalls = [];

      ScheduleOverrideSelectionConfirmation.showScheduleOverrideSelectionConfirmation({
         onConfirm: () => {
            confirmCalls.push('confirmed');
         },
      });

      const popup = document.querySelector('.tzg-confirm');
      const title = popup?.querySelector('.itin-top-title');
      const message = popup?.querySelector('.tzg-popup-message');
      const confirmButton = popup?.querySelector('.tzg-popup-confirm');

      assert.ok(popup);
      assert.equal(title?.textContent, Strings.itinerary.confirmation.scheduleOverrideSelectionTitle);
      assert.equal(message?.textContent, Strings.itinerary.confirmation.scheduleOverrideSelectionMessage);
      assert.equal(confirmButton?.textContent, Strings.itinerary.confirmation.saveIssuesButton);
      assert.equal(popup.querySelector('.tzg-popup-do-not-show-again'), null);

      confirmButton?.click();

      assert.deepEqual(confirmCalls, ['confirmed']);
   });
});
