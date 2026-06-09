import {
   afterEach,
   beforeEach,
} from 'node:test';

import { updateItineraryErrorTypesFromConfig } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import {
   installDocument,
   installTestWindow,
   teardownDocument,
} from './domMock.mjs';

export const MOCK_ERROR_TYPES = Object.freeze({
   SUCCESS: 'success',
   SAVE_FAILED: 'saveFailed',
   NO_AVAILABLE_SLOT: 'noAvailableSlot',
   REQUESTED_TIME_NOT_AVAILABLE: 'requestedTimeNotAvailable',
   ITEM_NOT_ON_ITINERARY: 'itemNotOnItinerary',
   GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: 'guardiansTalkWillUnscheduleItems',
   WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS: 'wildEncounterWillUnscheduleItems',
   BULK_SCHEDULE_ANIMALS_ALREADY_SCHEDULED: 'bulkScheduleAnimalsAlreadyScheduled',
});

export function mockJsonResponse(payload) {
   return {
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify(payload),
   };
}

export function installScheduleItemActionsTestHooks() {
   beforeEach(() => {
      installTestWindow();
      installDocument();
      updateItineraryErrorTypesFromConfig({
         errorTypes: MOCK_ERROR_TYPES,
         suppressedErrorTypes: [],
      });
   });

   afterEach(() => {
      teardownDocument();
      delete globalThis.fetch;
      delete globalThis.window;
   });
}
