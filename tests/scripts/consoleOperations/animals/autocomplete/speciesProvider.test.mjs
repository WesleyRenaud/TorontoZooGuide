import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesProvider } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesProvider.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { AnimalsClient } from '../../../../../scripts/api/animalsClient.js';
import { SpeciesSourceNormalizer } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesSourceNormalizer.js';

test('Test_CreateAnimalSpeciesSource_TestLoadForExhibit_ExpectCachedLists', async () => {
   const originalLoad = ConsoleOptionsLoader.loadSpecies;
   const originalAnimals = AnimalsClient.getAnimalsInExhibit;
   const originalNormalizeList = SpeciesSourceNormalizer.normalizeSpeciesList;
   const originalNormalizeKey = SpeciesSourceNormalizer.normalizeExhibitKey;
   let speciesLoads = 0;

   ConsoleOptionsLoader.loadSpecies = async () => {
      speciesLoads += 1;
      return ['Lion', 'Tiger'];
   };
   AnimalsClient.getAnimalsInExhibit = async () => ['Giraffe'];
   SpeciesSourceNormalizer.normalizeSpeciesList = (list) => list;
   SpeciesSourceNormalizer.normalizeExhibitKey = (value) => value || '';

   try {
      const source = SpeciesProvider.createAnimalSpeciesSource();
      assert.deepEqual(await source.loadForExhibit(''), ['Lion', 'Tiger']);
      assert.deepEqual(await source.loadForExhibit(''), ['Lion', 'Tiger']);
      assert.equal(speciesLoads, 1);

      assert.deepEqual(await source.loadForExhibit('Savanna'), ['Giraffe']);
      assert.deepEqual(await source.loadForExhibit('Savanna'), ['Giraffe']);
   } finally {
      ConsoleOptionsLoader.loadSpecies = originalLoad;
      AnimalsClient.getAnimalsInExhibit = originalAnimals;
      SpeciesSourceNormalizer.normalizeSpeciesList = originalNormalizeList;
      SpeciesSourceNormalizer.normalizeExhibitKey = originalNormalizeKey;
   }
});

test('Test_CreateAnimalSpeciesSource_TestInjectedFetchersWithoutCache_ExpectRefetch', async () => {
   let allLoads = 0;
   let exhibitLoads = 0;

   const source = SpeciesProvider.createAnimalSpeciesSource({
      fetchAllSpecies: async () => {
         allLoads += 1;
         return ['Lion'];
      },
      fetchSpeciesForExhibit: async (exhibit) => {
         exhibitLoads += 1;
         assert.equal(exhibit, 'Savanna');
         if (exhibitLoads === 1) {
            return undefined;
         }

         return [null, 'Giraffe'];
      },
      cacheLists: false,
   });

   assert.deepEqual(await source.loadForExhibit(''), ['Lion']);
   assert.deepEqual(await source.loadForExhibit(''), ['Lion']);
   assert.equal(allLoads, 2);

   assert.deepEqual(await source.loadForExhibit('Savanna'), []);
   assert.deepEqual(await source.loadForExhibit('Savanna'), ['Giraffe']);
   assert.equal(exhibitLoads, 2);
});

test('Test_FetchOffDisplaySpecies_TestClientResult_ExpectSpecies', async () => {
   const originalGet = ConsoleOperationsClient.getOffDisplayAnimalOptions;
   const payloads = [];

   ConsoleOperationsClient.getOffDisplayAnimalOptions = async (payload) => {
      payloads.push(payload);
      return { species: ['Lion'] };
   };

   try {
      assert.deepEqual(await SpeciesProvider.fetchOffDisplaySpecies(), ['Lion']);
      assert.deepEqual(payloads, [undefined]);
   } finally {
      ConsoleOperationsClient.getOffDisplayAnimalOptions = originalGet;
   }
});

test('Test_FetchOffDisplaySpeciesInExhibit_TestClientPayload_ExpectSpecies', async () => {
   const originalGet = ConsoleOperationsClient.getOffDisplayAnimalOptions;
   const payloads = [];

   ConsoleOperationsClient.getOffDisplayAnimalOptions = async (payload) => {
      payloads.push(payload);
      return { species: ['Lion'] };
   };

   try {
      assert.deepEqual(
         await SpeciesProvider.fetchOffDisplaySpeciesInExhibit('Savanna'),
         ['Lion']
      );
      assert.deepEqual(payloads, [{ exhibit: 'Savanna' }]);
   } finally {
      ConsoleOperationsClient.getOffDisplayAnimalOptions = originalGet;
   }
});

test('Test_CreateOffDisplayAnimalSpeciesSource_TestLoaders_ExpectOffDisplayFetchers', async () => {
   const originalAll = SpeciesProvider.fetchOffDisplaySpecies;
   const originalExhibit = SpeciesProvider.fetchOffDisplaySpeciesInExhibit;
   const calls = [];

   SpeciesProvider.fetchOffDisplaySpecies = async () => {
      calls.push('all');
      return ['Lion'];
   };
   SpeciesProvider.fetchOffDisplaySpeciesInExhibit = async (exhibit) => {
      calls.push(exhibit);
      return ['Giraffe'];
   };

   try {
      const source = SpeciesProvider.createOffDisplayAnimalSpeciesSource();
      assert.deepEqual(await source.loadForExhibit(''), ['Lion']);
      assert.deepEqual(await source.loadForExhibit('Savanna'), ['Giraffe']);
      assert.deepEqual(calls, ['all', 'Savanna']);
   } finally {
      SpeciesProvider.fetchOffDisplaySpecies = originalAll;
      SpeciesProvider.fetchOffDisplaySpeciesInExhibit = originalExhibit;
   }
});

