import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { showScheduleItemNotice } from '../../scripts/itinerary/panel/showScheduleItemNotice.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

test.describe('showScheduleItemNotice', () => {
   beforeEach(() => {
      installTestWindow();
      installDocument();
   });

   afterEach(() => {
      document.querySelector('.tzg-notice')?.__tzgPopupCleanup?.();
      document.querySelector('.tzg-notice')?.remove();
      teardownDocument();
      delete globalThis.window;
   });

   test('shows a notice popup on the itinerary panel mount element', () => {
      showScheduleItemNotice('Could not schedule item.');

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

   test('falls back to document.body when no itinerary panel mount exists', () => {
      const noticeCalls = [];

      showScheduleItemNotice('Missing mount.', {
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
