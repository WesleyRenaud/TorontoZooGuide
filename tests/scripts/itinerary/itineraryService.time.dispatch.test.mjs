import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryServiceFormatter } from '../../../scripts/itinerary/itineraryServiceFormatter.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installItineraryServiceTestHooks } from '../helpers/itineraryServiceTestSetup.mjs';

installItineraryServiceTestHooks();


test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryDepartureTimeDispatchesUnscheduledDiffForTrimmedVisit_ExpectOk', async () => {
   const updates = [];
   const date = '2026-06-15';
   const arrivalTime = '09:30';
   const departureTime = '16:15';
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
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
                  arrival_time: arrivalTime,
                  departure_time: '17:00',
                  animals: [
                     {
                        species,
                        exhibit,
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
               date,
               arrival_time: arrivalTime,
               departure_time: departureTime,
               animals: [
                  {
                     species,
                     exhibit,
                  },
               ],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const result = await ItineraryServiceFormatter.setItineraryDepartureTime(departureTime);

   assert.equal(result.validation.hasChanges, true);
   assert.equal(result.validation.unscheduled.animals[Position.FIRST].species, species);
   assert.equal(updates.length, 1);
   assert.equal(
      updates[Position.FIRST].validation.unscheduled.animals[Position.FIRST].species,
      species
   );
});


test('Test_ItineraryServiceTime_TestItineraryServiceTimeSetItineraryDepartureTimeDispatchesRemovedAndUnscheduledTalksAnd_ExpectOk', async () => {
   const updates = [];
   const date = '2026-06-15';
   const arrivalTime = '09:30';
   const departureTime = '16:15';
   const talkName = 'African Lion';
   const encounterName = 'African Rainforest';
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
                  arrival_time: arrivalTime,
                  departure_time: '17:00',
                  animals: [],
                  attractions: [],
                  guardians_talks: [
                     {
                        name: talkName,
                        start_time: '16:30',
                        end_time: '16:45',
                     },
                  ],
                  wild_encounters: [
                     {
                        name: encounterName,
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

   assert.equal(result.validation.hasChanges, true);
   assert.equal(result.validation.removed.guardiansTalks[Position.FIRST].name, talkName);
   assert.equal(result.validation.removed.wildEncounters[Position.FIRST].name, encounterName);
   assert.equal(updates.length, 1);
   assert.equal(
      updates[Position.FIRST].validation.removed.guardiansTalks[Position.FIRST].name,
      talkName
   );
   assert.equal(
      updates[Position.FIRST].validation.removed.wildEncounters[Position.FIRST].name,
      encounterName
   );
});
