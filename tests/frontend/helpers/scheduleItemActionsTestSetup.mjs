import { updateItineraryErrorTypesFromConfig } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { installDomTestHooks } from './domTestSetup.mjs';
import { mockJsonResponse } from './fetchMock.mjs';
import { createLocalStorageMock } from './localStorageMock.mjs';

export const MOCK_ERROR_TYPES = Object.freeze({
   SUCCESS: 'success',
   SAVE_FAILED: 'saveFailed',
   ACTIVITY_NOT_ON_DAY_SCHEDULE: 'activityNotOnDaySchedule',
   SCHEDULE_WINDOW_UNAVAILABLE: 'scheduleWindowUnavailable',
   NO_AVAILABLE_SLOT: 'noAvailableSlot',
   REQUESTED_TIME_NOT_AVAILABLE: 'requestedTimeNotAvailable',
   ITEM_NOT_ON_ITINERARY: 'itemNotOnItinerary',
   ITEM_ALREADY_SCHEDULED: 'itemAlreadyScheduled',
   GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: 'guardiansTalkWillUnscheduleItems',
   FIXED_TIME_ITEM_LONG_WAIT: 'fixedTimeItemLongWait',
   GUARDIANS_TALK_WITHOUT_ANIMAL: 'guardiansTalkWithoutAnimal',
   ATTRACTION_WITHOUT_ANIMAL: 'attractionWithoutAnimal',
   WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS: 'wildEncounterWillUnscheduleItems',
   BULK_SCHEDULE_ANIMALS_ALREADY_SCHEDULED: 'bulkScheduleAnimalsAlreadyScheduled',
   UNSCHEDULE_ALL_NOTHING_SCHEDULED: 'unscheduleAllNothingScheduled',
});

export { mockJsonResponse };

export function mockScheduleItemFetch({
   serverDate = '2026-06-15',
   routes = {},
} = {}) {
   return async (url, options = {}) => {
      if (url === '/get-itinerary-date') {
         return mockJsonResponse({ date: serverDate });
      }

      const handler = routes[url];

      if (typeof handler === 'function') {
         return mockJsonResponse(await handler(url, options));
      }

      if (handler !== undefined) {
         return mockJsonResponse(handler);
      }

      return mockJsonResponse({ status: 'success', reasons: [] });
   };
}

export function installScheduleItemActionsTestHooks() {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
         globalThis.CustomEvent = class CustomEvent {
            constructor(type, options = {}) {
               this.type = type;
               this.detail = options.detail;
            }
         };
         updateItineraryErrorTypesFromConfig({
            errorTypes: MOCK_ERROR_TYPES,
            suppressedErrorTypes: [],
         });
      },
      after: () => {
         delete globalThis.CustomEvent;
         delete globalThis.fetch;
         delete globalThis.localStorage;
      },
   });
}
