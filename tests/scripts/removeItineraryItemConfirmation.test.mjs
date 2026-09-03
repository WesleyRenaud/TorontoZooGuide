import assert from 'node:assert/strict';
import { test } from 'node:test';

import { showRemoveItineraryItemConfirmation } from '../../scripts/itinerary/panel/removeItineraryItemConfirmation.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';
import { cleanupConfirmPopup } from './helpers/confirmPopupTestSetup.mjs';

test.describe('removeItineraryItemConfirmation', () => {
   installDomTestHooks({
      after: () => {
         cleanupConfirmPopup();
      },
   });

   test('showRemoveItineraryItemConfirmation uses confirm popup without do-not-show-again', () => {
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
   });

   test('showRemoveItineraryItemConfirmation uses transit message for transit transportation', () => {
      const strings = APP_STRINGS.itinerary.confirmation;

      showRemoveItineraryItemConfirmation({
         itemType: ScheduleItemKind.TRANSPORTATION.itemType,
         key: 'Zoomobile||0',
      });

      const message = document.querySelector('.tzg-popup-message');

      assert.equal(
         message?.textContent,
         strings.removeTransitTransportationMessage
      );
   });

   test('showRemoveItineraryItemConfirmation keeps default message for attraction transportation', () => {
      const strings = APP_STRINGS.itinerary.confirmation;

      showRemoveItineraryItemConfirmation({
         itemType: ScheduleItemKind.TRANSPORTATION.itemType,
         key: 'Zoomobile||1',
      });

      const message = document.querySelector('.tzg-popup-message');

      assert.equal(message?.textContent, strings.removeItemMessage);
   });
});
