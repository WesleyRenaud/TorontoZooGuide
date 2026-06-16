import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   setItineraryArrivalTime,
   setItineraryDepartureTime,
} from '../../scripts/itinerary/itineraryServiceTime.js';
import { updateItineraryErrorTypesFromConfig } from '../../scripts/itinerary/itineraryErrorTypes.js';
import { installItineraryServiceTestHooks } from './helpers/itineraryServiceTestSetup.mjs';

installItineraryServiceTestHooks();

test('setItineraryArrivalTime confirms early admission warning before retrying', async () => {
   const requests = [];

   updateItineraryErrorTypesFromConfig({
      errorTypes: {
         SUCCESS: 'success',
         EARLY_ADMISSION_REQUIRES_MEMBERSHIP: 'earlyAdmissionRequiresMembership',
      },
      suppressedErrorTypes: [],
   });

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date: '2026-06-20' }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary: {
                  date: '2026-06-20',
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingEarlyAdmission
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'earlyAdmissionRequiresMembership',
            reasons: [],
            itinerary: {
               date: '2026-06-20',
               arrival_time: isConfirmed ? '09:00' : '',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const setPromise = setItineraryArrivalTime('09:00');

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.match(
      document.querySelector('.tzg-popup-message')?.textContent ?? '',
      /Early admission hours are only available/
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await setPromise;

   const setRequests = requests.filter((request) => (
      request.url === '/set-itinerary-arrival-time'
   ));

   assert.equal(setRequests.length, 2);
   assert.deepEqual(setRequests[0].body, {
      arrivalTime: '09:00',
      confirmingShortVisit: false,
      confirmingEarlyAdmission: false,
   });
   assert.deepEqual(setRequests[1].body, {
      arrivalTime: '09:00',
      confirmingShortVisit: false,
      confirmingEarlyAdmission: true,
   });
});

test('setItineraryDepartureTime dispatches unscheduled diff for trimmed visit window', async () => {
   const updates = [];

   window.dispatchEvent = (event) => {
      if (event.type === 'tzg:itineraryUpdated') {
         updates.push(event.detail.itinerary);
      }

      return true;
   };

   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date: '2026-06-15' }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary: {
                  date: '2026-06-15',
                  arrival_time: '09:30',
                  departure_time: '17:00',
                  animals: [
                     {
                        species: 'African Lion',
                        exhibit: 'Africa Savanna',
                        start_time: '16:30',
                        end_time: '16:45',
                     },
                  ],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      assert.equal(url, '/set-itinerary-departure-time');

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'success',
            reasons: [],
            itinerary: {
               date: '2026-06-15',
               arrival_time: '09:30',
               departure_time: '16:15',
               animals: [
                  {
                     species: 'African Lion',
                     exhibit: 'Africa Savanna',
                  },
               ],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const result = await setItineraryDepartureTime('16:15');

   assert.equal(result.validation.hasChanges, true);
   assert.deepEqual(
      result.validation.unscheduled.animals.map((animal) => animal.species),
      ['African Lion']
   );
   assert.equal(updates.length, 1);
   assert.deepEqual(
      updates[0].validation.unscheduled.animals.map((animal) => animal.species),
      ['African Lion']
   );
});

test('setItineraryDepartureTime dispatches removed and unscheduled talks and encounters', async () => {
   const updates = [];

   window.dispatchEvent = (event) => {
      if (event.type === 'tzg:itineraryUpdated') {
         updates.push(event.detail.itinerary);
      }

      return true;
   };

   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date: '2026-06-15' }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary: {
                  date: '2026-06-15',
                  arrival_time: '09:30',
                  departure_time: '17:00',
                  animals: [],
                  attractions: [],
                  guardians_talks: [
                     {
                        name: 'African Lion',
                        start_time: '16:30',
                        end_time: '16:45',
                     },
                  ],
                  wild_encounters: [
                     {
                        name: 'African Rainforest',
                        start_time: '16:30',
                        end_time: '16:45',
                     },
                  ],
               },
            }),
         };
      }

      assert.equal(url, '/set-itinerary-departure-time');

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'success',
            reasons: [],
            itinerary: {
               date: '2026-06-15',
               arrival_time: '09:30',
               departure_time: '16:15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const result = await setItineraryDepartureTime('16:15');

   assert.equal(result.validation.hasChanges, true);
   assert.deepEqual(
      result.validation.removed.guardiansTalks.map((talk) => talk.name),
      ['African Lion']
   );
   assert.deepEqual(
      result.validation.removed.wildEncounters.map((encounter) => encounter.name),
      ['African Rainforest']
   );
   assert.equal(updates.length, 1);
   assert.deepEqual(
      updates[0].validation.removed.guardiansTalks.map((talk) => talk.name),
      ['African Lion']
   );
   assert.deepEqual(
      updates[0].validation.removed.wildEncounters.map((encounter) => encounter.name),
      ['African Rainforest']
   );
});

