import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelectorModel } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';

const africanLionRow = {
   species: 'African Lion',
   exhibit: 'African Savanna',
   enclosure_type: 'Outdoor',
   likelihood: 75,
};

test('Test_GetAnimalEnclosureName_TestNullableNames_ExpectNormalized', () => {
   assert.equal(AnimalSelectorModel.getAnimalEnclosureName({ enclosure_name: 'Indoor' }), 'Indoor');
   assert.equal(AnimalSelectorModel.getAnimalEnclosureName({ enclosure_name: 'Outdoor' }), 'Outdoor');
   assert.equal(AnimalSelectorModel.getAnimalEnclosureName({ enclosure_name: 'White Rhino Viewing' }), 'White Rhino Viewing');
   assert.equal(AnimalSelectorModel.getAnimalEnclosureName({ enclosure_name: '  Savanna Overlook  ' }), 'Savanna Overlook');
   assert.equal(AnimalSelectorModel.getAnimalEnclosureName({ enclosure_name: null }), null);
   assert.equal(AnimalSelectorModel.getAnimalEnclosureName({ enclosure_name: '' }), null);
   assert.equal(AnimalSelectorModel.getAnimalEnclosureName({ enclosure_name: '   ' }), null);
   assert.equal(AnimalSelectorModel.getAnimalEnclosureName({}), null);
});

test('Test_GetAnimalId_TestPresentationFields_ExpectIdsSubtitlesAndImages', () => {
   assert.equal(
      AnimalSelectorModel.getAnimalId({
         species: 'Marabou Stork',
         exhibit: 'Africa Savanna',
         enclosure_name: 'White Rhino Viewing',
      }),
      'Marabou Stork||Africa Savanna||White Rhino Viewing'
   );
   assert.equal(AnimalSelectorModel.getAnimalId(africanLionRow), 'African Lion||African Savanna');
   assert.equal(AnimalSelectorModel.getAnimalTitleLine(africanLionRow), 'African Lion');
   assert.equal(AnimalSelectorModel.getAnimalSubtitle(africanLionRow), 'African Savanna');
   assert.equal(
      AnimalSelectorModel.getAnimalTitleLine({
         species: 'Marabou Stork',
         exhibit: 'Africa Savanna',
         enclosure_name: 'White Rhino Viewing',
         enclosure_type: 'Outdoor',
      }),
      'Marabou Stork \u2022 White Rhino Viewing'
   );
   assert.equal(
      AnimalSelectorModel.getAnimalSubtitle({
         species: 'Marabou Stork',
         exhibit: 'Africa Savanna',
         enclosure_name: 'White Rhino Viewing',
         enclosure_type: 'Outdoor',
      }),
      'Africa Savanna'
   );
   assert.equal(
      AnimalSelectorModel.getAnimalTitleLine({
         species: 'Red River Hog',
         exhibit: 'African Rainforest Pavilion',
         enclosure_type: 'Outdoor',
      }),
      'Red River Hog'
   );
   assert.equal(
      AnimalSelectorModel.getAnimalSubtitle({
         species: 'Red River Hog',
         exhibit: 'African Rainforest Pavilion',
         enclosure_type: 'Outdoor',
      }),
      'African Rainforest Pavilion'
   );
   assert.equal(
      AnimalSelectorModel.getAnimalTitleLine({
         species: 'Western Lowland Gorilla',
         exhibit: 'African Rainforest Pavilion',
         enclosure_name: 'Indoor',
         enclosure_type: 'Indoor',
      }),
      'Western Lowland Gorilla \u2022 Indoor'
   );
   assert.equal(
      AnimalSelectorModel.getAnimalSubtitle({
         species: 'Western Lowland Gorilla',
         exhibit: 'African Rainforest Pavilion',
         enclosure_name: 'Indoor',
         enclosure_type: 'Indoor',
      }),
      'African Rainforest Pavilion'
   );
   assert.equal(
      AnimalSelectorModel.buildAnimalImageSrc(africanLionRow),
      '../images/details/animals/african-savanna/african-lion.png'
   );
   assert.deepEqual(AnimalSelectorModel.makeAnimalSelection(africanLionRow), {
      id: 'African Lion||African Savanna',
      species: 'African Lion',
      exhibit: 'African Savanna',
      imageSrc: '../images/details/animals/african-savanna/african-lion.png',
   });
});

test('Test_GetAnimalLikelihoodLevel_TestThresholds_ExpectLevelsAndWarnings', () => {
   assert.equal(AnimalSelectorModel.getAnimalLikelihoodLevel({ likelihood: 20 }), 'low');
   assert.equal(AnimalSelectorModel.getAnimalLikelihoodLevel({ likelihood: 60 }), 'medium');
   assert.equal(AnimalSelectorModel.getAnimalLikelihoodLevel({ likelihood: 90 }), null);
   assert.equal(AnimalSelectorModel.isLikelyOffDisplayAnimal({ likelihood: 79 }), true);
   assert.equal(AnimalSelectorModel.isLikelyOffDisplayAnimal({ likelihood: 80 }), false);
   assert.equal(AnimalSelectorModel.OFF_DISPLAY_WARNING_THRESHOLD, 80);
});

test('Test_BuildOffDisplayWarningMessage_TestMissingAndLowLikelihood_ExpectMessages', () => {
   assert.match(
      AnimalSelectorModel.buildOffDisplayWarningMessage({ species: 'African Lion' }),
      /may be off display/
   );
   assert.match(
      AnimalSelectorModel.buildOffDisplayWarningMessage({ species: 'African Lion', likelihood: 55 }),
      /viewing likelihood below 80% \(55%\)/
   );
   assert.match(
      AnimalSelectorModel.buildOffDisplayWarningMessage({}),
      /This animal/
   );
});

test('Test_MigrateStoredAnimals_TestLegacyEntries_ExpectNormalized', () => {
   assert.deepEqual(
      AnimalSelectorModel.migrateStoredAnimals([
         'African Lion',
         {
            species: '  Amur Tiger  ',
            exhibit: 'Eurasia Wilds',
            image_src: ' ../images/tiger.png ',
         },
         {
            SPECIES: 'Red Panda',
            EXHIBIT: 'Indo-Malaya',
         },
      ]),
      [
         {
            id: 'African Lion||',
            species: 'African Lion',
            exhibit: '',
            imageSrc: null,
         },
         {
            id: 'Amur Tiger||Eurasia Wilds',
            species: 'Amur Tiger',
            exhibit: 'Eurasia Wilds',
            imageSrc: '../images/tiger.png',
         },
         {
            id: 'Red Panda||Indo-Malaya',
            species: 'Red Panda',
            exhibit: 'Indo-Malaya',
            imageSrc: null,
         },
      ]
   );
});
