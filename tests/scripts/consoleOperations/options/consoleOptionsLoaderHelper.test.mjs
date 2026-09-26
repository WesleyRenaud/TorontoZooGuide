import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOptionsLoaderHelper } from '../../../../scripts/consoleOperations/options/consoleOptionsLoaderHelper.js';
import { NamedItems } from '../../../../scripts/consoleOperations/options/namedItems.js';


test('Test_LoadCachedOptions_TestFetch_ExpectSorted', async () => {
   const cacheKey = 'species';
   const lion = { name: 'Lion' };
   const tiger = { name: 'Tiger' };
   const animals = [tiger, lion];
   ConsoleOptionsLoaderHelper.cachedOptionSets[cacheKey] = null;

   const options = await ConsoleOptionsLoaderHelper.loadCachedOptions({
      cacheKey,
      resultKey: 'animals',
      fetchOptions: async () => ({ animals }),
   });

   assert.deepEqual(options, NamedItems.sortNamedOptions(animals));
   ConsoleOptionsLoaderHelper.cachedOptionSets[cacheKey] = null;
});


test('Test_LoadCachedOptions_TestCached_ExpectSameReference', async () => {
   const cacheKey = 'species';
   const lion = { name: 'Lion' };
   const tiger = { name: 'Tiger' };
   ConsoleOptionsLoaderHelper.cachedOptionSets[cacheKey] = null;
   const options = await ConsoleOptionsLoaderHelper.loadCachedOptions({
      cacheKey,
      resultKey: 'animals',
      fetchOptions: async () => ({ animals: [tiger, lion] }),
   });

   const cached = await ConsoleOptionsLoaderHelper.loadCachedOptions({
      cacheKey,
      resultKey: 'animals',
      fetchOptions: async () => ({ animals: [] }),
   });

   assert.equal(cached, options);
   ConsoleOptionsLoaderHelper.cachedOptionSets[cacheKey] = null;
});
