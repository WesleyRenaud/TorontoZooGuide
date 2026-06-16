import { updateItineraryErrorTypesFromConfig } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { installDomTestHooks } from './domTestSetup.mjs';

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

export { mockJsonResponse } from './fetchMock.mjs';

export function installScheduleItemActionsTestHooks() {
   installDomTestHooks({
      before: () => {
         updateItineraryErrorTypesFromConfig({
            errorTypes: MOCK_ERROR_TYPES,
            suppressedErrorTypes: [],
         });
      },
      after: () => {
         delete globalThis.fetch;
      },
   });
}
