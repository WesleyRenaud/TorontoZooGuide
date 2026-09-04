import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalIdentity } from '../../../scripts/itinerary/animalIdentity.js';

test('Test_NormalizeAnimalIdentityFields_TestWhitespace_ExpectTrimmed', () => {
   assert.deepEqual(
      AnimalIdentity.normalizeAnimalIdentityFields({
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
      AnimalIdentity.normalizeAnimalIdentityFields({
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

test('Test_BuildAnimalIdentityComparisonKey_TestFields_ExpectLowercaseKey', () => {
   assert.equal(
      AnimalIdentity.buildAnimalIdentityComparisonKey({
         species: ' Masai Giraffe ',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Giraffe House',
      }),
      'masai giraffe||africa savanna||giraffe house'
   );
});

test('Test_BuildAnimalIdentityStorageKey_TestFields_ExpectLowercaseKey', () => {
   assert.equal(
      AnimalIdentity.buildAnimalIdentityStorageKey({
         species: 'African Penguin',
         exhibit: 'Africa Savanna',
         enclosure_name: 'Outdoor',
      }),
      'african penguin||africa savanna||outdoor'
   );
   assert.equal(
      AnimalIdentity.buildAnimalIdentityStorageKey({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      'african lion||africa savanna'
   );
});

test('Test_NormalizeAnimalForSave_TestInvalidAndBlank_ExpectFiltered', () => {
   assert.deepEqual(
      AnimalIdentity.normalizeAnimalForSave({
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
   assert.equal(AnimalIdentity.normalizeAnimalForSave({ species: '  ', exhibit: 'Africa Savanna' }), null);
   assert.deepEqual(
      AnimalIdentity.normalizeAnimalForSave({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }
   );
});
