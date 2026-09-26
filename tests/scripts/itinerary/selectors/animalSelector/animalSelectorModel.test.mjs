import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalSelectorModel } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorModel.js';
import { AnimalSelectorStoredAnimalFactory } from '../../../../../scripts/itinerary/selectors/animalSelector/animalSelectorStoredAnimalFactory.js';
import { AnimalDisplayFormatter } from '../../../../../scripts/animals/animalDisplayFormatter.js';
import { AssetKeyNormalizer } from '../../../../../scripts/assets/assetKeyNormalizer.js';
import { ScheduleItemKeySeparator } from '../../../../../scripts/itinerary/scheduleItemKeySeparator.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';


test('Test_GetAnimalEnclosureName_TestIndoor_ExpectName', () => {
   const enclosureName = 'Indoor';
   const row = { enclosure_name: enclosureName };

   const name = AnimalSelectorModel.getAnimalEnclosureName(row);

   assert.equal(name, enclosureName);
});


test('Test_GetAnimalEnclosureName_TestOutdoor_ExpectName', () => {
   const enclosureName = 'Outdoor';
   const row = { enclosure_name: enclosureName };

   const name = AnimalSelectorModel.getAnimalEnclosureName(row);

   assert.equal(name, enclosureName);
});


test('Test_GetAnimalEnclosureName_TestViewing_ExpectName', () => {
   const enclosureName = 'White Rhino Viewing';
   const row = { enclosure_name: enclosureName };

   const name = AnimalSelectorModel.getAnimalEnclosureName(row);

   assert.equal(name, enclosureName);
});


test('Test_GetAnimalEnclosureName_TestWhitespace_ExpectTrimmed', () => {
   const enclosureName = 'Savanna Overlook';
   const row = { enclosure_name: `  ${enclosureName}  ` };

   const name = AnimalSelectorModel.getAnimalEnclosureName(row);

   assert.equal(name, enclosureName);
});


test('Test_GetAnimalEnclosureName_TestNull_ExpectNull', () => {
   const row = { enclosure_name: null };

   const name = AnimalSelectorModel.getAnimalEnclosureName(row);

   assert.equal(name, null);
});


test('Test_GetAnimalEnclosureName_TestEmpty_ExpectNull', () => {
   const row = { enclosure_name: '' };

   const name = AnimalSelectorModel.getAnimalEnclosureName(row);

   assert.equal(name, null);
});


test('Test_GetAnimalEnclosureName_TestBlank_ExpectNull', () => {
   const row = { enclosure_name: '   ' };

   const name = AnimalSelectorModel.getAnimalEnclosureName(row);

   assert.equal(name, null);
});


test('Test_GetAnimalEnclosureName_TestMissing_ExpectNull', () => {
   const row = {};

   const name = AnimalSelectorModel.getAnimalEnclosureName(row);

   assert.equal(name, null);
});


