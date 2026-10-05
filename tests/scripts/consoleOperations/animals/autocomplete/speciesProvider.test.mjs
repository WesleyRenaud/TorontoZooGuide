import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalsClient } from '../../../../../scripts/api/animalsClient.js';
import { ConsoleOperationsClient } from '../../../../../scripts/api/consoleOperationsClient.js';
import { SpeciesProvider } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesProvider.js';
import { SpeciesSourceNormalizer } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesSourceNormalizer.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';


test('Test_CreateAnimalSpeciesSource_TestEmptyExhibit_ExpectCachedAllSpecies', async () => {
   const lion = 'Lion';
   const tiger = 'Tiger';
   const allSpecies = [lion, tiger];
   const originalLoad = ConsoleOptionsLoader.loadSpecies;
   const originalAnimals = AnimalsClient.getAnimalsInExhibit;
   const originalNormalizeList = SpeciesSourceNormalizer.normalizeSpeciesList;
   const originalNormalizeKey = SpeciesSourceNormalizer.normalizeExhibitKey;
   let speciesLoads = 0;

   ConsoleOptionsLoader.loadSpecies = async () => {
      speciesLoads += 1;
      return allSpecies;
   };
   AnimalsClient.getAnimalsInExhibit = async () => ['Giraffe'];
   SpeciesSourceNormalizer.normalizeSpeciesList = (list) => list;
   SpeciesSourceNormalizer.normalizeExhibitKey = (value) => value || '';

   try {
      const source = SpeciesProvider.createAnimalSpeciesSource();

      const first = await source.loadForExhibit('');
      const second = await source.loadForExhibit('');

      assert.deepEqual(first, allSpecies);
      assert.deepEqual(second, allSpecies);
      assert.equal(speciesLoads, 1);
   } finally {
      ConsoleOptionsLoader.loadSpecies = originalLoad;
      AnimalsClient.getAnimalsInExhibit = originalAnimals;
      SpeciesSourceNormalizer.normalizeSpeciesList = originalNormalizeList;
      SpeciesSourceNormalizer.normalizeExhibitKey = originalNormalizeKey;
   }
});


test('Test_CreateAnimalSpeciesSource_TestNamedExhibit_ExpectCachedExhibitSpecies', async () => {
   const giraffe = 'Giraffe';
   const exhibit = 'Savanna';
   const exhibitSpecies = [giraffe];
   const originalLoad = ConsoleOptionsLoader.loadSpecies;
   const originalAnimals = AnimalsClient.getAnimalsInExhibit;
   const originalNormalizeList = SpeciesSourceNormalizer.normalizeSpeciesList;
   const originalNormalizeKey = SpeciesSourceNormalizer.normalizeExhibitKey;
   let exhibitLoads = 0;

   ConsoleOptionsLoader.loadSpecies = async () => ['Lion', 'Tiger'];
   AnimalsClient.getAnimalsInExhibit = async () => {
      exhibitLoads += 1;
      return exhibitSpecies;
   };
   SpeciesSourceNormalizer.normalizeSpeciesList = (list) => list;
   SpeciesSourceNormalizer.normalizeExhibitKey = (value) => value || '';

   try {
      const source = SpeciesProvider.createAnimalSpeciesSource();

      const first = await source.loadForExhibit(exhibit);
      const second = await source.loadForExhibit(exhibit);

      assert.deepEqual(first, exhibitSpecies);
      assert.deepEqual(second, exhibitSpecies);
      assert.equal(exhibitLoads, 1);
   } finally {
      ConsoleOptionsLoader.loadSpecies = originalLoad;
      AnimalsClient.getAnimalsInExhibit = originalAnimals;
      SpeciesSourceNormalizer.normalizeSpeciesList = originalNormalizeList;
      SpeciesSourceNormalizer.normalizeExhibitKey = originalNormalizeKey;
   }
});


test('Test_CreateAnimalSpeciesSource_TestUncachedEmptyExhibit_ExpectRefetch', async () => {
   const lion = 'Lion';
   let allLoads = 0;

   const source = SpeciesProvider.createAnimalSpeciesSource({
      fetchAllSpecies: async () => {
         allLoads += 1;
         return [lion];
      },
      fetchSpeciesForExhibit: async () => [],
      cacheLists: false,
   });

   const first = await source.loadForExhibit('');
   const second = await source.loadForExhibit('');

   assert.deepEqual(first, [lion]);
   assert.deepEqual(second, [lion]);
   assert.equal(allLoads, 2);
});


test('Test_CreateAnimalSpeciesSource_TestUncachedExhibitUndefined_ExpectEmpty', async () => {
   const exhibit = 'Savanna';

   const source = SpeciesProvider.createAnimalSpeciesSource({
      fetchAllSpecies: async () => ['Lion'],
      fetchSpeciesForExhibit: async (requestedExhibit) => {
         assert.equal(requestedExhibit, exhibit);
         return undefined;
      },
      cacheLists: false,
   });

   const species = await source.loadForExhibit(exhibit);

   assert.deepEqual(species, []);
});


