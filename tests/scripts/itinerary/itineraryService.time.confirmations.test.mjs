import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryServiceFormatter } from '../../../scripts/itinerary/itineraryServiceFormatter.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installItineraryServiceTestHooks } from '../helpers/itineraryServiceTestSetup.mjs';
import { Strings } from '../../../scripts/strings.js';

installItineraryServiceTestHooks();


test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryArrivalTimeConfirmsEarlyAdmissionWarningBeforeRetrying_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-20';
   const arrivalTime = '09:00';
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
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
            text: async () => JSON.stringify({ date }),
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
                  date,
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      const isConfirmed = Boolean(
         requests.at(Position.LAST)?.body?.confirmingEarlyAdmission
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'earlyAdmissionRequiresMembership',
            reasons: [],
            itinerary: {
               date,
               arrival_time: isConfirmed ? arrivalTime : '',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const setPromise = ItineraryServiceFormatter.setItineraryArrivalTime(arrivalTime);
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.equal(
      document.querySelector('.tzg-popup-message').textContent,
      Strings.itinerary.confirmation.earlyAdmissionMessage
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
   assert.deepEqual(setRequests[Position.FIRST].body, {
      arrivalTime,
      confirmingShortVisit: false,
      confirmingEarlyAdmission: false,
   });
   assert.deepEqual(setRequests[Position.SECOND].body, {
      arrivalTime,
      confirmingShortVisit: false,
      confirmingEarlyAdmission: true,
   });
});


test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryDepartureTimeConfirmsShortVisitWarningBeforeRetrying_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-20';
   const departureTime = '16:00';
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
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
            text: async () => JSON.stringify({ date }),
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
                  date,
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [],
               },
            }),
         };
      }

      const isConfirmed = Boolean(
         requests.at(Position.LAST)?.body?.confirmingShortVisit
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'arrivalDepartureTooClose',
            reasons: [],
            itinerary: {
               date,
               departure_time: isConfirmed ? departureTime : '',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const setPromise = ItineraryServiceFormatter.setItineraryDepartureTime(departureTime);
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.equal(
      document.querySelector('.tzg-popup-message').textContent,
      Strings.itinerary.confirmation.shortVisitMessage
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
   assert.deepEqual(setRequests[Position.SECOND].body, {
      departureTime,
      confirmingShortVisit: true,
   });
});


test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryArrivalTimeRejectsWhenTheVisitorCancelsConfirmation_ExpectOk', async () => {
   const date = '2026-06-20';
   const arrivalTime = '09:00';
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date }),
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
                  date,
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
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const setPromise = ItineraryServiceFormatter.setItineraryArrivalTime(arrivalTime);
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   document.querySelector('.tzg-popup-cancel')?.click();

   await assert.rejects(
      setPromise,
      /Itinerary time change cancelled/
   );
});


test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryArrivalTimeThrowsForNonConfirmationErrors_ExpectOk', async () => {
   const date = '2026-06-20';
   const arrivalTime = '09:00';
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date }),
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
                  date,
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
      ItineraryServiceFormatter.setItineraryArrivalTime(arrivalTime),
      /outside operating hours/i
   );
});


test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryArrivalTimeReturnsTheRawAPIResultWhen_ExpectOk', async () => {
   const date = '2026-06-20';
   const arrivalTime = '09:30';
   const errorType = 'success';
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date }),
         };
      }

      if (url === '/get-itinerary') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: errorType,
               reasons: [],
               itinerary: {
                  date,
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
            status: errorType,
            reasons: [],
         }),
      };
   };

   const result = await ItineraryServiceFormatter.setItineraryArrivalTime(arrivalTime);

   assert.equal(result.errorType, errorType);
   assert.equal(result.itinerary, undefined);
});


test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryArrivalTimePersistsWarningSuppressionWhenDoNot_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-20';
   const arrivalTime = '09:00';
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
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
            text: async () => JSON.stringify({ date }),
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
                  date,
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
         requests.filter((request) => request.url === '/set-itinerary-arrival-time').at(Position.LAST)?.body?.confirmingEarlyAdmission
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'earlyAdmissionRequiresMembership',
            reasons: [],
            itinerary: {
               date,
               arrival_time: isConfirmed ? arrivalTime : '',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const setPromise = ItineraryServiceFormatter.setItineraryArrivalTime(arrivalTime);
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


test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryArrivalTimeRejectsWhenTheConfirmedRetryFails_ExpectOk', async () => {
   let arrivalRequestCount = 0;
   const date = '2026-06-20';
   const arrivalTime = '09:00';
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });
   globalThis.fetch = async (url) => {
      if (url === '/get-itinerary-date') {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({ date }),
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
                  date,
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
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   await assert.rejects(async () => {
      const setPromise = ItineraryServiceFormatter.setItineraryArrivalTime(arrivalTime);

      await new Promise((resolve) => {
         setTimeout(resolve, 0);
      });

      document.querySelector('.tzg-popup-confirm')?.click();

      await setPromise;
   }, /outside operating hours/i);
});
