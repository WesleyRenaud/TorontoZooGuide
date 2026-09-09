import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { installDomTestHooks } from './domTestSetup.mjs';
import { mockJsonResponse } from './fetchMock.mjs';
import { createLocalStorageMock } from './localStorageMock.mjs';

export const MOCK_ERROR_TYPES = Object.freeze({
   SUCCESS: ItineraryErrorType.SUCCESS,
   SAVE_FAILED: ItineraryErrorType.SAVE_FAILED,
   ACTIVITY_NOT_ON_DAY_SCHEDULE: ItineraryErrorType.ACTIVITY_NOT_ON_DAY_SCHEDULE,
   SCHEDULE_WINDOW_UNAVAILABLE: ItineraryErrorType.SCHEDULE_WINDOW_UNAVAILABLE,
   NO_AVAILABLE_SLOT: ItineraryErrorType.NO_AVAILABLE_SLOT,
   REQUESTED_TIME_NOT_AVAILABLE: ItineraryErrorType.REQUESTED_TIME_NOT_AVAILABLE,
   ATTRACTION_OUTSIDE_OPERATING_HOURS: ItineraryErrorType.ATTRACTION_OUTSIDE_OPERATING_HOURS,
   ITEM_NOT_ON_ITINERARY: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
   ITEM_ALREADY_SCHEDULED: ItineraryErrorType.ITEM_ALREADY_SCHEDULED,
   GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
   FIXED_TIME_ITEM_LONG_WAIT: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
   GUARDIANS_TALK_WITHOUT_ANIMAL: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
   ATTRACTION_WITHOUT_ANIMAL: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
   WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
   BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED: ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED,
   UNSCHEDULE_ALL_NOTHING_SCHEDULED: ItineraryErrorType.UNSCHEDULE_ALL_NOTHING_SCHEDULED,
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
         ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
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