test('Test_CreateAnimalSpeciesSource_TestUncachedExhibit_ExpectNormalizedSpecies', async () => {
   const exhibit = 'Savanna';
   const giraffe = 'Giraffe';

   const source = SpeciesProvider.createAnimalSpeciesSource({
      fetchAllSpecies: async () => ['Lion'],
      fetchSpeciesForExhibit: async (requestedExhibit) => {
         assert.equal(requestedExhibit, exhibit);
         return [null, giraffe];
      },
      cacheLists: false,
   });

   const species = await source.loadForExhibit(exhibit);

   assert.deepEqual(species, [giraffe]);
});


test('Test_FetchOffDisplaySpecies_TestClientResult_ExpectSpecies', async () => {
   const lion = 'Lion';
   const originalGet = ConsoleOperationsClient.getOffDisplayAnimalOptions;
   const payloads = [];

   ConsoleOperationsClient.getOffDisplayAnimalOptions = async (payload) => {
      payloads.push(payload);
      return { species: [lion] };
   };

   try {
      const species = await SpeciesProvider.fetchOffDisplaySpecies();

      assert.deepEqual(species, [lion]);
      assert.deepEqual(payloads, [undefined]);
   } finally {
      ConsoleOperationsClient.getOffDisplayAnimalOptions = originalGet;
   }
});


test('Test_FetchOffDisplaySpeciesInExhibit_TestClientPayload_ExpectSpecies', async () => {
   const lion = 'Lion';
   const exhibit = 'Savanna';
   const originalGet = ConsoleOperationsClient.getOffDisplayAnimalOptions;
   const payloads = [];

   ConsoleOperationsClient.getOffDisplayAnimalOptions = async (payload) => {
      payloads.push(payload);
      return { species: [lion] };
   };

   try {
      const species = await SpeciesProvider.fetchOffDisplaySpeciesInExhibit(exhibit);

      assert.deepEqual(species, [lion]);
      assert.deepEqual(payloads, [{ exhibit }]);
   } finally {
      ConsoleOperationsClient.getOffDisplayAnimalOptions = originalGet;
   }
});


test('Test_CreateOffDisplayAnimalSpeciesSource_TestEmptyExhibit_ExpectAllSpecies', async () => {
   const lion = 'Lion';
   const originalAll = SpeciesProvider.fetchOffDisplaySpecies;
   const originalExhibit = SpeciesProvider.fetchOffDisplaySpeciesInExhibit;
   const calls = [];

   SpeciesProvider.fetchOffDisplaySpecies = async () => {
      calls.push('all');
      return [lion];
   };
   SpeciesProvider.fetchOffDisplaySpeciesInExhibit = async () => [];

   try {
      const source = SpeciesProvider.createOffDisplayAnimalSpeciesSource();

      const species = await source.loadForExhibit('');

      assert.deepEqual(species, [lion]);
      assert.deepEqual(calls, ['all']);
   } finally {
      SpeciesProvider.fetchOffDisplaySpecies = originalAll;
      SpeciesProvider.fetchOffDisplaySpeciesInExhibit = originalExhibit;
   }
});


test('Test_CreateOffDisplayAnimalSpeciesSource_TestExhibit_ExpectExhibitSpecies', async () => {
   const giraffe = 'Giraffe';
   const exhibit = 'Savanna';
   const originalAll = SpeciesProvider.fetchOffDisplaySpecies;
   const originalExhibit = SpeciesProvider.fetchOffDisplaySpeciesInExhibit;
   const calls = [];

   SpeciesProvider.fetchOffDisplaySpecies = async () => [];
   SpeciesProvider.fetchOffDisplaySpeciesInExhibit = async (requestedExhibit) => {
      calls.push(requestedExhibit);
      return [giraffe];
   };

   try {
      const source = SpeciesProvider.createOffDisplayAnimalSpeciesSource();

      const species = await source.loadForExhibit(exhibit);

      assert.deepEqual(species, [giraffe]);
      assert.deepEqual(calls, [exhibit]);
   } finally {
      SpeciesProvider.fetchOffDisplaySpecies = originalAll;
      SpeciesProvider.fetchOffDisplaySpeciesInExhibit = originalExhibit;
   }
});


