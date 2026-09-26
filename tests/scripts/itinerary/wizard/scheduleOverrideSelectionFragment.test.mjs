import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleOverrideSelectionFragment } from '../../../../scripts/itinerary/wizard/scheduleOverrideSelectionFragment.js';
import { Strings } from '../../../../scripts/strings.js';
import { cleanupConfirmPopup } from '../../helpers/confirmPopupTestSetup.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks({
   after: () => {
      cleanupConfirmPopup();
   },
});


test('Test_ScheduleOverrideSelectionConfirmation_TestTitle_ExpectDefined', () => {
   const title = Strings.itinerary.confirmation.scheduleOverrideSelectionTitle;

   assert.equal(title, 'Adjust Activity Times?');
});


test('Test_ScheduleOverrideSelectionConfirmation_TestOverlapCopy_ExpectDefined', () => {
   const message = Strings.itinerary.confirmation.scheduleOverrideSelectionMessage;

   assert.match(message, /overlap in time/);
});


test('Test_ScheduleOverrideSelectionConfirmation_TestPriorityCopy_ExpectDefined', () => {
   const message = Strings.itinerary.confirmation.scheduleOverrideSelectionMessage;

   assert.match(message, /Wild Encounters taking priority/);
});


test('Test_ShowScheduleOverrideSelectionConfirmation_TestOverride_ExpectConfirmPopup', () => {
   const confirmCalls = [];
   const confirmed = 'confirmed';

   ScheduleOverrideSelectionFragment.showScheduleOverrideSelectionConfirmation({
      onConfirm: () => {
         confirmCalls.push(confirmed);
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

   assert.deepEqual(confirmCalls, [confirmed]);
});
