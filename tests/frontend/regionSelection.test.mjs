import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildSelectedAnimalKey,
   getExhibitNamesFromAnimals,
   mergeAnimals,
   normalizeSelectedAnimal,
   omitRemovedAnimals,
   shouldHideDuplicateSingleExhibit,
} from '../../scripts/itinerary/selectors/regionSelector/regionSelection.js';

test('getExhibitNamesFromAnimals dedupes exhibits from normalized animals', () => {
   assert.deepEqual(
      getExhibitNamesFromAnimals([
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'African Penguin', exhibit: 'Africa Savanna' },
         { species: 'Amur Tiger', exhibit: 'Eurasia Wilds' },
      ]),
      ['Africa Savanna', 'Eurasia Wilds']
   );
});

test('omitRemovedAnimals filters animals by normalized removal keys', () => {
   const animals = [
      { species: 'African Lion', exhibit: 'Africa Savanna' },
      { species: 'African Penguin', exhibit: 'Africa Savanna' },
   ];
   const removedKeys = new Set(['african penguin||africa savanna']);

   assert.deepEqual(
      omitRemovedAnimals(animals, removedKeys).map((animal) => animal.species),
      ['African Lion']
   );
});

test('buildSelectedAnimalKey prefers explicit animal ids', () => {
   assert.equal(
      buildSelectedAnimalKey({
         id: 'Custom-Id',
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      'custom-id'
   );
});

test('normalizeSelectedAnimal synthesizes ids from species and exhibit', () => {
   const normalized = normalizeSelectedAnimal({
      species: 'African Lion',
      exhibit: 'Africa Savanna',
   });

   assert.equal(normalized.id, 'African Lion||Africa Savanna');
   assert.equal(normalized.imageSrc, null);
});

test('mergeAnimals dedupes by selected animal key', () => {
   const merged = mergeAnimals(
      [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      [
         { species: 'African Lion', exhibit: 'Africa Savanna' },
         { species: 'African Penguin', exhibit: 'Africa Savanna' },
      ]
   );

   assert.deepEqual(
      merged.map((animal) => animal.species).sort(),
      ['African Lion', 'African Penguin']
   );
});

test('shouldHideDuplicateSingleExhibit hides lone exhibit rows that mirror the region name', () => {
   assert.equal(
      shouldHideDuplicateSingleExhibit({
         name: 'Americas',
         exhibits: ['Americas'],
      }),
      true
   );
   assert.equal(
      shouldHideDuplicateSingleExhibit({
         name: 'Africa',
         exhibits: ['Africa Savanna', 'Africa Rainforest'],
      }),
      false
   );
});
