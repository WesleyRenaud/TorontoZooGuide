import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ShowScheduleItemNotice } from '../../../../scripts/itinerary/panel/showScheduleItemNotice.js';
import { APP_STRINGS } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

test.describe('showScheduleItemNotice', () => {
   installDomTestHooks({
      after: () => {
         document.querySelector('.tzg-notice')?.__tzgPopupCleanup?.();
         document.querySelector('.tzg-notice')?.remove();
      },
   });

   test('Test_ShowScheduleItemNotice_TestPanelMount_ExpectNoticePopup', () => {
      ShowScheduleItemNotice.showScheduleItemNotice('Could not schedule item.');

      const popup = document.querySelector('.tzg-notice');
      const title = popup?.querySelector('.itin-top-title');
      const message = popup?.querySelector('.tzg-popup-message');
      const button = popup?.querySelector('.tzg-popup-confirm');

      assert.ok(popup);
      assert.equal(
         title?.textContent,
         APP_STRINGS.itinerary.scheduleItem.errorTitle
      );
      assert.equal(message?.textContent, 'Could not schedule item.');
      assert.equal(
         button?.textContent,
         APP_STRINGS.itinerary.noItemsSelected.button
      );
   });

   test('Test_ShowScheduleItemNotice_TestNoMount_ExpectDocumentBody', () => {
      const noticeCalls = [];

      ShowScheduleItemNotice.showScheduleItemNotice('Missing mount.', {
         getMountEl: () => null,
         showNoticePopup: (config) => {
            noticeCalls.push(config);
         },
      });

      assert.equal(noticeCalls.length, 1);
      assert.equal(noticeCalls[0].mountEl, document.body);
      assert.equal(noticeCalls[0].message, 'Missing mount.');
   });
});
