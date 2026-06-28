import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildAnimalImageSrc,
   buildOffDisplayWarningMessage,
   getAnimalEnclosureName,
   getAnimalId,
   getAnimalLikelihoodLevel,
   getAnimalSubtitle,
   getAnimalTitleLine,
   isLikelyOffDisplayAnimal,
   makeAnimalSelection,
   migrateStoredAnimals,
   OFF_DISPLAY_WARNING_THRESHOLD,
} from '../../scripts/itinerary/selectors/animalSelector/model.js';

const africanLionRow = {
   species: 'African Lion',
   exhibit: 'African Savanna',
   enclosure_type: 'Outdoor',
   likelihood: 75,
};

test('getAnimalEnclosureName omits indoor and outdoor viewing spot names', () => {
   assert.equal(getAnimalEnclosureName({ enclosure_name: 'Indoor' }), null);
   assert.equal(getAnimalEnclosureName({ enclosure_name: 'Outdoor' }), null);
   assert.equal(getAnimalEnclosureName({ enclosure_name: 'White Rhino Viewing' }), 'White Rhino Viewing');
});

test('getAnimalEnclosureName normalizes nullable enclosure names', () => {
   assert.equal(getAnimalEnclosureName({ enclosure_name: 'White Rhino Viewing' }), 'White Rhino Viewing');
   assert.equal(getAnimalEnclosureName({ enclosure_name: '  Savanna Overlook  ' }), 'Savanna Overlook');
   assert.equal(getAnimalEnclosureName({ enclosure_name: null }), null);
   assert.equal(getAnimalEnclosureName({ enclosure_name: '' }), null);
   assert.equal(getAnimalEnclosureName({ enclosure_name: '   ' }), null);
   assert.equal(getAnimalEnclosureName({}), null);
});

test('animal selector model derives ids, subtitles, and image paths', () => {
   assert.equal(getAnimalId(africanLionRow), 'African Lion||African Savanna');
   assert.equal(getAnimalTitleLine(africanLionRow), 'African Lion');
   assert.equal(getAnimalSubtitle(africanLionRow), 'African Savanna');
   assert.equal(
      getAnimalTitleLine({
         species: 'Marabou Stork',
         exhibit: 'Africa Savanna',
         enclosure_name: 'White Rhino Viewing',
         enclosure_type: 'Outdoor',
      }),
      'Marabou Stork \u2022 White Rhino Viewing'
   );
   assert.equal(
      buildAnimalImageSrc(africanLionRow),
      '../images/details/animals/african-savanna/african-lion.png'
   );
   assert.deepEqual(makeAnimalSelection(africanLionRow), {
      id: 'African Lion||African Savanna',
      species: 'African Lion',
      exhibit: 'African Savanna',
      imageSrc: '../images/details/animals/african-savanna/african-lion.png',
   });
});

test('animal selector model classifies likelihood levels and off-display warnings', () => {
   assert.equal(getAnimalLikelihoodLevel({ likelihood: 20 }), 'low');
   assert.equal(getAnimalLikelihoodLevel({ likelihood: 60 }), 'medium');
   assert.equal(getAnimalLikelihoodLevel({ likelihood: 90 }), null);
   assert.equal(isLikelyOffDisplayAnimal({ likelihood: 79 }), true);
   assert.equal(isLikelyOffDisplayAnimal({ likelihood: 80 }), false);
   assert.equal(OFF_DISPLAY_WARNING_THRESHOLD, 80);
});

test('buildOffDisplayWarningMessage handles missing and low likelihood values', () => {
   assert.match(
      buildOffDisplayWarningMessage({ species: 'African Lion' }),
      /may be off display/
   );
   assert.match(
      buildOffDisplayWarningMessage({ species: 'African Lion', likelihood: 55 }),
      /viewing likelihood below 80% \(55%\)/
   );
   assert.match(
      buildOffDisplayWarningMessage({}),
      /This animal/
   );
});

test('migrateStoredAnimals normalizes legacy string and object entries', () => {
   assert.deepEqual(
      migrateStoredAnimals([
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
