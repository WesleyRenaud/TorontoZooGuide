import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesSourceNormalizer } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesSourceNormalizer.js';

test('Test_NormalizeSpeciesList_TestDuplicatesAndWhitespace_ExpectUniqueSorted', () => {
   assert.deepEqual(
      SpeciesSourceNormalizer.normalizeSpeciesList([
         '  Amur Tiger  ',
         'African Lion',
         'Amur Tiger',
         '',
         '  ',
         null,
      ]),
      ['African Lion', 'Amur Tiger']
   );
});

test('Test_NormalizeSpeciesList_TestMissingList_ExpectEmpty', () => {
   assert.deepEqual(SpeciesSourceNormalizer.normalizeSpeciesList(null), []);
   assert.deepEqual(SpeciesSourceNormalizer.normalizeSpeciesList(undefined), []);
});

test('Test_NormalizeExhibitKey_TestWhitespace_ExpectTrimmed', () => {
   assert.equal(
      SpeciesSourceNormalizer.normalizeExhibitKey('  African Rainforest Pavilion  '),
      'African Rainforest Pavilion'
   );
});

test('Test_NormalizeExhibitKey_TestMissing_ExpectEmpty', () => {
   assert.equal(SpeciesSourceNormalizer.normalizeExhibitKey(null), '');
   assert.equal(SpeciesSourceNormalizer.normalizeExhibitKey(undefined), '');
   assert.equal(SpeciesSourceNormalizer.normalizeExhibitKey('   '), '');
});

test('Test_CreateAnimalSpeciesSource_TestLoadForExhibitUsesNormalizeExhibitKey', async () => {
   const { SpeciesProvider } = await import(
      '../../../../../scripts/consoleOperations/animals/autocomplete/speciesProvider.js'
   );
   const { AnimalsClient } = await import('../../../../../scripts/api/animalsClient.js');

   const originalAnimals = AnimalsClient.getAnimalsInExhibit;
   const exhibitsRequested = [];

   AnimalsClient.getAnimalsInExhibit = async (exhibit) => {
      exhibitsRequested.push(exhibit);
      return ['Black Crake', 'Yellow-Vented Bulbul'];
   };

   try {
      const source = SpeciesProvider.createAnimalSpeciesSource();
      const species = await source.loadForExhibit('  African Rainforest Pavilion  ');
      assert.deepEqual(exhibitsRequested, ['African Rainforest Pavilion']);
      assert.deepEqual(species, ['Black Crake', 'Yellow-Vented Bulbul']);
   } finally {
      AnimalsClient.getAnimalsInExhibit = originalAnimals;
   }
});
