import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOptionsLoader } from '../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOptionsLoaderHelper } from '../../../../scripts/consoleOperations/options/consoleOptionsLoaderHelper.js';
import { ConsoleOperationsClient } from '../../../../scripts/api/consoleOperationsClient.js';

test('Test_LoadOptionsMethods_TestDelegation_ExpectCachedLoaderArgs', async () => {
   const calls = [];
   const original = ConsoleOptionsLoaderHelper.loadCachedOptions;
   ConsoleOptionsLoaderHelper.loadCachedOptions = async (args) => {
      calls.push(args);
      return ['ok'];
   };

   try {
      assert.deepEqual(await ConsoleOptionsLoader.loadSpecies(), ['ok']);
      assert.deepEqual(await ConsoleOptionsLoader.loadExhibits(), ['ok']);
      assert.deepEqual(await ConsoleOptionsLoader.loadRestaurants(), ['ok']);
      assert.deepEqual(await ConsoleOptionsLoader.loadRestrooms(), ['ok']);
      assert.deepEqual(await ConsoleOptionsLoader.loadGiftShops(), ['ok']);
      assert.deepEqual(await ConsoleOptionsLoader.loadAttractions(), ['ok']);
      assert.deepEqual(await ConsoleOptionsLoader.loadTransportationStations(), ['ok']);
      assert.deepEqual(await ConsoleOptionsLoader.loadGuardiansTalks(), ['ok']);
      assert.deepEqual(await ConsoleOptionsLoader.loadWildEncounters(), ['ok']);

      assert.equal(calls.length, 9);
      assert.equal(calls[0].cacheKey, 'species');
      assert.equal(calls[0].fetchOptions, ConsoleOperationsClient.getSpeciesOptions);
      assert.equal(calls[0].resultKey, 'species');
      assert.equal(calls[6].resultKey, 'transportation_stations');
      assert.equal(calls[8].resultKey, 'wild_encounters');
   } finally {
      ConsoleOptionsLoaderHelper.loadCachedOptions = original;
   }
});

test('Test_LoadClosedExhibits_TestClientResult_ExpectExhibits', async () => {
   const originalGet = ConsoleOperationsClient.getClosedExhibitOptions;

   ConsoleOperationsClient.getClosedExhibitOptions = async () => ({
      exhibits: ['Canadian Domain', 'Kids Zoo'],
   });

   try {
      assert.deepEqual(
         await ConsoleOptionsLoader.loadClosedExhibits(),
         ['Canadian Domain', 'Kids Zoo']
      );
   } finally {
      ConsoleOperationsClient.getClosedExhibitOptions = originalGet;
   }
});

test('Test_LoadClosedRestrooms_TestClientResult_ExpectRestrooms', async () => {
   const originalGet = ConsoleOperationsClient.getClosedRestroomOptions;

   ConsoleOperationsClient.getClosedRestroomOptions = async () => ({
      restrooms: ['Entrance Restroom', 'Africa Restaurant Restroom'],
   });

   try {
      assert.deepEqual(
         await ConsoleOptionsLoader.loadClosedRestrooms(),
         ['Entrance Restroom', 'Africa Restaurant Restroom']
      );
   } finally {
      ConsoleOperationsClient.getClosedRestroomOptions = originalGet;
   }
});

test('Test_LoadAlertRestrooms_TestClientResult_ExpectRestrooms', async () => {
   const originalGet = ConsoleOperationsClient.getRestroomAlertOptions;

   ConsoleOperationsClient.getRestroomAlertOptions = async () => ({
      restrooms: ['Entrance Restroom', 'Splash Island Restroom'],
   });

   try {
      assert.deepEqual(
         await ConsoleOptionsLoader.loadAlertRestrooms(),
         ['Entrance Restroom', 'Splash Island Restroom']
      );
   } finally {
      ConsoleOperationsClient.getRestroomAlertOptions = originalGet;
   }
});

test('Test_LoadClosedTransportationStations_TestClientResult_ExpectStations', async () => {
   const originalGet = ConsoleOperationsClient.getClosedTransportationStationOptions;

   ConsoleOperationsClient.getClosedTransportationStationOptions = async () => ({
      transportation_stations: ['Africa Zoomobile Station', 'Main Zoomobile Station'],
   });

   try {
      assert.deepEqual(
         await ConsoleOptionsLoader.loadClosedTransportationStations(),
         ['Africa Zoomobile Station', 'Main Zoomobile Station']
      );
   } finally {
      ConsoleOperationsClient.getClosedTransportationStationOptions = originalGet;
   }
});

test('Test_LoadOffDisplayExhibits_TestClientResult_ExpectExhibits', async () => {
   const originalGet = ConsoleOperationsClient.getOffDisplayExhibitOptions;

   ConsoleOperationsClient.getOffDisplayExhibitOptions = async () => ({
      exhibits: ['Africa Savanna', 'Eurasia Wilds'],
   });

   try {
      assert.deepEqual(
         await ConsoleOptionsLoader.loadOffDisplayExhibits(),
         ['Africa Savanna', 'Eurasia Wilds']
      );
   } finally {
      ConsoleOperationsClient.getOffDisplayExhibitOptions = originalGet;
   }
});

test('Test_LoadVisibilityScheduleExhibits_TestClientResult_ExpectExhibits', async () => {
   const originalGet = ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions;

   ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions = async () => ({
      exhibits: ['Africa Savanna', 'Eurasia Wilds'],
   });

   try {
      assert.deepEqual(
         await ConsoleOptionsLoader.loadVisibilityScheduleExhibits(),
         ['Africa Savanna', 'Eurasia Wilds']
      );
   } finally {
      ConsoleOperationsClient.getAnimalVisibilityScheduleExhibitOptions = originalGet;
   }
});

test('Test_LoadScheduledWildEncounters_TestClientResult_ExpectEncounters', async () => {
   const originalGet = ConsoleOperationsClient.getWildEncounterScheduleOptions;

   ConsoleOperationsClient.getWildEncounterScheduleOptions = async () => ({
      wild_encounters: ['Giraffe Encounter', 'Kangaroo Encounter'],
   });

   try {
      assert.deepEqual(
         await ConsoleOptionsLoader.loadScheduledWildEncounters(),
         ['Giraffe Encounter', 'Kangaroo Encounter']
      );
   } finally {
      ConsoleOperationsClient.getWildEncounterScheduleOptions = originalGet;
   }
});

test('Test_LoadViewingAlertExhibits_TestClientResult_ExpectExhibits', async () => {
   const originalGet = ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions;

   ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions = async () => ({
      exhibits: ['Africa Savanna', 'Eurasia Wilds'],
   });

   try {
      assert.deepEqual(
         await ConsoleOptionsLoader.loadViewingAlertExhibits(),
         ['Africa Savanna', 'Eurasia Wilds']
      );
   } finally {
      ConsoleOperationsClient.getAnimalViewingAlertExhibitOptions = originalGet;
   }
});
