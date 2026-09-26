import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelectorStoredAnimalFactory } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorStoredAnimalFactory.js';
import { StoredSelectionNormalizer } from '../../../../../scripts/itinerary/selectors/base/storedSelectionNormalizer.js';
import { ScheduleItemKeySeparator } from '../../../../../scripts/itinerary/scheduleItemKeySeparator.js';


test('Test_NormalizeLegacyStoredSpecies_TestUppercaseField_ExpectNormalized', () => {
   const species = 'African Lion';
   const item = { SPECIES: species };

   const normalized = AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredSpecies(item);

   assert.equal(normalized, species);
});


test('Test_NormalizeLegacyStoredExhibit_TestUppercaseField_ExpectNormalized', () => {
   const exhibit = 'Savanna';
   const item = { EXHIBIT: exhibit };

   const normalized = AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredExhibit(item);

   assert.equal(normalized, exhibit);
});


test('Test_NormalizeLegacyStoredImageSrc_TestImageField_ExpectNormalized', () => {
   const image = 'lion.png';
   const item = { image };

   const normalized = AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredImageSrc(item);

   assert.equal(normalized, image);
});


test('Test_CreateStoredAnimalFromString_TestEmpty_ExpectNull', () => {
   const value = '';

   const stored = AnimalSelectorStoredAnimalFactory.createStoredAnimalFromString(value);

   assert.equal(stored, null);
});


test('Test_CreateStoredAnimalFromString_TestSpecies_ExpectStored', () => {
   const species = 'African Lion';

   const stored = AnimalSelectorStoredAnimalFactory.createStoredAnimalFromString(species);

   assert.equal(stored.species, species);
   assert.equal(stored.exhibit, '');
   assert.equal(stored.imageSrc, null);
   assert.equal(stored.id, `${species}${ScheduleItemKeySeparator.VALUE}`);
});


test('Test_CreateStoredAnimalFromObject_TestFields_ExpectStored', () => {
   const species = 'African Lion';
   const exhibit = 'Savanna';
   const enclosureName = 'Overlook';
   const imageSrc = 'lion.png';
   const item = {
      species,
      exhibit,
      enclosure_name: enclosureName,
      imageSrc,
   };

   const stored = AnimalSelectorStoredAnimalFactory.createStoredAnimalFromObject(item);

   assert.equal(stored.species, species);
   assert.equal(stored.exhibit, exhibit);
   assert.equal(stored.enclosure_name, enclosureName);
   assert.equal(stored.imageSrc, imageSrc);
   assert.equal(
      stored.id,
      [species, exhibit, enclosureName].join(ScheduleItemKeySeparator.VALUE)
   );
});


test('Test_CreateStoredAnimalFromObject_TestMissingId_ExpectNull', () => {
   const originalNormalize = StoredSelectionNormalizer.normalizeStoredId;
   StoredSelectionNormalizer.normalizeStoredId = () => '';
   const species = 'African Lion';
   const exhibit = 'Savanna';
   const item = { species, exhibit };

   try {
      const stored = AnimalSelectorStoredAnimalFactory.createStoredAnimalFromObject(item);

      assert.equal(stored, null);
   } finally {
      StoredSelectionNormalizer.normalizeStoredId = originalNormalize;
   }
});
