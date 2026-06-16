import { createLocalStorageMock } from './localStorageMock.mjs';
import { updateItineraryErrorTypesFromConfig } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { installDomTestHooks } from './domTestSetup.mjs';

export function installItineraryServiceTestHooks() {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
         updateItineraryErrorTypesFromConfig({
            errorTypes: {
               SUCCESS: 'success',
               GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: 'guardiansTalkWillUnscheduleItems',
            },
            suppressedErrorTypes: [],
         });
         globalThis.CustomEvent = class CustomEvent {
            constructor(type, options = {}) {
               this.type = type;
               this.detail = options.detail;
            }
         };
      },
      after: () => {
         delete globalThis.CustomEvent;
         delete globalThis.fetch;
         delete globalThis.localStorage;
      },
   });
}
