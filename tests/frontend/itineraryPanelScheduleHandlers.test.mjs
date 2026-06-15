import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildItineraryPanelScheduleHandlers,
   openScheduleItemModule,
} from '../../scripts/itinerary/panel/itineraryPanelScheduleHandlers.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';

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

test('openScheduleItemModule forwards options to the schedule module popup', () => {
   const calls = [];

   openScheduleItemModule({
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

test('buildItineraryPanelScheduleHandlers opens the module for a picked row', () => {
   const opened = [];
   const handlers = buildItineraryPanelScheduleHandlers(
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

test('buildItineraryPanelScheduleHandlers unschedules items and refreshes the panel', async () => {
   const unscheduled = [];
   let refreshed = false;
   const handlers = buildItineraryPanelScheduleHandlers(
      {},
      {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps: {
            unscheduleItem: async (payload) => {
               unscheduled.push(payload);
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
   assert.equal(refreshed, true);
});

test('buildItineraryPanelScheduleHandlers confirms before removing configured event types', async () => {
   const removed = [];
   const confirmations = [];
   let refreshed = false;
   const handlers = buildItineraryPanelScheduleHandlers(
      { itineraryConfig: ITINERARY_CONFIG },
      {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps: {
            removeItem: async (payload) => {
               removed.push(payload);
            },
            removeAnimalDraft: () => {},
            requiresRemoveConfirmation: () => true,
            showRemoveConfirmation: ({ onConfirm }) => {
               confirmations.push(onConfirm);
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
   assert.equal(refreshed, true);
});

test('buildItineraryPanelScheduleHandlers removes animals without confirmation', async () => {
   const removed = [];
   const handlers = buildItineraryPanelScheduleHandlers(
      { itineraryConfig: ITINERARY_CONFIG },
      {
         deps: {
            removeItem: async (payload) => {
               removed.push(payload);
            },
            removeAnimalDraft: () => {},
            requiresRemoveConfirmation: () => false,
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
});
