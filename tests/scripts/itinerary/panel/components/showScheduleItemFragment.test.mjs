import assert from 'node:assert/strict';
import test from 'node:test';

import { ShowScheduleItemFragment } from '../../../../../scripts/itinerary/panel/components/showScheduleItemFragment.js';
import { ShowScheduleItemModuleHelper } from '../../../../../scripts/itinerary/panel/components/showScheduleItemModuleHelper.js';
import { ScheduleItemSearcher } from '../../../../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks({
   after: () => {
      document.querySelector('.schedule-item-module')?.__tzgPopupCleanup?.();
      document.querySelector('.schedule-item-module')?.remove?.();
   },
});


test('Test_ShowScheduleItemModule_TestFormFields_ExpectMounted', () => {
   const popup = ShowScheduleItemFragment.showScheduleItemModule({
      eventTypes: ['lunch', 'break'],
   });
   const root = document.querySelector('.schedule-item-module');

   assert.ok(popup);
   assert.ok(root);
   assert.equal(root?.querySelector('.itin-top-title')?.textContent, Strings.itinerary.scheduleItem.title);
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
   assert.equal(
      root?.querySelector('.itin-finish')?.textContent,
      Strings.itinerary.scheduleItem.scheduleButton
   );
   assert.equal(
      root?.querySelector('.itin-prev')?.textContent,
      Strings.itinerary.actions.cancel
   );
});


test('Test_ShowScheduleItemModule_TestUnscheduledZoomobileAttraction_ExpectPreselected', () => {
   const rideName = 'Zoomobile';
   const durationMinutes = 75;

   ShowScheduleItemFragment.showScheduleItemModule({
      eventTypes: ['lunch'],
      itinerary: {
         transportations: [{
            name: rideName,
            added_as_attraction: true,
         }],
      },
      preselectedRow: ScheduleItemSearcher.tagScheduleItemRow(ScheduleItemKind.TRANSPORTATION.itemType, {
         name: rideName,
         added_as_attraction: true,
         route_duration_minutes: durationMinutes,
      }),
   });
   const root = document.querySelector('.schedule-item-module');
   const resultText = root.querySelector('.schedule-item-results').textContent;

   assert.equal(
      root?.querySelector('.schedule-item-select')?.value,
      ScheduleItemKind.ATTRACTION.itemType
   );
   assert.equal(root?.querySelector('.schedule-item-search-input')?.value, rideName);
   assert.equal(root?.querySelector('.schedule-item-select')?.disabled, true);
   assert.equal(root?.querySelector('.schedule-item-search-input')?.disabled, true);
   assert.equal(root?.querySelector('.schedule-item-only-itinerary-checkbox')?.disabled, true);
   assert.equal(root?.querySelector('.schedule-item-duration-input')?.disabled, true);
   assert.equal(
      root?.querySelector('.schedule-item-duration-input')?.value,
      String(durationMinutes)
   );
   assert.equal(root?.querySelector('.schedule-item-time-input')?.disabled, false);
   assert.equal(root?.querySelector('.itin-card')?.getAttribute('tabindex'), '-1');
   assert.match(resultText, new RegExp(rideName));
   assert.match(resultText, new RegExp(Strings.search.extraCharge));
   assert.doesNotMatch(resultText, /round trip/);
   assert.equal(root?.querySelector('.itin-finish')?.disabled, false);
});


test('Test_ShowScheduleItemModule_TestTransportationStations_ExpectPreselected', () => {
   const rideName = 'Zoomobile';
   const durationMinutes = 75;
   const mainStation = 'Main Zoomobile Station';
   const domainStation = 'Canadian Domain Zoomobile Station';

   ShowScheduleItemFragment.showScheduleItemModule({
      eventTypes: ['lunch'],
      itinerary: {
         transportations: [{
            name: rideName,
            added_as_attraction: false,
         }],
      },
      preselectedRow: ScheduleItemSearcher.tagScheduleItemRow(ScheduleItemKind.TRANSPORTATION.itemType, {
         name: rideName,
         added_as_attraction: false,
         route_duration_minutes: durationMinutes,
         legs: [
            {
               from_station: mainStation,
               to_station: domainStation,
            },
            {
               from_station: domainStation,
               to_station: mainStation,
            },
         ],
      }),
   });
   const root = document.querySelector('.schedule-item-module');
   const resultText = root.querySelector('.schedule-item-results').textContent;

   assert.equal(
      root?.querySelector('.schedule-item-select')?.value,
      ScheduleItemKind.TRANSPORTATION.itemType
   );
   assert.equal(root?.querySelector('.schedule-item-search-input')?.value, rideName);
   assert.equal(root?.querySelector('.schedule-item-select')?.disabled, true);
   assert.equal(root?.querySelector('.schedule-item-search-input')?.disabled, true);
   assert.equal(root?.querySelector('.schedule-item-only-itinerary-checkbox')?.disabled, true);
   assert.equal(root?.querySelector('.schedule-item-duration-input')?.disabled, true);
   assert.equal(
      root?.querySelector('.schedule-item-duration-input')?.value,
      String(durationMinutes)
   );
   assert.match(resultText, new RegExp(rideName));
   assert.match(resultText, new RegExp(`${mainStation} \\(round trip\\)`));
   assert.equal(root?.querySelector('.itin-finish')?.disabled, false);
});


test('Test_ShowScheduleItemModule_TestCancel_ExpectClosed', () => {
   const originalDebounce = ShowScheduleItemModuleHelper.debounce;
   let capturedSearchFn = null;

   ShowScheduleItemModuleHelper.debounce = (fn) => {
      capturedSearchFn = fn;
      return () => {
         fn();
      };
   };

   try {
      ShowScheduleItemFragment.showScheduleItemModule({ eventTypes: ['lunch'] });
      const root = document.querySelector('.schedule-item-module');
      capturedSearchFn();
      root.querySelector('.itin-prev')?.listeners?.click?.();

      assert.ok(root);
      assert.equal(typeof capturedSearchFn, 'function');
      assert.equal(document.querySelector('.schedule-item-module'), null);
   } finally {
      ShowScheduleItemModuleHelper.debounce = originalDebounce;
   }
});


test('Test_ShowScheduleItemModule_TestClose_ExpectClosed', () => {
   const originalDebounce = ShowScheduleItemModuleHelper.debounce;
   let capturedSearchFn = null;

   ShowScheduleItemModuleHelper.debounce = (fn) => {
      capturedSearchFn = fn;
      return () => fn();
   };

   try {
      ShowScheduleItemFragment.showScheduleItemModule({ eventTypes: ['lunch'] });
      const root = document.querySelector('.schedule-item-module');
      const closeButton = root?.querySelector('.itin-close')
         || [...(root?.querySelectorAll('button') || [])].find((button) => (
            String(button.className || '').includes('close')
            || button.getAttribute?.('aria-label')?.toLowerCase?.().includes('close')
         ));
      closeButton?.listeners?.click?.();

      assert.equal(typeof capturedSearchFn, 'function');
      assert.equal(document.querySelector('.schedule-item-module'), null);
   } finally {
      ShowScheduleItemModuleHelper.debounce = originalDebounce;
   }
});
