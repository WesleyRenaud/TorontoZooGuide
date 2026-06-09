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

function createLocalStorageMock() {
   const values = new Map();

   return {
      getItem: (key) => values.get(key) ?? null,
      setItem: (key, value) => {
         values.set(key, String(value));
      },
      removeItem: (key) => {
         values.delete(key);
      },
   };
}

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
