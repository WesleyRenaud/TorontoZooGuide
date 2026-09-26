import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RemoveItineraryItemFragment } from '../../../../scripts/itinerary/panel/removeItineraryItemFragment.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { cleanupConfirmPopup } from '../../helpers/confirmPopupTestSetup.mjs';
import { TransportationScheduleItemKey } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';

installDomTestHooks({
   after: () => {
      cleanupConfirmPopup();
   },
});


test('Test_ShowRemoveItineraryItemConfirmation_TestDefault_ExpectConfirmPopup', () => {
   RemoveItineraryItemFragment.showRemoveItineraryItemConfirmation({});

   const popup = document.querySelector('.tzg-confirm');
   const title = popup?.querySelector('.itin-top-title');
   const message = popup?.querySelector('.tzg-popup-message');
   const confirmButton = popup?.querySelector('.tzg-popup-confirm');

   assert.ok(popup);
   assert.equal(title?.textContent, Strings.itinerary.confirmation.removeItemTitle);
   assert.equal(message?.textContent, Strings.itinerary.confirmation.removeItemMessage);
   assert.equal(popup.querySelector('.tzg-popup-do-not-show-again'), null);
   assert.equal(confirmButton?.textContent, Strings.itinerary.dayPlanner.remove);
});


test('Test_ShowRemoveItineraryItemConfirmation_TestConfirm_ExpectConfirmed', () => {
   const confirmed = 'confirmed';
   const confirmCalls = [];
   RemoveItineraryItemFragment.showRemoveItineraryItemConfirmation({
      onConfirm: () => {
         confirmCalls.push(confirmed);
      },
   });
   const confirmButton = document.querySelector('.tzg-popup-confirm');

   confirmButton?.click();

   assert.deepEqual(confirmCalls, [confirmed]);
});


test('Test_ShowRemoveItineraryItemConfirmation_TestTransit_ExpectTransitMessage', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const key = new TransportationScheduleItemKey('Zoomobile', false).toWire();

   RemoveItineraryItemFragment.showRemoveItineraryItemConfirmation({
      itemType,
      key,
   });

   const message = document.querySelector('.tzg-popup-message');

   assert.equal(
      message?.textContent,
      Strings.itinerary.confirmation.removeTransitTransportationMessage
   );
});


test('Test_ShowRemoveItineraryItemConfirmation_TestAttractionTransport_ExpectDefaultMessage', () => {
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const key = new TransportationScheduleItemKey('Zoomobile', true).toWire();

   RemoveItineraryItemFragment.showRemoveItineraryItemConfirmation({
      itemType,
      key,
   });

   const message = document.querySelector('.tzg-popup-message');

   assert.equal(message?.textContent, Strings.itinerary.confirmation.removeItemMessage);
});
