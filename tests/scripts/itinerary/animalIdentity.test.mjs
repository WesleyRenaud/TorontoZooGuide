import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalIdentity } from '../../../scripts/itinerary/animalIdentity.js';
import { ScheduleItemKeySeparator } from '../../../scripts/itinerary/scheduleItemKeySeparator.js';


test('Test_NormalizeAnimalIdentityFields_TestWhitespace_ExpectTrimmed', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'Giraffe House';
   const animal = {
      species: `  ${species}  `,
      exhibit: ` ${exhibit} `,
      enclosure_name: `  ${enclosureName}  `,
   };

   const normalized = AnimalIdentity.normalizeAnimalIdentityFields(animal);

   assert.deepEqual(normalized, {
      species,
      exhibit,
      enclosure_name: enclosureName,
   });
});


test('Test_NormalizeAnimalIdentityFields_TestBlankEnclosure_ExpectNull', () => {
   const species = 'African Penguin';
   const exhibit = 'Africa Savanna';
   const animal = {
      species,
      exhibit,
      enclosure_name: '   ',
   };

   const normalized = AnimalIdentity.normalizeAnimalIdentityFields(animal);

   assert.deepEqual(normalized, {
      species,
      exhibit,
      enclosure_name: null,
   });
});


test('Test_BuildAnimalIdentityComparisonKey_TestFields_ExpectLowercaseKey', () => {
   const species = 'Masai Giraffe';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'Giraffe House';
   const animal = {
      species: ` ${species} `,
      exhibit,
      enclosure_name: enclosureName,
   };

   const key = AnimalIdentity.buildAnimalIdentityComparisonKey(animal);

   assert.equal(
      key,
      [species.toLowerCase(), exhibit.toLowerCase(), enclosureName.toLowerCase()]
         .join(ScheduleItemKeySeparator.VALUE)
   );
});


test('Test_BuildAnimalIdentityStorageKey_TestFields_ExpectLowercaseKey', () => {
   const species = 'African Penguin';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'Outdoor';
   const animal = {
      species,
      exhibit,
      enclosure_name: enclosureName,
   };

   const key = AnimalIdentity.buildAnimalIdentityStorageKey(animal);

   assert.equal(
      key,
      [species.toLowerCase(), exhibit.toLowerCase(), enclosureName.toLowerCase()]
         .join(ScheduleItemKeySeparator.VALUE)
   );
});


test('Test_BuildAnimalIdentityStorageKey_TestMissingEnclosure_ExpectSpeciesAndExhibit', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const animal = { species, exhibit };

   const key = AnimalIdentity.buildAnimalIdentityStorageKey(animal);

   assert.equal(
      key,
      [species.toLowerCase(), exhibit.toLowerCase()].join(ScheduleItemKeySeparator.VALUE)
   );
});


test('Test_NormalizeAnimalForSave_TestValid_ExpectNormalized', () => {
   const species = 'Masai Giraffe';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'Outdoor';
   const animal = {
      species,
      exhibit,
      enclosure_name: enclosureName,
   };

   const normalized = AnimalIdentity.normalizeAnimalForSave(animal);

   assert.deepEqual(normalized, {
      species,
      exhibit,
      enclosure_name: enclosureName,
   });
});


test('Test_NormalizeAnimalForSave_TestBlankSpecies_ExpectNull', () => {
   const animal = { species: '  ', exhibit: 'Africa Savanna' };

   const normalized = AnimalIdentity.normalizeAnimalForSave(animal);

   assert.equal(normalized, null);
});


test('Test_NormalizeAnimalForSave_TestNull_ExpectNull', () => {
   const animal = null;

   const normalized = AnimalIdentity.normalizeAnimalForSave(animal);

   assert.equal(normalized, null);
});


test('Test_NormalizeAnimalForSave_TestString_ExpectNull', () => {
   const animal = 'lion';

   const normalized = AnimalIdentity.normalizeAnimalForSave(animal);

   assert.equal(normalized, null);
});


test('Test_NormalizeAnimalForSave_TestSpeciesAndExhibit_ExpectNormalized', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const animal = { species, exhibit };

   const normalized = AnimalIdentity.normalizeAnimalForSave(animal);

   assert.deepEqual(normalized, { species, exhibit });
});


test('Test_BuildAnimalIdentityStorageKey_TestMissingSpecies_ExpectEmpty', () => {
   const animal = {
      species: '  ',
      exhibit: 'Africa Savanna',
   };

   const key = AnimalIdentity.buildAnimalIdentityStorageKey(animal);

   assert.equal(key, '');
});
