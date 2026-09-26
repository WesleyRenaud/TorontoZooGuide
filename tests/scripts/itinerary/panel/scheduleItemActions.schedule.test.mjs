import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemController } from '../../../../scripts/itinerary/panel/scheduleItemController.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { mockJsonResponse, mockScheduleItemFetch, installScheduleItemActionsTestHooks } from '../../helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();

const visitDate = '2026-06-15';
const species = 'Amur Tiger';
const exhibit = 'Eurasia Wilds';
const animalRow = {
   species,
   exhibit,
   scheduleItemKind: ScheduleItemKind.ANIMAL.kind,
};
const animalItinerary = {
   date: visitDate,
   animals: [{ species, exhibit }],
   attractions: [],
};
const emptyItinerary = {
   date: visitDate,
   animals: [],
   attractions: [],
};


test('Test_ScheduleSelectedItineraryItem_TestAnimalSuccess_ExpectItineraryUpdated', async () => {
   const events = [];
   const itinerary = {
      date: visitDate,
      animals: [{ species, exhibit, start_time: '10:00' }],
      attractions: [],
      guardians_talks: [],
      wild_encounters: [],
   };
   globalThis.window.dispatchEvent = (event) => {
      if (event.type === 'tzg:itineraryUpdated') {
         events.push(event.detail?.itinerary ?? null);
      }

      return true;
   };
   globalThis.fetch = mockScheduleItemFetch({
      routes: {
         '/schedule-itinerary-item': {
            status: ItineraryErrorType.SUCCESS,
            reasons: [],
            itinerary,
         },
      },
   });

   const result = await ScheduleItemController.scheduleSelectedItineraryItem(
      emptyItinerary,
      ScheduleItemKind.ANIMAL.itemType,
      animalRow,
      []
   );
   const updated = events.at(Position.FIRST);

   assert.equal(result.errorType, ItineraryErrorType.SUCCESS);
   assert.equal(events.length, Position.SECOND);
   assert.equal(updated?.date, visitDate);
   assert.equal(updated?.animals?.length, Position.SECOND);
   assert.equal(updated?.animals?.at(Position.FIRST)?.species, species);
});


test('Test_ScheduleSelectedItineraryItem_TestEventType_ExpectRequestPayload', async () => {
   const requests = [];
   const itemType = 'lunch';
   const startTime = '1:30 PM';
   const durationMinutes = 15;
   globalThis.fetch = async (url, options = {}) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      return mockScheduleItemFetch()(url, options);
   };

   const result = await ScheduleItemController.scheduleSelectedItineraryItem(
      emptyItinerary,
      itemType,
      null,
      [itemType],
      { startTime, durationMinutes }
   );
   const scheduleRequests = requests.filter((request) => request.url === '/schedule-itinerary-item');

   assert.equal(result.errorType, ItineraryErrorType.SUCCESS);
   assert.deepEqual(scheduleRequests, [{
      url: '/schedule-itinerary-item',
      body: {
         itemType,
         key: '',
         startTime,
         durationMinutes,
         confirmingScheduleItemNotOnItinerary: false,
         confirmingAttractionOutsideOperatingHours: false,
         confirmingGuardiansTalkUnschedule: false,
         confirmingWildEncounterUnschedule: false,
         confirmingFixedTimeItemLongWait: false,
         confirmingGuardiansTalkWithoutAnimal: false,
      },
   }]);
});


test('Test_ScheduleSelectedItineraryItem_TestUnsetTypeWithAnimalRow_ExpectScheduled', async () => {
   const urls = [];
   globalThis.fetch = async (url, options = {}) => {
      urls.push(url);

      return mockScheduleItemFetch()(url, options);
   };

   const result = await ScheduleItemController.scheduleSelectedItineraryItem(
      animalItinerary,
      '',
      animalRow,
      []
   );

   assert.equal(result.errorType, ItineraryErrorType.SUCCESS);
   assert.deepEqual(urls, ['/get-itinerary-date', '/schedule-itinerary-item']);
});


test('Test_ScheduleSelectedItineraryItem_TestNoAvailableSlot_ExpectErrorWithoutRefresh', async () => {
   const errorType = ItineraryErrorType.NO_AVAILABLE_SLOT;
   globalThis.fetch = mockScheduleItemFetch({
      routes: {
         '/schedule-itinerary-item': {
            status: errorType,
            reasons: [],
         },
      },
   });

   const result = await ScheduleItemController.scheduleSelectedItineraryItem(
      animalItinerary,
      ScheduleItemKind.ANIMAL.itemType,
      animalRow,
      []
   );

   assert.equal(result.errorType, errorType);
});


test('Test_ScheduleSelectedItineraryItem_TestRequestedTimeNotAvailable_ExpectError', async () => {
   const errorType = ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE;
   const startTime = '12:00 PM';
   globalThis.fetch = mockScheduleItemFetch({
      routes: {
         '/schedule-itinerary-item': {
            status: errorType,
            reasons: [],
         },
      },
   });

   const result = await ScheduleItemController.scheduleSelectedItineraryItem(
      emptyItinerary,
      ScheduleItemKind.ANIMAL.itemType,
      animalRow,
      [],
      { startTime }
   );

   assert.equal(result.errorType, errorType);
});


test('Test_ScheduleSelectedItineraryItem_TestMissingVisitDate_ExpectDateSavedThenScheduled', async () => {
   const requests = [];
   globalThis.fetch = async (url, options = {}) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: null });
      }

      if (url === '/get-zoo-hours') {
         return mockJsonResponse({
            hours: {
               openTime: '09:30',
               closeTime: '19:00',
            },
         });
      }

      if (url === '/set-itinerary') {
         return mockJsonResponse({
            status: ItineraryErrorType.SUCCESS,
            reasons: [],
            itinerary: {
               date: JSON.parse(options.body).date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            itinerary_config: {
               itinerary_error_types: { SUCCESS: ItineraryErrorType.SUCCESS },
            },
         });
      }

      if (url === '/schedule-itinerary-item') {
         return mockJsonResponse({ status: ItineraryErrorType.SUCCESS, reasons: [] });
      }

      throw new Error(`Unexpected fetch: ${url}`);
   };

   const result = await ScheduleItemController.scheduleSelectedItineraryItem(
      { animals: [], attractions: [] },
      ScheduleItemKind.ANIMAL.itemType,
      animalRow,
      []
   );
   const setItinerary = requests.find((request) => request.url === '/set-itinerary');
   const lastRequest = requests.at(Position.LAST);

   assert.equal(result.errorType, ItineraryErrorType.SUCCESS);
   assert.equal(requests.some((request) => request.url === '/get-zoo-hours'), true);
   assert.equal(requests.some((request) => request.url === '/set-itinerary'), true);
   assert.ok(setItinerary?.body?.date);
   assert.equal(lastRequest?.url, '/schedule-itinerary-item');
});
