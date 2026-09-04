import assert from 'node:assert/strict';
import test from 'node:test';

import { showScheduleItemModule } from '../../scripts/itinerary/panel/components/showScheduleItemModule.js';
import { ScheduleItemSearch } from '../../scripts/itinerary/panel/scheduleItemSearch.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

test.describe('showScheduleItemModule', () => {
   installDomTestHooks({
      after: () => {
         document.querySelector('.schedule-item-module')?.__tzgPopupCleanup?.();
         document.querySelector('.schedule-item-module')?.remove?.();
      },
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
      assert.equal(root?.querySelector('.schedule-item-select')?.disabled, false);
      assert.ok(root?.querySelector('.schedule-item-search-input'));
      assert.equal(root?.querySelector('.schedule-item-search-input')?.disabled, false);
      assert.ok(root?.querySelector('.schedule-item-only-itinerary-checkbox'));
      assert.equal(root?.querySelector('.schedule-item-only-itinerary-checkbox')?.disabled, false);
      assert.ok(root?.querySelector('.schedule-item-time-input'));
      assert.ok(root?.querySelector('.schedule-item-duration-input'));
      assert.ok(root?.querySelector('.schedule-item-results'));
      assert.equal(root?.querySelector('.itin-card')?.getAttribute('tabindex'), null);
      assert.equal(root?.querySelector('.itin-finish')?.textContent, strings.scheduleButton);
      assert.equal(
         root?.querySelector('.itin-prev')?.textContent,
         APP_STRINGS.itinerary.actions.cancel
      );
   });

   test('preselects unscheduled Zoomobile as an attraction', () => {
      showScheduleItemModule({
         eventTypes: ['lunch'],
         itinerary: {
            transportations: [{
               name: 'Zoomobile',
               added_as_attraction: true,
            }],
         },
         preselectedRow: ScheduleItemSearch.tagScheduleItemRow(ScheduleItemKind.TRANSPORTATION.itemType, {
            name: 'Zoomobile',
            added_as_attraction: true,
            route_duration_minutes: 75,
         }),
      });

      const root = document.querySelector('.schedule-item-module');
      const resultText = root?.querySelector('.schedule-item-results')?.textContent ?? '';

      assert.equal(
         root?.querySelector('.schedule-item-select')?.value,
         ScheduleItemKind.ATTRACTION.itemType
      );
      assert.equal(root?.querySelector('.schedule-item-search-input')?.value, 'Zoomobile');
      assert.equal(root?.querySelector('.schedule-item-select')?.disabled, true);
      assert.equal(root?.querySelector('.schedule-item-search-input')?.disabled, true);
      assert.equal(root?.querySelector('.schedule-item-only-itinerary-checkbox')?.disabled, true);
      assert.equal(root?.querySelector('.schedule-item-duration-input')?.disabled, true);
      assert.equal(root?.querySelector('.schedule-item-duration-input')?.value, '75');
      assert.equal(root?.querySelector('.schedule-item-time-input')?.disabled, false);
      assert.equal(root?.querySelector('.itin-card')?.getAttribute('tabindex'), '-1');
      assert.match(resultText, /Zoomobile/);
      assert.match(resultText, new RegExp(APP_STRINGS.search.extraCharge));
      assert.doesNotMatch(resultText, /round trip/);
      assert.equal(root?.querySelector('.itin-finish')?.disabled, false);
   });

   test('preselects transportation with station subtext', () => {
      showScheduleItemModule({
         eventTypes: ['lunch'],
         itinerary: {
            transportations: [{
               name: 'Zoomobile',
               added_as_attraction: false,
            }],
         },
         preselectedRow: ScheduleItemSearch.tagScheduleItemRow(ScheduleItemKind.TRANSPORTATION.itemType, {
            name: 'Zoomobile',
            added_as_attraction: false,
            route_duration_minutes: 75,
            legs: [
               {
                  from_station: 'Main Zoomobile Station',
                  to_station: 'Canadian Domain Zoomobile Station',
               },
               {
                  from_station: 'Canadian Domain Zoomobile Station',
                  to_station: 'Main Zoomobile Station',
               },
            ],
         }),
      });

      const root = document.querySelector('.schedule-item-module');
      const resultText = root?.querySelector('.schedule-item-results')?.textContent ?? '';

      assert.equal(
         root?.querySelector('.schedule-item-select')?.value,
         ScheduleItemKind.TRANSPORTATION.itemType
      );
      assert.equal(root?.querySelector('.schedule-item-search-input')?.value, 'Zoomobile');
      assert.equal(root?.querySelector('.schedule-item-select')?.disabled, true);
      assert.equal(root?.querySelector('.schedule-item-search-input')?.disabled, true);
      assert.equal(root?.querySelector('.schedule-item-only-itinerary-checkbox')?.disabled, true);
      assert.equal(root?.querySelector('.schedule-item-duration-input')?.disabled, true);
      assert.equal(root?.querySelector('.schedule-item-duration-input')?.value, '75');
      assert.match(resultText, /Zoomobile/);
      assert.match(resultText, /Main Zoomobile Station \(round trip\)/);
      assert.equal(root?.querySelector('.itin-finish')?.disabled, false);
   });
});
