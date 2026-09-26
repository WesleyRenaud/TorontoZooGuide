import assert from 'node:assert/strict';
import { test } from 'node:test';

import { SpeciesExhibitKey } from '../../../scripts/itinerary/speciesExhibitKey.js';
import { EnclosureType } from '../../../scripts/shared/enums/enclosureType.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_BuildSpeciesExhibitKey_TestNormalizedFields_ExpectJoinedKey', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const animal = {
      species: `  ${species}  `,
      exhibit: ` ${exhibit} `,
   };

   const key = SpeciesExhibitKey.buildSpeciesExhibitKey(animal);

   assert.equal(key, `${species.toLowerCase()}|${exhibit.toLowerCase()}`);
});


test('Test_BuildSpeciesExhibitKey_TestMissingExhibit_ExpectEmpty', () => {
   const animal = { species: 'Amur Tiger' };

   const key = SpeciesExhibitKey.buildSpeciesExhibitKey(animal);

   assert.equal(key, '');
});


test('Test_BuildSpeciesExhibitKey_TestExhibitNotRequired_ExpectSpeciesKey', () => {
   const species = 'Amur Tiger';
   const animal = { species };

   const key = SpeciesExhibitKey.buildSpeciesExhibitKey(animal, { requireExhibit: false });

   assert.equal(key, `${species.toLowerCase()}|`);
});


test('Test_BuildAnimalViewingSpotKey_TestEnclosureName_ExpectSuffix', () => {
   const species = 'Masai Giraffe';
   const exhibit = 'African Savanna';
   const enclosureName = 'Giraffe House';
   const animal = {
      species,
      exhibit,
      enclosure_name: enclosureName,
   };

   const key = SpeciesExhibitKey.buildAnimalViewingSpotKey(animal);

   assert.equal(
      key,
      `${species.toLowerCase()}|${exhibit.toLowerCase()}|${enclosureName.toLowerCase()}`
   );
});


test('Test_BuildAnimalViewingSpotKey_TestEnclosureType_ExpectSuffix', () => {
   const species = 'Masai Giraffe';
   const exhibit = 'African Savanna';
   const animal = {
      species,
      exhibit,
      enclosure_type: EnclosureType.INDOOR,
   };

   const key = SpeciesExhibitKey.buildAnimalViewingSpotKey(animal);

   assert.equal(
      key,
      `${species.toLowerCase()}|${exhibit.toLowerCase()}|${EnclosureType.INDOOR.toLowerCase()}`
   );
});


test('Test_BuildAnimalViewingSpotKey_TestEmptySpecies_ExpectEmpty', () => {
   const animal = { species: '' };

   const key = SpeciesExhibitKey.buildAnimalViewingSpotKey(animal);

   assert.equal(key, '');
});


test('Test_BuildAnimalViewingSpotKey_TestSpeciesAndExhibit_ExpectJoinedKey', () => {
   const species = 'Masai Giraffe';
   const exhibit = 'African Savanna';
   const animal = { species, exhibit };

   const key = SpeciesExhibitKey.buildAnimalViewingSpotKey(animal);

   assert.equal(key, `${species.toLowerCase()}|${exhibit.toLowerCase()}`);
});


test('Test_BuildUniqueSpeciesExhibitEntries_TestDuplicates_ExpectMerged', () => {
   const lion = 'African Lion';
   const exhibit = 'Africa Savanna';
   const zebra = 'Grant\'s Zebra';
   const lowerLikelihood = 0.4;
   const higherLikelihood = 0.8;
   const animals = [
      { species: lion, exhibit, likelihood: lowerLikelihood },
      { species: lion, exhibit, likelihood: higherLikelihood },
      { species: zebra, exhibit },
      { species: 'Missing' },
   ];

   const entries = SpeciesExhibitKey.buildUniqueSpeciesExhibitEntries(
      animals,
      {
         mergeAnimals: (existing, animal) => ({
            ...existing,
            likelihood: Math.max(existing.likelihood ?? 0, animal.likelihood ?? 0),
         }),
      }
   );

   assert.equal(entries.length, 2);
   assert.equal(entries[Position.FIRST].item.likelihood, higherLikelihood);
   assert.equal(entries[Position.SECOND].item.species, zebra);
});


test('Test_BuildUniqueSpeciesExhibitEntries_TestFiltered_ExpectEmpty', () => {
   const animals = [{ species: 'African Lion', exhibit: 'Africa Savanna' }];

   const filtered = SpeciesExhibitKey.buildUniqueSpeciesExhibitEntries(
      animals,
      { includeAnimal: () => false }
   );

   assert.deepEqual(filtered, []);
});
