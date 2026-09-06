import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryServiceTime } from '../../../scripts/itinerary/itineraryServiceTime.js';
import { installItineraryServiceTestHooks } from '../helpers/itineraryServiceTestSetup.mjs';

installItineraryServiceTestHooks();

test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryDepartureTimeDispatchesUnscheduledDiffForTrimmedVisit_ExpectOk', async () => {
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

   const result = await ItineraryServiceTime.setItineraryDepartureTime('16:15');

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

test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryDepartureTimeDispatchesRemovedAndUnscheduledTalksAnd_ExpectOk', async () => {
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

   const result = await ItineraryServiceTime.setItineraryDepartureTime('16:15');

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