test('Test_GetAnimalId_TestSpeciesExhibitAndEnclosure_ExpectJoined', () => {
   const species = 'Marabou Stork';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'White Rhino Viewing';
   const row = { species, exhibit, enclosure_name: enclosureName };

   const animalId = AnimalSelectorModel.getAnimalId(row);

   assert.equal(animalId, [species, exhibit, enclosureName].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_GetAnimalId_TestSpeciesAndExhibit_ExpectJoined', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const row = { species, exhibit };

   const animalId = AnimalSelectorModel.getAnimalId(row);

   assert.equal(animalId, [species, exhibit].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_GetAnimalTitleLine_TestSpeciesOnly_ExpectSpecies', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const row = { species, exhibit };

   const title = AnimalSelectorModel.getAnimalTitleLine(row);

   assert.equal(title, species);
});


test('Test_GetAnimalSubtitle_TestExhibit_ExpectExhibit', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const row = { species, exhibit };

   const subtitle = AnimalSelectorModel.getAnimalSubtitle(row);

   assert.equal(subtitle, exhibit);
});


test('Test_GetAnimalTitleLine_TestEnclosure_ExpectSpeciesAndEnclosure', () => {
   const species = 'Marabou Stork';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'White Rhino Viewing';
   const row = {
      species,
      exhibit,
      enclosure_name: enclosureName,
      enclosure_type: 'Outdoor',
   };

   const title = AnimalSelectorModel.getAnimalTitleLine(row);

   assert.equal(title, AnimalDisplayFormatter.formatSpeciesEnclosureLine(species, enclosureName));
});


test('Test_GetAnimalSubtitle_TestEnclosureRow_ExpectExhibit', () => {
   const species = 'Marabou Stork';
   const exhibit = 'Africa Savanna';
   const enclosureName = 'White Rhino Viewing';
   const row = {
      species,
      exhibit,
      enclosure_name: enclosureName,
      enclosure_type: 'Outdoor',
   };

   const subtitle = AnimalSelectorModel.getAnimalSubtitle(row);

   assert.equal(subtitle, exhibit);
});


test('Test_GetAnimalTitleLine_TestOutdoorWithoutEnclosure_ExpectSpecies', () => {
   const species = 'Red River Hog';
   const exhibit = 'African Rainforest Pavilion';
   const row = {
      species,
      exhibit,
      enclosure_type: 'Outdoor',
   };

   const title = AnimalSelectorModel.getAnimalTitleLine(row);

   assert.equal(title, species);
});


test('Test_GetAnimalSubtitle_TestOutdoorWithoutEnclosure_ExpectExhibit', () => {
   const species = 'Red River Hog';
   const exhibit = 'African Rainforest Pavilion';
   const row = {
      species,
      exhibit,
      enclosure_type: 'Outdoor',
   };

   const subtitle = AnimalSelectorModel.getAnimalSubtitle(row);

   assert.equal(subtitle, exhibit);
});


test('Test_GetAnimalTitleLine_TestIndoorEnclosure_ExpectSpeciesAndEnclosure', () => {
   const species = 'Western Lowland Gorilla';
   const exhibit = 'African Rainforest Pavilion';
   const enclosureName = 'Indoor';
   const row = {
      species,
      exhibit,
      enclosure_name: enclosureName,
      enclosure_type: enclosureName,
   };

   const title = AnimalSelectorModel.getAnimalTitleLine(row);

   assert.equal(title, AnimalDisplayFormatter.formatSpeciesEnclosureLine(species, enclosureName));
});


test('Test_GetAnimalSubtitle_TestIndoorEnclosure_ExpectExhibit', () => {
   const species = 'Western Lowland Gorilla';
   const exhibit = 'African Rainforest Pavilion';
   const enclosureName = 'Indoor';
   const row = {
      species,
      exhibit,
      enclosure_name: enclosureName,
      enclosure_type: enclosureName,
   };

   const subtitle = AnimalSelectorModel.getAnimalSubtitle(row);

   assert.equal(subtitle, exhibit);
});


test('Test_BuildAnimalImageSrc_TestSpeciesAndExhibit_ExpectPath', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const row = { species, exhibit, enclosure_type: 'Outdoor', likelihood: 75 };

   const imageSrc = AnimalSelectorModel.buildAnimalImageSrc(row);

   assert.equal(
      imageSrc,
      `../images/details/animals/${AssetKeyNormalizer.normalize(exhibit)}/${AssetKeyNormalizer.normalize(species)}.png`
   );
});


test('Test_MakeAnimalSelection_TestRow_ExpectSelection', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const row = { species, exhibit, enclosure_type: 'Outdoor', likelihood: 75 };

   const selection = AnimalSelectorModel.makeAnimalSelection(row);

   assert.equal(selection.id, AnimalSelectorModel.getAnimalId(row));
   assert.equal(selection.species, species);
   assert.equal(selection.exhibit, exhibit);
   assert.equal(selection.imageSrc, AnimalSelectorModel.buildAnimalImageSrc(row));
});


test('Test_GetAnimalLikelihoodLevel_TestLow_ExpectLow', () => {
   const likelihood = 20;
   const row = { likelihood };

   const level = AnimalSelectorModel.getAnimalLikelihoodLevel(row);

   assert.equal(level, 'low');
});


test('Test_GetAnimalLikelihoodLevel_TestMedium_ExpectMedium', () => {
   const likelihood = 60;
   const row = { likelihood };

   const level = AnimalSelectorModel.getAnimalLikelihoodLevel(row);

   assert.equal(level, 'medium');
});


test('Test_GetAnimalLikelihoodLevel_TestHigh_ExpectNull', () => {
   const likelihood = 90;
   const row = { likelihood };

   const level = AnimalSelectorModel.getAnimalLikelihoodLevel(row);

   assert.equal(level, null);
});


test('Test_GetAnimalLikelihoodLevel_TestNonNumeric_ExpectNull', () => {
   const likelihood = 'na';
   const row = { likelihood };

   const level = AnimalSelectorModel.getAnimalLikelihoodLevel(row);

   assert.equal(level, null);
});


test('Test_IsLikelyOffDisplayAnimal_TestBelowThreshold_ExpectTrue', () => {
   const likelihood = AnimalSelectorModel.OFF_DISPLAY_WARNING_THRESHOLD - 1;
   const row = { likelihood };

   const isOffDisplay = AnimalSelectorModel.isLikelyOffDisplayAnimal(row);

   assert.equal(isOffDisplay, true);
});


