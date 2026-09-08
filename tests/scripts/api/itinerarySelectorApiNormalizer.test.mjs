import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySelectorApiNormalizer } from '../../../scripts/api/itinerarySelectorApiNormalizer.js';

test('Test_NormalizeRegion_TestExhibits_ExpectTrimmedNames', () => {
   assert.deepEqual(
      ItinerarySelectorApiNormalizer.normalizeRegion({
         name: '  Americas  ',
         exhibits: ['  Mayan Temple  ', '', '  Australasia Pavilion  '],
      }),
      {
         name: 'Americas',
         exhibits: ['Mayan Temple', 'Australasia Pavilion'],
      }
   );
});

test('Test_NormalizeRegion_TestMissingExhibits_ExpectEmptyList', () => {
   assert.deepEqual(
      ItinerarySelectorApiNormalizer.normalizeRegion({ name: 'Eurasia' }),
      { name: 'Eurasia', exhibits: [] }
   );
});

test('Test_NormalizeAnimal_TestFields_ExpectTrimmedSpeciesAndExhibit', () => {
   assert.deepEqual(
      ItinerarySelectorApiNormalizer.normalizeAnimal({
         species: '  African Lion  ',
         exhibit: '  African Savanna  ',
         region: 'Africa',
      }),
      {
         species: 'African Lion',
         exhibit: 'African Savanna',
         region: 'Africa',
      }
   );
});
