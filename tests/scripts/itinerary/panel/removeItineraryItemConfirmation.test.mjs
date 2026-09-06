import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RemoveItineraryItemConfirmation } from '../../../../scripts/itinerary/panel/removeItineraryItemConfirmation.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { cleanupConfirmPopup } from '../../helpers/confirmPopupTestSetup.mjs';

test.describe('removeItineraryItemConfirmation', () => {
   installDomTestHooks({
      after: () => {
         cleanupConfirmPopup();
      },
   });

   test('Test_ShowRemoveItineraryItemConfirmation_TestDefault_ExpectConfirmPopup', () => {
      const confirmCalls = [];

      RemoveItineraryItemConfirmation.showRemoveItineraryItemConfirmation({
         onConfirm: () => {
            confirmCalls.push('confirmed');
         },
      });

      const popup = document.querySelector('.tzg-confirm');
      const strings = Strings.itinerary.confirmation;
      const title = popup?.querySelector('.itin-top-title');
      const message = popup?.querySelector('.tzg-popup-message');
      const confirmButton = popup?.querySelector('.tzg-popup-confirm');

      assert.ok(popup);
      assert.equal(title?.textContent, strings.removeItemTitle);
      assert.equal(message?.textContent, strings.removeItemMessage);
      assert.equal(popup.querySelector('.tzg-popup-do-not-show-again'), null);
      assert.equal(confirmButton?.textContent, Strings.itinerary.dayPlanner.remove);

      confirmButton?.click();

      assert.deepEqual(confirmCalls, ['confirmed']);
   });

   test('Test_ShowRemoveItineraryItemConfirmation_TestTransit_ExpectTransitMessage', () => {
      const strings = Strings.itinerary.confirmation;

      RemoveItineraryItemConfirmation.showRemoveItineraryItemConfirmation({
         itemType: ScheduleItemKind.TRANSPORTATION.itemType,
         key: 'Zoomobile||0',
      });

      const message = document.querySelector('.tzg-popup-message');

      assert.equal(
         message?.textContent,
         strings.removeTransitTransportationMessage
      );
   });

   test('Test_ShowRemoveItineraryItemConfirmation_TestAttractionTransport_ExpectDefaultMessage', () => {
      const strings = Strings.itinerary.confirmation;

      RemoveItineraryItemConfirmation.showRemoveItineraryItemConfirmation({
         itemType: ScheduleItemKind.TRANSPORTATION.itemType,
         key: 'Zoomobile||1',
      });

      const message = document.querySelector('.tzg-popup-message');

      assert.equal(message?.textContent, strings.removeItemMessage);
   });
});
