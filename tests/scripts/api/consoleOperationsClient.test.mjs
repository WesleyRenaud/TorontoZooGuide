import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../scripts/api/consoleOperationsClient.js';
import { ApiClient } from '../../../scripts/api/apiClient.js';

test('Test_ConsoleOperationsClientGetters_TestDelegation_ExpectPostJson', async () => {
   const originalPost = ApiClient.postJson;
   const calls = [];

   ApiClient.postJson = async (url, payload) => {
      calls.push([url, payload]);
      return { ok: true, url, payload };
   };

   try {
      assert.deepEqual(await ConsoleOperationsClient.getSpeciesOptions(), {
         ok: true,
         url: '/get-species',
         payload: {},
      });
      assert.deepEqual(await ConsoleOperationsClient.getExhibitOptions(), {
         ok: true,
         url: '/get-exhibits',
         payload: {},
      });
      assert.deepEqual(await ConsoleOperationsClient.getRestaurantNameOptions(), {
         ok: true,
         url: '/get-restaurant-names',
         payload: {},
      });
      assert.deepEqual(await ConsoleOperationsClient.getActiveUpdateOptions(), {
         ok: true,
         url: '/get-active-update-options',
         payload: {},
      });
      assert.deepEqual(await ConsoleOperationsClient.getGuardiansTalkLocations(), {
         ok: true,
         url: '/get-guardians-talk-locations',
         payload: {},
      });
      assert.deepEqual(
         await ConsoleOperationsClient.getAttractionHoursScheduleTimeBounds({ attraction: 'Carousel' }),
         {
            ok: true,
            url: '/get-attraction-hours-schedule-time-bounds',
            payload: { attraction: 'Carousel' },
         }
      );

      assert.deepEqual(calls[0], ['/get-species', {}]);
      assert.deepEqual(calls.at(-1), [
         '/get-attraction-hours-schedule-time-bounds',
         { attraction: 'Carousel' },
      ]);
   } finally {
      ApiClient.postJson = originalPost;
   }
});

test('Test_ConsoleOperationsClientMutations_TestPayloads_ExpectPostJson', async () => {
   const originalPost = ApiClient.postJson;
   const calls = [];

   ApiClient.postJson = async (url, payload) => {
      calls.push([url, payload]);
      return { success: true, url, payload };
   };

   try {
      const animalPayload = { species: 'Lion', exhibit: 'Savanna' };
      assert.deepEqual(
         await ConsoleOperationsClient.setAnimalOffDisplay(animalPayload),
         { success: true, url: '/set-animal-off-display', payload: animalPayload }
      );
      assert.deepEqual(
         await ConsoleOperationsClient.setRestaurantOpeningSchedule({ restaurant: 'Peaks' }),
         {
            success: true,
            url: '/set-restaurant-opening-schedule',
            payload: { restaurant: 'Peaks' },
         }
      );
      assert.deepEqual(
         await ConsoleOperationsClient.cancelGuardiansTalkOccurrence({
            talk: 'Tiger',
            location: 'Eurasia',
         }),
         {
            success: true,
            url: '/cancel-guardians-talk-occurrence',
            payload: { talk: 'Tiger', location: 'Eurasia' },
         }
      );
      assert.deepEqual(
         await ConsoleOperationsClient.cancelWildEncounterOccurrence({
            wildEncounter: 'Giraffe',
            date: '2026-07-01',
         }),
         {
            success: true,
            url: '/cancel-wild-encounter-occurrence',
            payload: { wildEncounter: 'Giraffe', date: '2026-07-01' },
         }
      );
      assert.deepEqual(
         await ConsoleOperationsClient.createUpdate({ title: 'Notice' }),
         { success: true, url: '/create-update', payload: { title: 'Notice' } }
      );
      assert.deepEqual(
         await ConsoleOperationsClient.setDrinkingFountainsClosed({ startDate: '2026-01-01' }),
         {
            success: true,
            url: '/set-drinking-fountains-closed',
            payload: { startDate: '2026-01-01' },
         }
      );

      assert.equal(calls.length, 6);
      assert.equal(calls[0][0], '/set-animal-off-display');
      assert.equal(calls[2][0], '/cancel-guardians-talk-occurrence');
   } finally {
      ApiClient.postJson = originalPost;
   }
});

test('Test_ConsoleOperationsClient_TestPostJsonThrows_ExpectPropagates', async () => {
   const originalPost = ApiClient.postJson;
   ApiClient.postJson = async () => {
      throw new Error('network down');
   };

   try {
      await assert.rejects(
         () => ConsoleOperationsClient.getWildEncounterNameOptions(),
         { message: 'network down' }
      );
      await assert.rejects(
         () => ConsoleOperationsClient.setExhibitClosed({ exhibit: 'Savanna' }),
         { message: 'network down' }
      );
   } finally {
      ApiClient.postJson = originalPost;
   }
});

test('Test_ConsoleOperationsClientOverlapHelpers_TestEndpoints_ExpectDelegated', async () => {
   const originalPost = ApiClient.postJson;
   ApiClient.postJson = async (url, payload) => ({ url, payload });

   try {
      assert.deepEqual(
         await ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps({ restaurant: 'A' }),
         { url: '/replace-restaurant-opening-schedule-overlaps', payload: { restaurant: 'A' } }
      );
      assert.deepEqual(
         await ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps({ giftShop: 'B' }),
         { url: '/trim-gift-shop-opening-schedule-overlaps', payload: { giftShop: 'B' } }
      );
      assert.deepEqual(
         await ConsoleOperationsClient.replaceAttractionHoursScheduleOverlaps({ attraction: 'C' }),
         { url: '/replace-attraction-hours-schedule-overlaps', payload: { attraction: 'C' } }
      );
      assert.deepEqual(
         await ConsoleOperationsClient.trimWildEncounterScheduleOverlaps({ wildEncounter: 'D' }),
         { url: '/trim-wild-encounter-schedule-overlaps', payload: { wildEncounter: 'D' } }
      );
   } finally {
      ApiClient.postJson = originalPost;
   }
});