test('Test_FetchVisibilityScheduleSpecies_TestClientResult_ExpectSpecies', async () => {
   const lion = 'Lion';
   const originalGet = ConsoleOperationsClient.getAnimalVisibilityScheduleOptions;
   const payloads = [];

   ConsoleOperationsClient.getAnimalVisibilityScheduleOptions = async (payload) => {
      payloads.push(payload);
      return { species: [lion] };
   };

   try {
      const species = await SpeciesProvider.fetchVisibilityScheduleSpecies();

      assert.deepEqual(species, [lion]);
      assert.deepEqual(payloads, [undefined]);
   } finally {
      ConsoleOperationsClient.getAnimalVisibilityScheduleOptions = originalGet;
   }
});


test('Test_FetchVisibilityScheduleSpeciesInExhibit_TestClientPayload_ExpectSpecies', async () => {
   const lion = 'Lion';
   const exhibit = 'Savanna';
   const originalGet = ConsoleOperationsClient.getAnimalVisibilityScheduleOptions;
   const payloads = [];

   ConsoleOperationsClient.getAnimalVisibilityScheduleOptions = async (payload) => {
      payloads.push(payload);
      return { species: [lion] };
   };

   try {
      const species = await SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit(exhibit);

      assert.deepEqual(species, [lion]);
      assert.deepEqual(payloads, [{ exhibit }]);
   } finally {
      ConsoleOperationsClient.getAnimalVisibilityScheduleOptions = originalGet;
   }
});


test('Test_CreateVisibilityScheduleAnimalSpeciesSource_TestEmptyExhibit_ExpectAllSpecies', async () => {
   const lion = 'Lion';
   const originalAll = SpeciesProvider.fetchVisibilityScheduleSpecies;
   const originalExhibit = SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit;
   const calls = [];

   SpeciesProvider.fetchVisibilityScheduleSpecies = async () => {
      calls.push('all');
      return [lion];
   };
   SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit = async () => [];

   try {
      const source = SpeciesProvider.createVisibilityScheduleAnimalSpeciesSource();

      const species = await source.loadForExhibit('');

      assert.deepEqual(species, [lion]);
      assert.deepEqual(calls, ['all']);
   } finally {
      SpeciesProvider.fetchVisibilityScheduleSpecies = originalAll;
      SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit = originalExhibit;
   }
});


test('Test_CreateVisibilityScheduleAnimalSpeciesSource_TestExhibit_ExpectExhibitSpecies', async () => {
   const giraffe = 'Giraffe';
   const exhibit = 'Savanna';
   const originalAll = SpeciesProvider.fetchVisibilityScheduleSpecies;
   const originalExhibit = SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit;
   const calls = [];

   SpeciesProvider.fetchVisibilityScheduleSpecies = async () => [];
   SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit = async (requestedExhibit) => {
      calls.push(requestedExhibit);
      return [giraffe];
   };

   try {
      const source = SpeciesProvider.createVisibilityScheduleAnimalSpeciesSource();

      const species = await source.loadForExhibit(exhibit);

      assert.deepEqual(species, [giraffe]);
      assert.deepEqual(calls, [exhibit]);
   } finally {
      SpeciesProvider.fetchVisibilityScheduleSpecies = originalAll;
      SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit = originalExhibit;
   }
});


test('Test_FetchViewingAlertSpecies_TestClientResult_ExpectSpecies', async () => {
   const lion = 'Lion';
   const originalGet = ConsoleOperationsClient.getAnimalViewingAlertOptions;
   const payloads = [];

   ConsoleOperationsClient.getAnimalViewingAlertOptions = async (payload) => {
      payloads.push(payload);
      return { species: [lion] };
   };

   try {
      const species = await SpeciesProvider.fetchViewingAlertSpecies();

      assert.deepEqual(species, [lion]);
      assert.deepEqual(payloads, [undefined]);
   } finally {
      ConsoleOperationsClient.getAnimalViewingAlertOptions = originalGet;
   }
});


test('Test_FetchViewingAlertSpeciesInExhibit_TestClientPayload_ExpectSpecies', async () => {
   const lion = 'Lion';
   const exhibit = 'Savanna';
   const originalGet = ConsoleOperationsClient.getAnimalViewingAlertOptions;
   const payloads = [];

   ConsoleOperationsClient.getAnimalViewingAlertOptions = async (payload) => {
      payloads.push(payload);
      return { species: [lion] };
   };

   try {
      const species = await SpeciesProvider.fetchViewingAlertSpeciesInExhibit(exhibit);

      assert.deepEqual(species, [lion]);
      assert.deepEqual(payloads, [{ exhibit }]);
   } finally {
      ConsoleOperationsClient.getAnimalViewingAlertOptions = originalGet;
   }
});


