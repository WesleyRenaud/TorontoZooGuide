import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryPanelScheduleHandler } from '../../../../scripts/itinerary/panel/itineraryPanelScheduleHandler.js';
import { ScheduleItemKeySeparator } from '../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { TransportationScheduleItemKey } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';

const eventType = 'lunch';
const itineraryConfig = {
   eventTypes: [eventType, 'break'],
   visitBoundaryEventTypes: {
      arrival: 'arrival',
      departure: 'departure',
   },
};
const species = 'Amur Tiger';
const exhibit = 'Eurasia Wilds';
const animalRow = {
   species,
   exhibit,
   scheduleItemKind: ScheduleItemKind.ANIMAL.kind,
};
const animalKey = [species, exhibit].join(ScheduleItemKeySeparator.VALUE);


test('Test_OpenScheduleItemModule_TestOptions_ExpectForwarded', () => {
   const calls = [];
   const visitDate = '2026-06-15';
   const itinerary = { date: visitDate };
   const eventTypes = [eventType];
   const onScheduled = () => {};

   ItineraryPanelScheduleHandler.openScheduleItemModule({
      itinerary,
      eventTypes,
      onScheduled,
      preselectedRow: animalRow,
   }, {
      showScheduleItemModule: (options) => {
         calls.push(options);
      },
   });
   const opened = calls.at(Position.FIRST);

   assert.equal(calls.length, Position.SECOND);
   assert.deepEqual(opened, {
      itinerary,
      eventTypes,
      preselectedRow: animalRow,
      onScheduled,
   });
});


test('Test_BuildItineraryPanelScheduleHandlers_TestScheduleItem_ExpectModuleOpened', () => {
   const opened = [];
   const eventTypes = [eventType];
   const handlers = ItineraryPanelScheduleHandler.buildItineraryPanelScheduleHandlers(
      { itineraryConfig },
      {
         onPanelRefresh: async () => {},
         deps: {
            openModule: (options) => {
               opened.push(options);
            },
            buildEventTypes: () => eventTypes,
         },
      }
   );

   handlers.onScheduleItineraryItem({ row: animalRow });
   const openedOptions = opened.at(Position.FIRST);

   assert.equal(opened.length, Position.SECOND);
   assert.deepEqual(openedOptions.eventTypes, eventTypes);
   assert.equal(openedOptions.preselectedRow, animalRow);
});


test('Test_BuildItineraryPanelScheduleHandlers_TestUnscheduleItem_ExpectRefreshed', async () => {
   const unscheduled = [];
   let refreshed = false;
   let notified = false;
   const payload = {
      itemType: ScheduleItemKind.ANIMAL.itemType,
      key: animalKey,
   };
   const handlers = ItineraryPanelScheduleHandler.buildItineraryPanelScheduleHandlers(
      {},
      {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps: {
            unscheduleItem: async (request) => {
               unscheduled.push(request);
               return { errorType: ItineraryErrorType.SUCCESS };
            },
            notifyUpdated: async () => {
               notified = true;
               return true;
            },
         },
      }
   );

   await handlers.onUnscheduleItineraryItem(payload);

   assert.deepEqual(unscheduled, [payload]);
   assert.equal(notified, true);
   assert.equal(refreshed, true);
});


test('Test_BuildItineraryPanelScheduleHandlers_TestRemoveEventType_ExpectConfirmedThenRemoved', async () => {
   const removed = [];
   const confirmations = [];
   let refreshed = false;
   let notified = false;
   const payload = {
      itemType: eventType,
      key: '',
   };
   const handlers = ItineraryPanelScheduleHandler.buildItineraryPanelScheduleHandlers(
      { itineraryConfig },
      {
         onPanelRefresh: async () => {
            refreshed = true;
         },
         deps: {
            removeItem: async (request) => {
               removed.push(request);
               return { errorType: ItineraryErrorType.SUCCESS };
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

   handlers.onRemoveItineraryItem(payload);
   const onConfirm = confirmations.at(Position.FIRST);

   assert.equal(removed.length, 0);
   assert.equal(confirmations.length, Position.SECOND);

   await onConfirm();

   assert.deepEqual(removed, [payload]);
   assert.equal(notified, true);
   assert.equal(refreshed, true);
});


test('Test_BuildItineraryPanelScheduleHandlers_TestRemoveTransportation_ExpectIdentityPassedToConfirmation', () => {
   const confirmations = [];
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;
   const key = new TransportationScheduleItemKey('Zoomobile', false).toWire();
   const handlers = ItineraryPanelScheduleHandler.buildItineraryPanelScheduleHandlers(
      { itineraryConfig },
      {
         deps: {
            removeItem: async () => ({ errorType: ItineraryErrorType.SUCCESS }),
            removeAnimalDraft: () => {},
            requiresRemoveConfirmation: () => true,
            showRemoveConfirmation: (options) => {
               confirmations.push(options);
            },
            notifyUpdated: async () => true,
         },
      }
   );

   handlers.onRemoveItineraryItem({ itemType, key });
   const confirmation = confirmations.at(Position.FIRST);

   assert.equal(confirmations.length, Position.SECOND);
   assert.equal(confirmation.itemType, itemType);
   assert.equal(confirmation.key, key);
});


test('Test_BuildItineraryPanelScheduleHandlers_TestRemoveAnimalWithoutConfirmation_ExpectRemoved', async () => {
   const removed = [];
   let notified = false;
   const payload = {
      itemType: ScheduleItemKind.ANIMAL.itemType,
      key: animalKey,
   };
   const handlers = ItineraryPanelScheduleHandler.buildItineraryPanelScheduleHandlers(
      { itineraryConfig },
      {
         deps: {
            removeItem: async (request) => {
               removed.push(request);
               return { errorType: ItineraryErrorType.SUCCESS };
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

   handlers.onRemoveItineraryItem(payload);
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.deepEqual(removed, [payload]);
   assert.equal(notified, true);
});
