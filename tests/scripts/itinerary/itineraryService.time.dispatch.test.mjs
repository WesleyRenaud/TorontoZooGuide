import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryServiceFormatter } from '../../../scripts/itinerary/itineraryServiceFormatter.js';
import { installItineraryServiceTestHooks } from '../helpers/itineraryServiceTestSetup.mjs';

installItineraryServiceTestHooks();


test('Test_ItineraryServiceTime_TestDepartureTimeDropsTalkSameDate_ExpectDispatchedWithoutChanges', async () => {
   const updates = [];
   const requestedUrls = [];
   const date = '2026-06-15';
   const arrivalTime = '09:30';
   const departureTime = '16:15';
   window.dispatchEvent = (event) => {
      if (event.type === 'tzg:itineraryUpdated') {
         updates.push(event.detail.itinerary);
      }

      return true;
   };
   globalThis.fetch = async (url) => {
      requestedUrls.push(url);

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'success',
            reasons: [],
            itinerary: {
               date,
               arrival_time: arrivalTime,
               departure_time: departureTime,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const result = await ItineraryServiceFormatter.setItineraryDepartureTime(departureTime);

   assert.deepEqual(requestedUrls, ['/set-itinerary-departure-time']);
   assert.equal(result.validation.hasChanges, false);
   assert.deepEqual(updates, [result]);
});
