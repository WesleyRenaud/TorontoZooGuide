import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ActionsBar } from '../../../../../scripts/itinerary/panel/components/actionsBar.js';
import { APP_STRINGS } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

test.describe('makeActionsBar', () => {
   installDomTestHooks({
      after: () => {
         document.querySelector('.tzg-confirm')?.__tzgPopupCleanup?.();
         document.querySelector('.tzg-confirm')?.remove();
      },
   });

   test('Test_Dispatches_TestDispatchesEditItineraryWhenTheEditButtonIs_ExpectOk', () => {
      const dispatched = [];

      globalThis.window.dispatchEvent = (event) => {
         dispatched.push(event.type);
         return true;
      };

      const actionsBar = ActionsBar.makeActionsBar();
      const editButton = actionsBar.querySelector('.itin-panel-edit-btn');

      editButton?.click();

      assert.deepEqual(dispatched, ['tzg:editItinerary']);
      assert.equal(
         editButton?.textContent,
         APP_STRINGS.itinerary.actions.editItinerary
      );
   });

   test('Test_Shows_TestShowsAClearConfirmationPopupAndRunsOnAfterClear_ExpectOk', async () => {
      const cleared = [];
      const actionsBar = ActionsBar.makeActionsBar({
         onAfterClear: async () => {
            cleared.push('cleared');
         },
      });

      actionsBar.querySelector('.itin-panel-clear-btn')?.click();

      const popup = document.querySelector('.tzg-confirm');
      const title = popup?.querySelector('.itin-top-title');
      const confirmButton = popup?.querySelector('.tzg-popup-confirm');

      assert.ok(popup);
      assert.equal(
         title?.textContent,
         APP_STRINGS.itinerary.confirmation.clearTitle
      );
      assert.equal(
         confirmButton?.textContent,
         APP_STRINGS.itinerary.actions.clear
      );

      confirmButton?.click();

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      assert.deepEqual(cleared, ['cleared']);
   });
});
