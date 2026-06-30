import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildAnimalIdentityComparisonKey,
   buildAnimalIdentityStorageKey,
   normalizeAnimalForSave,
   normalizeAnimalIdentityFields,
} from '../../scripts/itinerary/animalIdentity.js';

test('normalizeAnimalIdentityFields trims species, exhibit, and enclosure name', () => {
   assert.deepEqual(
      normalizeAnimalIdentityFields({
         species: '  African Lion  ',
         exhibit: ' Africa Savanna ',
         enclosure_name: '  Giraffe House  ',
      }),
      {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Giraffe House',
      }
   );
   assert.deepEqual(
      normalizeAnimalIdentityFields({
         species: 'African Penguin',
         exhibit: 'Africa Savanna',
         enclosure_name: '   ',
      }),
      {
         species: 'African Penguin',
         exhibit: 'Africa Savanna',
         enclosure_name: null,
      }
   );
});

test('buildAnimalIdentityComparisonKey lowercases identity fields for sorting', () => {
   assert.equal(
      buildAnimalIdentityComparisonKey({
         species: ' Masai Giraffe ',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Giraffe House',
      }),
      'masai giraffe||africa savanna||giraffe house'
   );
});

test('buildAnimalIdentityStorageKey builds lowercase draft removal keys', () => {
   assert.equal(
      buildAnimalIdentityStorageKey({
         species: 'African Penguin',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Outdoor',
      }),
      'african penguin||africa savanna||outdoor'
   );
   assert.equal(
      buildAnimalIdentityStorageKey({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      'african lion||africa savanna'
   );
});

test('normalizeAnimalForSave drops invalid rows and omits blank enclosure names', () => {
   assert.deepEqual(
      normalizeAnimalForSave({
         species: 'Masai Giraffe',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Outdoor',
      }),
      {
         species: 'Masai Giraffe',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Outdoor',
      }
   );
   assert.equal(normalizeAnimalForSave({ species: '  ', exhibit: 'Africa Savanna' }), null);
   assert.deepEqual(
      normalizeAnimalForSave({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }
   );
});