test('setItineraryDepartureTime confirms short visit warning before retrying', async () => {
   const requests = [];

   updateItineraryErrorTypesFromConfig({
      errorTypes: {
         SUCCESS: 'success',
         ARRIVAL_DEPARTURE_TOO_CLOSE: 'arrivalDepartureTooClose',
      },
      suppressedErrorTypes: [],
   });

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options?.body ?? '{}'),
      });

      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date: '2026-06-20' }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary: {
                  date: '2026-06-20',
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingShortVisit
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'arrivalDepartureTooClose',
            reasons: [],
            itinerary: {
               date: '2026-06-20',
               departure_time: isConfirmed ? '16:00' : '',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const setPromise = setItineraryDepartureTime('16:00');

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.match(
      document.querySelector('.tzg-popup-message')?.textContent ?? '',
      /very close together/i
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await setPromise;

   const setRequests = requests.filter((request) => (
      request.url === '/set-itinerary-departure-time'
   ));

   assert.equal(setRequests.length, 2);
   assert.deepEqual(setRequests[1].body, {
      departureTime: '16:00',
      confirmingShortVisit: true,
   });
});

test('setItineraryArrivalTime rejects when the visitor cancels confirmation', async () => {
   updateItineraryErrorTypesFromConfig({
      errorTypes: {
         SUCCESS: 'success',
         EARLY_ADMISSION_REQUIRES_MEMBERSHIP: 'earlyAdmissionRequiresMembership',
      },
      suppressedErrorTypes: [],
   });

   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date: '2026-06-20' }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary: {
                  date: '2026-06-20',
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'earlyAdmissionRequiresMembership',
            reasons: [],
            itinerary: {
               date: '2026-06-20',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const setPromise = setItineraryArrivalTime('09:00');

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   document.querySelector('.tzg-popup-cancel')?.click();

   await assert.rejects(
      setPromise,
      /Itinerary time change cancelled/
   );
});

test('setItineraryArrivalTime throws for non-confirmation errors', async () => {
   updateItineraryErrorTypesFromConfig({
      errorTypes: {
         SUCCESS: 'success',
         TIME_OUT_OF_BOUNDS: 'timeOutOfBounds',
         EARLY_ADMISSION_REQUIRES_MEMBERSHIP: 'earlyAdmissionRequiresMembership',
         ARRIVAL_DEPARTURE_TOO_CLOSE: 'arrivalDepartureTooClose',
      },
      suppressedErrorTypes: [],
   });

   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date: '2026-06-20' }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary: {
                  date: '2026-06-20',
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'timeOutOfBounds',
            reasons: [],
         }),
      };
   };

   await assert.rejects(
      setItineraryArrivalTime('09:00'),
      /outside operating hours/i
   );
});

test('setItineraryArrivalTime returns the raw API result when no itinerary payload is included', async () => {
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date: '2026-06-20' }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary: {
                  date: '2026-06-20',
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'success',
            reasons: [],
         }),
      };
   };

   const result = await setItineraryArrivalTime('09:30');

   assert.equal(result.errorType, 'success');
   assert.equal(result.itinerary, undefined);
});

test('setItineraryArrivalTime persists warning suppression when do not show again is checked', async () => {
   const requests = [];

   updateItineraryErrorTypesFromConfig({
      errorTypes: {
         SUCCESS: 'success',
         EARLY_ADMISSION_REQUIRES_MEMBERSHIP: 'earlyAdmissionRequiresMembership',
      },
      suppressedErrorTypes: [],
   });

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options?.body ?? '{}'),
      });

      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date: '2026-06-20' }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary: {
                  date: '2026-06-20',
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      if (url === '/suppress-itinerary-warning') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ status: 'success' }),
         };
      }

      const isConfirmed = Boolean(
         requests.filter((request) => request.url === '/set-itinerary-arrival-time').at(-1)?.body?.confirmingEarlyAdmission
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'earlyAdmissionRequiresMembership',
            reasons: [],
            itinerary: {
               date: '2026-06-20',
               arrival_time: isConfirmed ? '09:00' : '',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const setPromise = setItineraryArrivalTime('09:00');

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const doNotShowAgainLabel = document.querySelector('.tzg-popup-do-not-show-again');
   const checkbox = doNotShowAgainLabel?.children?.find(
      (child) => child.tagName === 'input'
   );

   assert.ok(checkbox);
   checkbox.checked = true;
   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await setPromise;

   assert.equal(
      requests.some((request) => request.url === '/suppress-itinerary-warning'),
      true
   );
});

test('setItineraryArrivalTime rejects when the confirmed retry fails', async () => {
   let arrivalRequestCount = 0;

   updateItineraryErrorTypesFromConfig({
      errorTypes: {
         SUCCESS: 'success',
         TIME_OUT_OF_BOUNDS: 'timeOutOfBounds',
         EARLY_ADMISSION_REQUIRES_MEMBERSHIP: 'earlyAdmissionRequiresMembership',
      },
      suppressedErrorTypes: [],
   });

   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date: '2026-06-20' }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary: {
                  date: '2026-06-20',
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      assert.equal(url, '/set-itinerary-arrival-time');

      arrivalRequestCount += 1;

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: arrivalRequestCount === 1
               ? 'earlyAdmissionRequiresMembership'
               : 'timeOutOfBounds',
            reasons: [],
            itinerary: {
               date: '2026-06-20',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   await assert.rejects(async () => {
      const setPromise = setItineraryArrivalTime('09:00');

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      document.querySelector('.tzg-popup-confirm')?.click();

      await setPromise;
   }, /outside operating hours/i);
});
