import assert from 'node:assert/strict';
import test from 'node:test';

import { showScheduleItemModule } from '../../scripts/itinerary/panel/components/showScheduleItemModule.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

test.describe('showScheduleItemModule', () => {
   test.beforeEach(() => {
      installTestWindow();
      installDocument();
   });

   test.afterEach(() => {
      document.querySelector('.schedule-item-module')?.__tzgPopupCleanup?.();
      document.querySelector('.schedule-item-module')?.remove?.();
      teardownDocument();
      delete globalThis.window;
   });

   test('mounts the schedule popup with form fields', () => {
      const popup = showScheduleItemModule({
         eventTypes: ['lunch', 'break'],
      });

      const root = document.querySelector('.schedule-item-module');
      const strings = APP_STRINGS.itinerary.scheduleItem;

      assert.ok(popup);
      assert.ok(root);
      assert.equal(root?.querySelector('.itin-top-title')?.textContent, strings.title);
      assert.ok(root?.querySelector('.schedule-item-select'));
      assert.ok(root?.querySelector('.schedule-item-search-input'));
      assert.ok(root?.querySelector('.schedule-item-only-itinerary-checkbox'));
      assert.ok(root?.querySelector('.schedule-item-time-input'));
      assert.ok(root?.querySelector('.schedule-item-duration-input'));
      assert.ok(root?.querySelector('.schedule-item-results'));
      assert.equal(root?.querySelector('.itin-finish')?.textContent, strings.scheduleButton);
      assert.equal(
         root?.querySelector('.itin-prev')?.textContent,
         APP_STRINGS.itinerary.actions.cancel
      );
   });
});
