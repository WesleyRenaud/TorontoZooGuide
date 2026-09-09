import { createLocalStorageMock } from './localStorageMock.mjs';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { installDomTestHooks } from './domTestSetup.mjs';

export function installItineraryServiceTestHooks() {
   installDomTestHooks({
      before: () => {
         globalThis.localStorage = createLocalStorageMock();
         ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
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