test('Test_IsLikelyOffDisplayAnimal_TestAtThreshold_ExpectFalse', () => {
   const likelihood = AnimalSelectorModel.OFF_DISPLAY_WARNING_THRESHOLD;
   const row = { likelihood };

   const isOffDisplay = AnimalSelectorModel.isLikelyOffDisplayAnimal(row);

   assert.equal(isOffDisplay, false);
});


test('Test_GetAnimalEnclosureType_TestOutdoor_ExpectType', () => {
   const enclosureType = 'Outdoor';
   const row = { species: 'African Lion', exhibit: 'African Savanna', enclosure_type: enclosureType };

   const type = AnimalSelectorModel.getAnimalEnclosureType(row);

   assert.equal(type, enclosureType);
});


test('Test_GetAnimalEnclosureType_TestUnknown_ExpectEmpty', () => {
   const row = { enclosure_type: 'Unknown' };

   const type = AnimalSelectorModel.getAnimalEnclosureType(row);

   assert.equal(type, '');
});


test('Test_BuildAnimalImageSrc_TestMissingSpecies_ExpectNull', () => {
   const exhibit = 'Africa';
   const row = { species: '', exhibit };

   const imageSrc = AnimalSelectorModel.buildAnimalImageSrc(row);

   assert.equal(imageSrc, null);
});


test('Test_BuildOffDisplayWarningMessage_TestUnknownLikelihood_ExpectUnknownCopy', () => {
   const species = 'African Lion';
   const row = { species, likelihood: 'na' };

   const message = AnimalSelectorModel.buildOffDisplayWarningMessage(row);

   assert.equal(
      message,
      Strings.itinerary.confirmation.animalOffDisplayUnknownLikelihoodMessage(species)
   );
});


test('Test_BuildOffDisplayWarningMessage_TestMissingLikelihood_ExpectZeroPercentCopy', () => {
   const species = 'African Lion';
   const row = { species };

   const message = AnimalSelectorModel.buildOffDisplayWarningMessage(row);

   assert.equal(
      message,
      Strings.itinerary.confirmation.animalOffDisplayLowLikelihoodMessage(
         species,
         AnimalSelectorModel.OFF_DISPLAY_WARNING_THRESHOLD,
         AnimalSelectorModel.getAnimalLikelihood(row)
      )
   );
});


test('Test_BuildOffDisplayWarningMessage_TestLowLikelihood_ExpectPercentCopy', () => {
   const species = 'African Lion';
   const likelihood = 55;
   const row = { species, likelihood };

   const message = AnimalSelectorModel.buildOffDisplayWarningMessage(row);

   assert.equal(
      message,
      Strings.itinerary.confirmation.animalOffDisplayLowLikelihoodMessage(
         species,
         AnimalSelectorModel.OFF_DISPLAY_WARNING_THRESHOLD,
         likelihood
      )
   );
});


test('Test_BuildOffDisplayWarningMessage_TestMissingSpecies_ExpectFallback', () => {
   const row = {};

   const message = AnimalSelectorModel.buildOffDisplayWarningMessage(row);

   assert.match(message, new RegExp(Strings.itinerary.confirmation.animalFallbackName));
});


test('Test_MigrateStoredAnimals_TestLegacyEntries_ExpectNormalized', () => {
   const lion = 'African Lion';
   const tiger = 'Amur Tiger';
   const tigerExhibit = 'Eurasia Wilds';
   const tigerImage = '../images/tiger.png';
   const panda = 'Red Panda';
   const pandaExhibit = 'Indo-Malaya';
   const items = [
      lion,
      {
         species: `  ${tiger}  `,
         exhibit: tigerExhibit,
         image_src: ` ${tigerImage} `,
      },
      {
         SPECIES: panda,
         EXHIBIT: pandaExhibit,
      },
   ];

   const migrated = AnimalSelectorModel.migrateStoredAnimals(items);

   assert.deepEqual(
      migrated.at(Position.FIRST),
      AnimalSelectorStoredAnimalFactory.createStoredAnimalFromString(lion)
   );
   assert.deepEqual(
      migrated.at(Position.SECOND),
      AnimalSelectorStoredAnimalFactory.createStoredAnimalFromObject({
         species: tiger,
         exhibit: tigerExhibit,
         image_src: tigerImage,
      })
   );
   assert.deepEqual(
      migrated.at(Position.THIRD),
      AnimalSelectorStoredAnimalFactory.createStoredAnimalFromObject({
         SPECIES: panda,
         EXHIBIT: pandaExhibit,
      })
   );
});
