import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryPanelScheduleHandlers } from '../../../../scripts/itinerary/panel/itineraryPanelScheduleHandlers.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';

const ITINERARY_CONFIG = {
   eventTypes: ['lunch', 'break'],
   visitBoundaryEventTypes: {
      arrival: 'arrival',
      departure: 'departure',
   },
};

const ANIMAL_ROW = {
   species: 'Tiger',
   exhibit: 'Savanna',
   scheduleItemKind: 'animals',
};

test('Test_ItineraryPanelScheduleHandlers_TestItineraryPanelScheduleHandlersOpenScheduleItemModuleForwardsOptionsToTheScheduleModule_ExpectOk', () => {
   const calls = [];

   ItineraryPanelScheduleHandlers.openScheduleItemModule({
      itinerary: { date: '2026-06-15' },
      eventTypes: ['lunch'],
      onScheduled: () => {},
      preselectedRow: ANIMAL_ROW,
   }, {
      showScheduleItemModule: (options) => {
         calls.push(options);
      },
   });

   assert.equal(calls.length, 1);
   assert.deepEqual(calls[0], {
      itinerary: { date: '2026-06-15' },
      eventTypes: ['lunch'],
      preselectedRow: ANIMAL_ROW,
      onScheduled: calls[0].onScheduled,
   });
});

test('Test_ItineraryPanelScheduleHandlers_TestItineraryPanelScheduleHandlersBuildItineraryPanelScheduleHandlersOpensTheModuleForAPicked_ExpectOk', () => {
   const opened = [];
   const handlers = ItineraryPanelScheduleHandlers.buildItineraryPanelScheduleHandlers(
      { itineraryConfig: ITINERARY_CONFIG },
      {
         onPanelRefresh: async () => {},
         deps: {
            openModule: (options) => {
               opened.push(options);
            },
            buildEventTypes: () => ['lunch'],
         },
      }
   );

   handlers.onScheduleItineraryItem({ row: ANIMAL_ROW });

   assert.equal(opened.length, 1);
   assert.deepEqual(opened[0].eventTypes, ['lunch']);
   assert.equal(opened[0].preselectedRow, ANIMAL_ROW);
});

test('Test_ItineraryPanelScheduleHandlers_TestItineraryPanelScheduleHandlersBuildItineraryPanelScheduleHandlersUnschedulesItemsAndRefreshesThePanel_ExpectOk', async () => {
   const unscheduled = [];
   let refreshed = false;
   let notified = false;
   const handlers = ItineraryPanelScheduleHandlers.buildItineraryPanelScheduleHandlers(
      {},
      {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps: {
            unscheduleItem: async (payload) => {
               unscheduled.push(payload);
               return { errorType: 'success' };
            },
            notifyUpdated: async () => {
               notified = true;
               return true;
            },
         },
      }
   );

   await handlers.onUnscheduleItineraryItem({
      itemType: ScheduleItemKind.ANIMAL.itemType,
      key: 'Tiger||Savanna',
   });

   assert.deepEqual(unscheduled, [{
      itemType: ScheduleItemKind.ANIMAL.itemType,
      key: 'Tiger||Savanna',
   }]);
   assert.equal(notified, true);
   assert.equal(refreshed, true);
});

test('Test_ItineraryPanelScheduleHandlers_TestItineraryPanelScheduleHandlersBuildItineraryPanelScheduleHandlersConfirmsBeforeRemovingConfiguredEventTypes_ExpectOk', async () => {
   const removed = [];
   const confirmations = [];
   let refreshed = false;
   let notified = false;
   const handlers = ItineraryPanelScheduleHandlers.buildItineraryPanelScheduleHandlers(
      { itineraryConfig: ITINERARY_CONFIG },
      {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps: {
            removeItem: async (payload) => {
               removed.push(payload);
               return { errorType: 'success' };
            },
            removeAnimalDraft: () => {},
            requiresRemoveConfirmation: () => true,
            showRemoveConfirmation: ({ onConfirm }) => {
               confirmations.push(onConfirm);
            },
            notifyUpdated: async () => {
               notified = true;
               return true;
            },
         },
      }
   );

   handlers.onRemoveItineraryItem({
      itemType: 'lunch',
      key: '',
   });

   assert.equal(removed.length, 0);
   assert.equal(confirmations.length, 1);

   await confirmations[0]();

   assert.deepEqual(removed, [{ itemType: 'lunch', key: '' }]);
   assert.equal(notified, true);
   assert.equal(refreshed, true);
});

test('Test_ItineraryPanelScheduleHandlers_TestItineraryPanelScheduleHandlersBuildItineraryPanelScheduleHandlersPassesItemIdentityIntoRemoveConfirmation_ExpectOk', async () => {
   const confirmations = [];
   const handlers = ItineraryPanelScheduleHandlers.buildItineraryPanelScheduleHandlers(
      { itineraryConfig: ITINERARY_CONFIG },
      {
         deps: {
            removeItem: async () => ({ errorType: 'success' }),
            removeAnimalDraft: () => {},
            requiresRemoveConfirmation: () => true,
            showRemoveConfirmation: (options) => {
               confirmations.push(options);
            },
            notifyUpdated: async () => true,
         },
      }
   );

   handlers.onRemoveItineraryItem({
      itemType: ScheduleItemKind.TRANSPORTATION.itemType,
      key: 'Zoomobile||0',
   });

   assert.equal(confirmations.length, 1);
   assert.equal(
      confirmations[0].itemType,
      ScheduleItemKind.TRANSPORTATION.itemType
   );
   assert.equal(confirmations[0].key, 'Zoomobile||0');
});

test('Test_ItineraryPanelScheduleHandlers_TestItineraryPanelScheduleHandlersBuildItineraryPanelScheduleHandlersRemovesAnimalsWithoutConfirmation_ExpectOk', async () => {
   const removed = [];
   let notified = false;
   const handlers = ItineraryPanelScheduleHandlers.buildItineraryPanelScheduleHandlers(
      { itineraryConfig: ITINERARY_CONFIG },
      {
         deps: {
            removeItem: async (payload) => {
               removed.push(payload);
               return { errorType: 'success' };
            },
            removeAnimalDraft: () => {},
            requiresRemoveConfirmation: () => false,
            notifyUpdated: async () => {
               notified = true;
               return true;
            },
         },
      }
   );

   handlers.onRemoveItineraryItem({
      itemType: ScheduleItemKind.ANIMAL.itemType,
      key: 'Tiger||Savanna',
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.deepEqual(removed, [{
      itemType: ScheduleItemKind.ANIMAL.itemType,
      key: 'Tiger||Savanna',
   }]);
   assert.equal(notified, true);
});
