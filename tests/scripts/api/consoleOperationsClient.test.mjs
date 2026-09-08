import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOperationsClient } from '../../../scripts/api/consoleOperationsClient.js';
import { ApiClient } from '../../../scripts/api/apiClient.js';

const _NO_ARG_GETTERS = [
   ['getSpeciesOptions', '/get-species'],
   ['getExhibitOptions', '/get-exhibits'],
   ['getRestaurantNameOptions', '/get-restaurant-names'],
   ['getRestroomNameOptions', '/get-restroom-names'],
   ['getGiftShopNameOptions', '/get-gift-shop-names'],
   ['getAttractionNameOptions', '/get-attraction-names'],
   ['getTransportationStationNameOptions', '/get-transportation-station-names'],
   ['getGuardiansTalkNameOptions', '/get-guardians-talk-names'],
   ['getWildEncounterNameOptions', '/get-wild-encounter-names'],
   ['getActiveUpdateOptions', '/get-active-update-options'],
   ['getGuardiansTalkLocations', '/get-guardians-talk-locations'],
];

const _PAYLOAD_METHODS = [
   ['setAnimalOffDisplay', '/set-animal-off-display'],
   ['setAnimalOnDisplay', '/set-animal-on-display'],
   ['setAnimalViewingAlert', '/set-animal-viewing-alert'],
   ['removeAnimalViewingAlert', '/remove-animal-viewing-alert'],
   ['setAnimalVisibilitySchedule', '/set-animal-visibility-schedule'],
   ['removeAnimalVisibilitySchedule', '/remove-animal-visibility-schedule'],
   ['setExhibitOpen', '/set-exhibit-open'],
   ['setExhibitClosed', '/set-exhibit-closed'],
   ['setRestaurantOpeningSchedule', '/set-restaurant-opening-schedule'],
   ['replaceRestaurantOpeningScheduleOverlaps', '/replace-restaurant-opening-schedule-overlaps'],
   ['trimRestaurantOpeningScheduleOverlaps', '/trim-restaurant-opening-schedule-overlaps'],
   ['setRestaurantClosed', '/set-restaurant-closed'],
   ['setRestaurantClosureOverride', '/set-restaurant-closure-override'],
   ['setRestroomOpen', '/set-restroom-open'],
   ['setRestroomClosed', '/set-restroom-closed'],
   ['setRestroomAlert', '/set-restroom-alert'],
   ['removeRestroomAlert', '/remove-restroom-alert'],
   ['createUpdate', '/create-update'],
   ['createEvent', '/create-event'],
   ['endUpdate', '/end-update'],
   ['editUpdate', '/edit-update'],
   ['setGiftShopOpeningSchedule', '/set-gift-shop-opening-schedule'],
   ['replaceGiftShopOpeningScheduleOverlaps', '/replace-gift-shop-opening-schedule-overlaps'],
   ['trimGiftShopOpeningScheduleOverlaps', '/trim-gift-shop-opening-schedule-overlaps'],
   ['setGiftShopClosed', '/set-gift-shop-closed'],
   ['setGiftShopClosureOverride', '/set-gift-shop-closure-override'],
   ['setAttractionOpeningSchedule', '/set-attraction-opening-schedule'],
   ['replaceAttractionOpeningScheduleOverlaps', '/replace-attraction-opening-schedule-overlaps'],
   ['trimAttractionOpeningScheduleOverlaps', '/trim-attraction-opening-schedule-overlaps'],
   ['setAttractionClosed', '/set-attraction-closed'],
   ['setAttractionClosureOverride', '/set-attraction-closure-override'],
   ['getAttractionHoursScheduleTimeBounds', '/get-attraction-hours-schedule-time-bounds'],
   ['setAttractionHoursSchedule', '/set-attraction-hours-schedule'],
   ['replaceAttractionHoursScheduleOverlaps', '/replace-attraction-hours-schedule-overlaps'],
   ['trimAttractionHoursScheduleOverlaps', '/trim-attraction-hours-schedule-overlaps'],
   ['setTransportationStationOpen', '/set-transportation-station-open'],
   ['setTransportationStationClosed', '/set-transportation-station-closed'],
   ['setCurrentTransportationRoute', '/set-current-transportation-route'],
   ['getGuardiansTalkNamesAtLocation', '/get-guardians-talk-names-at-location'],
   ['setGuardiansTalkSchedule', '/set-guardians-talk-schedule'],
   ['replaceGuardiansTalkScheduleOverlaps', '/replace-guardians-talk-schedule-overlaps'],
   ['trimGuardiansTalkScheduleOverlaps', '/trim-guardians-talk-schedule-overlaps'],
   ['endGuardiansTalkSchedule', '/end-guardians-talk-schedule'],
   ['getGuardiansTalkOccurrences', '/get-guardians-talk-occurrences'],
   ['getGuardiansTalkScheduleTimes', '/get-guardians-talk-schedule-times'],
   ['cancelGuardiansTalkOccurrence', '/cancel-guardians-talk-occurrence'],
   ['addGuardiansTalkOccurrence', '/add-guardians-talk-occurrence'],
   ['setWildEncounterSchedule', '/set-wild-encounter-schedule'],
   ['replaceWildEncounterScheduleOverlaps', '/replace-wild-encounter-schedule-overlaps'],
   ['trimWildEncounterScheduleOverlaps', '/trim-wild-encounter-schedule-overlaps'],
   ['endWildEncounterSchedule', '/end-wild-encounter-schedule'],
   ['getWildEncounterScheduleTimes', '/get-wild-encounter-schedule-times'],
   ['getWildEncounterOccurrences', '/get-wild-encounter-occurrences'],
   ['cancelWildEncounterOccurrence', '/cancel-wild-encounter-occurrence'],
   ['setDrinkingFountainsClosed', '/set-drinking-fountains-closed'],
   ['setDrinkingFountainsOpen', '/set-drinking-fountains-open'],
];

test('Test_ConsoleOperationsClient', async () => {
   const originalPost = ApiClient.postJson;
   const calls = [];

   ApiClient.postJson = async (url, payload) => {
      calls.push([url, payload]);
      return { ok: true, url, payload };
   };

   try {
      for (const [methodName, url] of _NO_ARG_GETTERS) {
         assert.deepEqual(await ConsoleOperationsClient[methodName](), {
            ok: true,
            url,
            payload: {},
         });
      }

      for (const [methodName, url] of _PAYLOAD_METHODS) {
         const payload = { method: methodName };
         assert.deepEqual(await ConsoleOperationsClient[methodName](payload), {
            ok: true,
            url,
            payload,
         });
      }

      assert.deepEqual(
         await ConsoleOperationsClient.getAttractionHoursScheduleTimeBounds(),
         {
            ok: true,
            url: '/get-attraction-hours-schedule-time-bounds',
            payload: {},
         }
      );

      assert.equal(
         calls.length,
         _NO_ARG_GETTERS.length + _PAYLOAD_METHODS.length + 1
      );
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
