import {
   afterEach,
   beforeEach,
} from 'node:test';

import { createLocalStorageMock } from './localStorageMock.mjs';
import { updateItineraryErrorTypesFromConfig } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import {
   installDocument,
   installTestWindow,
   teardownDocument,
} from './domMock.mjs';

export function installItineraryServiceTestHooks() {
   beforeEach(() => {
      globalThis.localStorage = createLocalStorageMock();
      installTestWindow();
      installDocument();
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
   });

   afterEach(() => {
      teardownDocument();
      delete globalThis.CustomEvent;
      delete globalThis.fetch;
      delete globalThis.localStorage;
      delete globalThis.window;
   });
}
