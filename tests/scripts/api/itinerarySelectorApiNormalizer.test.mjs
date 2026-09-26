import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySelectorApiNormalizer } from '../../../scripts/api/itinerarySelectorApiNormalizer.js';


test('Test_NormalizeRegion_TestExhibits_ExpectTrimmedNames', () => {
   const name = 'Americas';
   const mayanTemple = 'Mayan Temple';
   const australasiaPavilion = 'Australasia Pavilion';
   const region = {
      name: `  ${name}  `,
      exhibits: [`  ${mayanTemple}  `, '', `  ${australasiaPavilion}  `],
   };

   const normalized = ItinerarySelectorApiNormalizer.normalizeRegion(region);

   assert.deepEqual(normalized, {
      name,
      exhibits: [mayanTemple, australasiaPavilion],
   });
});


test('Test_NormalizeRegion_TestMissingExhibits_ExpectEmptyList', () => {
   const name = 'Eurasia';
   const region = { name };

   const normalized = ItinerarySelectorApiNormalizer.normalizeRegion(region);

   assert.deepEqual(normalized, { name, exhibits: [] });
});


test('Test_NormalizeAnimal_TestFields_ExpectTrimmedSpeciesAndExhibit', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const region = 'Africa';
   const animal = {
      species: `  ${species}  `,
      exhibit: `  ${exhibit}  `,
      region,
   };

   const normalized = ItinerarySelectorApiNormalizer.normalizeAnimal(animal);

   assert.deepEqual(normalized, {
      species,
      exhibit,
      region,
   });
});