test('Test_CreateViewingAlertAnimalSpeciesSource_TestEmptyExhibit_ExpectAllSpecies', async () => {
   const lion = 'Lion';
   const originalAll = SpeciesProvider.fetchViewingAlertSpecies;
   const originalExhibit = SpeciesProvider.fetchViewingAlertSpeciesInExhibit;
   const calls = [];

   SpeciesProvider.fetchViewingAlertSpecies = async () => {
      calls.push('all');
      return [lion];
   };
   SpeciesProvider.fetchViewingAlertSpeciesInExhibit = async () => [];

   try {
      const source = SpeciesProvider.createViewingAlertAnimalSpeciesSource();

      const species = await source.loadForExhibit('');

      assert.deepEqual(species, [lion]);
      assert.deepEqual(calls, ['all']);
   } finally {
      SpeciesProvider.fetchViewingAlertSpecies = originalAll;
      SpeciesProvider.fetchViewingAlertSpeciesInExhibit = originalExhibit;
   }
});


test('Test_CreateViewingAlertAnimalSpeciesSource_TestExhibit_ExpectExhibitSpecies', async () => {
   const giraffe = 'Giraffe';
   const exhibit = 'Savanna';
   const originalAll = SpeciesProvider.fetchViewingAlertSpecies;
   const originalExhibit = SpeciesProvider.fetchViewingAlertSpeciesInExhibit;
   const calls = [];

   SpeciesProvider.fetchViewingAlertSpecies = async () => [];
   SpeciesProvider.fetchViewingAlertSpeciesInExhibit = async (requestedExhibit) => {
      calls.push(requestedExhibit);
      return [giraffe];
   };

   try {
      const source = SpeciesProvider.createViewingAlertAnimalSpeciesSource();

      const species = await source.loadForExhibit(exhibit);

      assert.deepEqual(species, [giraffe]);
      assert.deepEqual(calls, [exhibit]);
   } finally {
      SpeciesProvider.fetchViewingAlertSpecies = originalAll;
      SpeciesProvider.fetchViewingAlertSpeciesInExhibit = originalExhibit;
   }
});


test('Test_FetchOffDisplayForSeasonSpecies_TestClientPayload_ExpectSeasonOnlyPayload', async (t) => {
   const stork = 'Marabou Stork';
   const originalGet = ConsoleOperationsClient.getOffDisplayAnimalOptions;
   const payloads = [];
   t.after(() => {
      ConsoleOperationsClient.getOffDisplayAnimalOptions = originalGet;
   });
   ConsoleOperationsClient.getOffDisplayAnimalOptions = async (payload) => {
      payloads.push(payload);
      return { species: [stork] };
   };

   const species = await SpeciesProvider.fetchOffDisplayForSeasonSpecies();

   assert.deepEqual(species, [stork]);
   assert.deepEqual(payloads, [{ forSeasonOnly: true }]);
});


test('Test_FetchOffDisplayForSeasonSpeciesInExhibit_TestClientPayload_ExpectSeasonOnlyPayload', async (t) => {
   const stork = 'Marabou Stork';
   const exhibit = 'Africa Savanna';
   const originalGet = ConsoleOperationsClient.getOffDisplayAnimalOptions;
   const payloads = [];
   t.after(() => {
      ConsoleOperationsClient.getOffDisplayAnimalOptions = originalGet;
   });
   ConsoleOperationsClient.getOffDisplayAnimalOptions = async (payload) => {
      payloads.push(payload);
      return { species: [stork] };
   };

   const species = await SpeciesProvider.fetchOffDisplayForSeasonSpeciesInExhibit(exhibit);

   assert.deepEqual(species, [stork]);
   assert.deepEqual(payloads, [{ exhibit, forSeasonOnly: true }]);
});


test('Test_CreateOffDisplayForSeasonAnimalSpeciesSource_TestExhibit_ExpectSeasonFetchers', async (t) => {
   const stork = 'Marabou Stork';
   const vulture = 'White-Headed Vulture';
   const exhibit = 'Africa Savanna';
   const originalAll = SpeciesProvider.fetchOffDisplayForSeasonSpecies;
   const originalExhibit = SpeciesProvider.fetchOffDisplayForSeasonSpeciesInExhibit;
   const calls = [];
   t.after(() => {
      SpeciesProvider.fetchOffDisplayForSeasonSpecies = originalAll;
      SpeciesProvider.fetchOffDisplayForSeasonSpeciesInExhibit = originalExhibit;
   });
   SpeciesProvider.fetchOffDisplayForSeasonSpecies = async () => {
      calls.push('all');
      return [vulture];
   };
   SpeciesProvider.fetchOffDisplayForSeasonSpeciesInExhibit = async (requestedExhibit) => {
      calls.push(requestedExhibit);
      return [stork];
   };
   const source = SpeciesProvider.createOffDisplayForSeasonAnimalSpeciesSource();

   const allSpecies = await source.loadForExhibit('');
   const exhibitSpecies = await source.loadForExhibit(exhibit);

   assert.deepEqual(allSpecies, [vulture]);
   assert.deepEqual(exhibitSpecies, [stork]);
   assert.deepEqual(calls, ['all', exhibit]);
});
