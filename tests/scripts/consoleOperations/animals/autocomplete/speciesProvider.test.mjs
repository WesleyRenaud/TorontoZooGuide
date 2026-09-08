import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesProvider } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesProvider.js';
import { ConsoleOptionsLoader } from '../../../../../scripts/consoleOperations/options/consoleOptionsLoader.js';
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
