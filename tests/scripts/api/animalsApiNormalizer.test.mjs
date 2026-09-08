import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalsApiNormalizer } from '../../../scripts/api/animalsApiNormalizer.js';
import { AnimalViewingModel } from '../../../scripts/shared/enums/animalViewingModel.js';

test('Test_NormalizeNamedList_TestValues_ExpectTrimmedNonEmpty', () => {
   assert.deepEqual(
      AnimalsApiNormalizer.normalizeNamedList(['  Lion  ', '', 'Tiger', null]),
      ['Lion', 'Tiger']
   );
});

test('Test_NormalizeRegion_TestFields_ExpectNormalized', () => {
   assert.deepEqual(
      AnimalsApiNormalizer.normalizeRegion({ name: '  Africa  ', hasExhibits: true }),
      { name: 'Africa', hasExhibits: true }
   );
});

test('Test_NormalizeRegionsResponse_TestRegions_ExpectNamedOnly', () => {
   assert.deepEqual(
      AnimalsApiNormalizer.normalizeRegionsResponse({
         regions: [
            { name: '  Africa  ', hasExhibits: true },
            { name: '', hasExhibits: false },
         ],
      }),
      [{ name: 'Africa', hasExhibits: true }]
   );
});

test('Test_NormalizeAnimalsResponse_TestAnimals_ExpectNamedList', () => {
   assert.deepEqual(
      AnimalsApiNormalizer.normalizeAnimalsResponse({ animals: ['  Lion  ', ''] }),
      ['Lion']
   );
});

test('Test_NormalizeAnimalViewingScopesResponse_TestValidAndInvalid_ExpectFiltered', () => {
   assert.deepEqual(
      AnimalsApiNormalizer.normalizeAnimalViewingScopesResponse({
         viewingScopes: [
            AnimalViewingModel.ALL,
            'not-a-scope',
            AnimalViewingModel.INDOOR,
         ],
      }),
      [AnimalViewingModel.ALL, AnimalViewingModel.INDOOR]
   );
});

test('Test_NormalizeAnimalInformationResponse_TestFirstValid_ExpectAnimalOrNull', () => {
   assert.equal(
      AnimalsApiNormalizer.normalizeAnimalInformationResponse({ information: [] }),
      null
   );

   const animal = AnimalsApiNormalizer.normalizeAnimalInformationResponse({
      information: [{
         species: '  African Lion  ',
         exhibit: '  African Savanna  ',
         latin_name: '  Panthera leo  ',
      }],
   });

   assert.equal(animal.species, 'African Lion');
   assert.equal(animal.exhibit, 'African Savanna');
   assert.equal(animal.latin_name, 'Panthera leo');
});