test('Test_FetchVisibilityScheduleSpecies_TestClientResult_ExpectSpecies', async () => {
   const originalGet = ConsoleOperationsClient.getAnimalVisibilityScheduleOptions;
   const payloads = [];

   ConsoleOperationsClient.getAnimalVisibilityScheduleOptions = async (payload) => {
      payloads.push(payload);
      return { species: ['Lion'] };
   };

   try {
      assert.deepEqual(await SpeciesProvider.fetchVisibilityScheduleSpecies(), ['Lion']);
      assert.deepEqual(payloads, [undefined]);
   } finally {
      ConsoleOperationsClient.getAnimalVisibilityScheduleOptions = originalGet;
   }
});

test('Test_FetchVisibilityScheduleSpeciesInExhibit_TestClientPayload_ExpectSpecies', async () => {
   const originalGet = ConsoleOperationsClient.getAnimalVisibilityScheduleOptions;
   const payloads = [];

   ConsoleOperationsClient.getAnimalVisibilityScheduleOptions = async (payload) => {
      payloads.push(payload);
      return { species: ['Lion'] };
   };

   try {
      assert.deepEqual(
         await SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit('Savanna'),
         ['Lion']
      );
      assert.deepEqual(payloads, [{ exhibit: 'Savanna' }]);
   } finally {
      ConsoleOperationsClient.getAnimalVisibilityScheduleOptions = originalGet;
   }
});

test('Test_CreateVisibilityScheduleAnimalSpeciesSource_TestLoaders_ExpectVisibilityScheduleFetchers', async () => {
   const originalAll = SpeciesProvider.fetchVisibilityScheduleSpecies;
   const originalExhibit = SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit;
   const calls = [];

   SpeciesProvider.fetchVisibilityScheduleSpecies = async () => {
      calls.push('all');
      return ['Lion'];
   };
   SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit = async (exhibit) => {
      calls.push(exhibit);
      return ['Giraffe'];
   };

   try {
      const source = SpeciesProvider.createVisibilityScheduleAnimalSpeciesSource();
      assert.deepEqual(await source.loadForExhibit(''), ['Lion']);
      assert.deepEqual(await source.loadForExhibit('Savanna'), ['Giraffe']);
      assert.deepEqual(calls, ['all', 'Savanna']);
   } finally {
      SpeciesProvider.fetchVisibilityScheduleSpecies = originalAll;
      SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit = originalExhibit;
   }
});

test('Test_FetchViewingAlertSpecies_TestClientResult_ExpectSpecies', async () => {
   const originalGet = ConsoleOperationsClient.getAnimalViewingAlertOptions;
   const payloads = [];

   ConsoleOperationsClient.getAnimalViewingAlertOptions = async (payload) => {
      payloads.push(payload);
      return { species: ['Lion'] };
   };

   try {
      assert.deepEqual(await SpeciesProvider.fetchViewingAlertSpecies(), ['Lion']);
      assert.deepEqual(payloads, [undefined]);
   } finally {
      ConsoleOperationsClient.getAnimalViewingAlertOptions = originalGet;
   }
});

test('Test_FetchViewingAlertSpeciesInExhibit_TestClientPayload_ExpectSpecies', async () => {
   const originalGet = ConsoleOperationsClient.getAnimalViewingAlertOptions;
   const payloads = [];

   ConsoleOperationsClient.getAnimalViewingAlertOptions = async (payload) => {
      payloads.push(payload);
      return { species: ['Lion'] };
   };

   try {
      assert.deepEqual(
         await SpeciesProvider.fetchViewingAlertSpeciesInExhibit('Savanna'),
         ['Lion']
      );
      assert.deepEqual(payloads, [{ exhibit: 'Savanna' }]);
   } finally {
      ConsoleOperationsClient.getAnimalViewingAlertOptions = originalGet;
   }
});

test('Test_CreateViewingAlertAnimalSpeciesSource_TestLoaders_ExpectViewingAlertFetchers', async () => {
   const originalAll = SpeciesProvider.fetchViewingAlertSpecies;
   const originalExhibit = SpeciesProvider.fetchViewingAlertSpeciesInExhibit;
   const calls = [];

   SpeciesProvider.fetchViewingAlertSpecies = async () => {
      calls.push('all');
      return ['Lion'];
   };
   SpeciesProvider.fetchViewingAlertSpeciesInExhibit = async (exhibit) => {
      calls.push(exhibit);
      return ['Giraffe'];
   };

   try {
      const source = SpeciesProvider.createViewingAlertAnimalSpeciesSource();
      assert.deepEqual(await source.loadForExhibit(''), ['Lion']);
      assert.deepEqual(await source.loadForExhibit('Savanna'), ['Giraffe']);
      assert.deepEqual(calls, ['all', 'Savanna']);
   } finally {
      SpeciesProvider.fetchViewingAlertSpecies = originalAll;
      SpeciesProvider.fetchViewingAlertSpeciesInExhibit = originalExhibit;
   }
});

