import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalsClient } from '../../../../../scripts/api/animalsClient.js';
import { SpeciesProvider } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesProvider.js';
import { SpeciesSourceNormalizer } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesSourceNormalizer.js';


test('Test_NormalizeSpeciesList_TestDuplicatesAndWhitespace_ExpectUniqueSorted', () => {
   const amurTiger = 'Amur Tiger';
   const africanLion = 'African Lion';
   const values = [`  ${amurTiger}  `, africanLion, amurTiger, '', '  ', null];

   const species = SpeciesSourceNormalizer.normalizeSpeciesList(values);

   assert.deepEqual(species, [africanLion, amurTiger]);
});


test('Test_NormalizeSpeciesList_TestNull_ExpectEmpty', () => {
   const value = null;

   const species = SpeciesSourceNormalizer.normalizeSpeciesList(value);

   assert.deepEqual(species, []);
});


test('Test_NormalizeSpeciesList_TestUndefined_ExpectEmpty', () => {
   const value = undefined;

   const species = SpeciesSourceNormalizer.normalizeSpeciesList(value);

   assert.deepEqual(species, []);
});


test('Test_NormalizeExhibitKey_TestWhitespace_ExpectTrimmed', () => {
   const exhibit = 'African Rainforest Pavilion';
   const value = `  ${exhibit}  `;

   const key = SpeciesSourceNormalizer.normalizeExhibitKey(value);

   assert.equal(key, exhibit);
});


test('Test_NormalizeExhibitKey_TestNull_ExpectEmpty', () => {
   const value = null;

   const key = SpeciesSourceNormalizer.normalizeExhibitKey(value);

   assert.equal(key, '');
});


test('Test_NormalizeExhibitKey_TestUndefined_ExpectEmpty', () => {
   const value = undefined;

   const key = SpeciesSourceNormalizer.normalizeExhibitKey(value);

   assert.equal(key, '');
});


test('Test_NormalizeExhibitKey_TestBlank_ExpectEmpty', () => {
   const value = '   ';

   const key = SpeciesSourceNormalizer.normalizeExhibitKey(value);

   assert.equal(key, '');
});


test('Test_CreateAnimalSpeciesSource_TestLoadForExhibitUsesNormalizeExhibitKey_ExpectTrimmedExhibit', async () => {
   const exhibit = 'African Rainforest Pavilion';
   const value = `  ${exhibit}  `;
   const blackCrake = 'Black Crake';
   const yellowVentedBulbul = 'Yellow-Vented Bulbul';
   const animals = [blackCrake, yellowVentedBulbul];
   const originalAnimals = AnimalsClient.getAnimalsInExhibit;
   const exhibitsRequested = [];

   AnimalsClient.getAnimalsInExhibit = async (requestedExhibit) => {
      exhibitsRequested.push(requestedExhibit);
      return animals;
   };

   try {
      const source = SpeciesProvider.createAnimalSpeciesSource();

      const species = await source.loadForExhibit(value);

      assert.deepEqual(exhibitsRequested, [exhibit]);
      assert.deepEqual(species, animals);
   } finally {
      AnimalsClient.getAnimalsInExhibit = originalAnimals;
   }
});
