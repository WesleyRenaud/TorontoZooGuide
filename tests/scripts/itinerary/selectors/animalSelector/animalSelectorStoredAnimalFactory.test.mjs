import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelectorStoredAnimalFactory } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorStoredAnimalFactory.js';

test('Test_NormalizeLegacyStoredFields_TestCasing_ExpectNormalized', () => {
   assert.equal(
      AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredSpecies({ SPECIES: 'African Lion' }),
      'African Lion'
   );
   assert.equal(
      AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredExhibit({ EXHIBIT: 'Savanna' }),
      'Savanna'
   );
   assert.equal(
      AnimalSelectorStoredAnimalFactory.normalizeLegacyStoredImageSrc({ image: 'lion.png' }),
      'lion.png'
   );
});

test('Test_CreateStoredAnimalFromString_TestSpecies_ExpectStoredOrNull', () => {
   assert.equal(AnimalSelectorStoredAnimalFactory.createStoredAnimalFromString(''), null);
   assert.deepEqual(AnimalSelectorStoredAnimalFactory.createStoredAnimalFromString('African Lion'), {
      id: 'African Lion||',
      species: 'African Lion',
      exhibit: '',
      imageSrc: null,
   });
});

test('Test_CreateStoredAnimalFromObject_TestFields_ExpectStored', () => {
   assert.deepEqual(
      AnimalSelectorStoredAnimalFactory.createStoredAnimalFromObject({
         species: 'African Lion',
         exhibit: 'Savanna',
         enclosure_name: 'Overlook',
         imageSrc: 'lion.png',
      }),
      {
         id: 'African Lion||Savanna||Overlook',
         species: 'African Lion',
         exhibit: 'Savanna',
         enclosure_name: 'Overlook',
         imageSrc: 'lion.png',
      }
   );
});

test('Test_CreateStoredAnimalFromObject_TestMissingId_ExpectNull', async () => {
   const { StoredSelectionNormalizer } = await import(
      '../../../../../scripts/itinerary/selectors/base/storedSelectionNormalizer.js'
   );
   const originalNormalize = StoredSelectionNormalizer.normalizeStoredId;
   StoredSelectionNormalizer.normalizeStoredId = () => '';

   try {
      assert.equal(
         AnimalSelectorStoredAnimalFactory.createStoredAnimalFromObject({
            species: 'African Lion',
            exhibit: 'Savanna',
         }),
         null
      );
   } finally {
      StoredSelectionNormalizer.normalizeStoredId = originalNormalize;
   }
});
