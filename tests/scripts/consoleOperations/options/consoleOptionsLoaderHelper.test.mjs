import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleOptionsLoaderHelper } from '../../../../scripts/consoleOperations/options/consoleOptionsLoaderHelper.js';

test('Test_LoadCachedOptions_TestFetchAndCache_ExpectSortedCached', async () => {
   ConsoleOptionsLoaderHelper.cachedOptionSets.species = null;
   let fetches = 0;

   const options = await ConsoleOptionsLoaderHelper.loadCachedOptions({
      cacheKey: 'species',
      resultKey: 'animals',
      fetchOptions: async () => {
         fetches += 1;
         return { animals: [{ name: 'Tiger' }, { name: 'Lion' }] };
      },
   });

   assert.deepEqual(options, [{ name: 'Lion' }, { name: 'Tiger' }]);
   assert.equal(fetches, 1);

   const cached = await ConsoleOptionsLoaderHelper.loadCachedOptions({
      cacheKey: 'species',
      resultKey: 'animals',
      fetchOptions: async () => {
         fetches += 1;
         return { animals: [] };
      },
   });

   assert.equal(cached, options);
   assert.equal(fetches, 1);
   ConsoleOptionsLoaderHelper.cachedOptionSets.species = null;
});
