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
