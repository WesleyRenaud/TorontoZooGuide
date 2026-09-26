import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalsApiNormalizer } from '../../../scripts/api/animalsApiNormalizer.js';


test('Test_NormalizeNamedList_TestValues_ExpectTrimmedNonEmpty', () => {
   const lion = 'Lion';
   const tiger = 'Tiger';
   const values = [`  ${lion}  `, '', tiger, null];

   const names = AnimalsApiNormalizer.normalizeNamedList(values);

   assert.deepEqual(names, [lion, tiger]);
});


test('Test_NormalizeRegion_TestFields_ExpectNormalized', () => {
   const name = 'Africa';
   const hasExhibits = true;
   const region = { name: `  ${name}  `, hasExhibits };

   const normalized = AnimalsApiNormalizer.normalizeRegion(region);

   assert.deepEqual(normalized, { name, hasExhibits });
});


test('Test_NormalizeRegionsResponse_TestRegions_ExpectNamedOnly', () => {
   const name = 'Africa';
   const hasExhibits = true;
   const response = {
      regions: [
         { name: `  ${name}  `, hasExhibits },
         { name: '', hasExhibits: false },
      ],
   };

   const regions = AnimalsApiNormalizer.normalizeRegionsResponse(response);

   assert.deepEqual(regions, [{ name, hasExhibits }]);
});


test('Test_NormalizeAnimalsResponse_TestAnimals_ExpectNamedList', () => {
   const species = 'Lion';
   const response = { animals: [`  ${species}  `, ''] };

   const animals = AnimalsApiNormalizer.normalizeAnimalsResponse(response);

   assert.deepEqual(animals, [species]);
});


test('Test_NormalizeAnimalInformationResponse_TestEmpty_ExpectNull', () => {
   const response = { information: [] };

   const animal = AnimalsApiNormalizer.normalizeAnimalInformationResponse(response);

   assert.equal(animal, null);
});


test('Test_NormalizeAnimalInformationResponse_TestFirstValid_ExpectAnimal', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const latinName = 'Panthera leo';
   const row = {
      species: `  ${species}  `,
      exhibit: `  ${exhibit}  `,
      latin_name: `  ${latinName}  `,
   };

   const animal = AnimalsApiNormalizer.normalizeAnimalInformationResponse({
      information: [row],
   });

   assert.equal(animal.species, species);
   assert.equal(animal.exhibit, exhibit);
   assert.equal(animal.latin_name, latinName);
});
