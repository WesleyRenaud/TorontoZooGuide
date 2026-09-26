import assert from 'node:assert/strict';
import { test } from 'node:test';

import { AnimalDisplayFormatter } from '../../../scripts/animals/animalDisplayFormatter.js';
import { TimelineLayoutConstants } from '../../../scripts/shared/timelineLayoutConstants.js';


test('Test_FormatSpeciesEnclosureLine_TestNullEnclosure_ExpectSpeciesOnly', () => {
   const species = 'Marabou Stork';
   const enclosureName = null;

   const line = AnimalDisplayFormatter.formatSpeciesEnclosureLine(species, enclosureName);

   assert.equal(line, species);
});


test('Test_FormatSpeciesEnclosureLine_TestBlankEnclosure_ExpectSpeciesOnly', () => {
   const species = 'Marabou Stork';
   const enclosureName = '';

   const line = AnimalDisplayFormatter.formatSpeciesEnclosureLine(species, enclosureName);

   assert.equal(line, species);
});


test('Test_FormatSpeciesEnclosureLine_TestEnclosureName_ExpectJoined', () => {
   const species = 'Marabou Stork';
   const enclosureName = 'White Rhino Viewing';

   const line = AnimalDisplayFormatter.formatSpeciesEnclosureLine(species, enclosureName);

   assert.equal(line, `${species}${TimelineLayoutConstants.DETAIL_SEPARATOR}${enclosureName}`);
});


test('Test_FormatSpeciesEnclosureLine_TestIndoorEnclosure_ExpectJoined', () => {
   const species = 'Golden Lion Tamarin';
   const enclosureName = 'Indoor';

   const line = AnimalDisplayFormatter.formatSpeciesEnclosureLine(species, enclosureName);

   assert.equal(line, `${species}${TimelineLayoutConstants.DETAIL_SEPARATOR}${enclosureName}`);
});


test('Test_FormatExhibitEnclosureTypeLine_TestIndoor_ExpectJoined', () => {
   const exhibit = 'Americas Pavilion';
   const enclosureType = 'Indoor';

   const line = AnimalDisplayFormatter.formatExhibitEnclosureTypeLine(exhibit, enclosureType);

   assert.equal(line, `${exhibit}${TimelineLayoutConstants.DETAIL_SEPARATOR}${enclosureType}`);
});


test('Test_FormatExhibitEnclosureTypeLine_TestOutdoor_ExpectJoined', () => {
   const exhibit = 'Africa Savanna';
   const enclosureType = 'Outdoor';

   const line = AnimalDisplayFormatter.formatExhibitEnclosureTypeLine(exhibit, enclosureType);

   assert.equal(line, `${exhibit}${TimelineLayoutConstants.DETAIL_SEPARATOR}${enclosureType}`);
});


test('Test_FormatExhibitEnclosureTypeLine_TestAviary_ExpectJoined', () => {
   const exhibit = 'Africa Savanna';
   const enclosureType = 'Aviary';

   const line = AnimalDisplayFormatter.formatExhibitEnclosureTypeLine(exhibit, enclosureType);

   assert.equal(line, `${exhibit}${TimelineLayoutConstants.DETAIL_SEPARATOR}${enclosureType}`);
});


test('Test_FormatExhibitEnclosureTypeLine_TestBlankType_ExpectExhibitOnly', () => {
   const exhibit = 'Africa Savanna';
   const enclosureType = '';

   const line = AnimalDisplayFormatter.formatExhibitEnclosureTypeLine(exhibit, enclosureType);

   assert.equal(line, exhibit);
});


test('Test_FormatExhibitEnclosureTypeLine_TestNullType_ExpectExhibitOnly', () => {
   const exhibit = 'Africa Savanna';
   const enclosureType = null;

   const line = AnimalDisplayFormatter.formatExhibitEnclosureTypeLine(exhibit, enclosureType);

   assert.equal(line, exhibit);
});


test('Test_FormatAnimalTitleSuffix_TestBlank_ExpectEmpty', () => {
   const enclosureName = '';

   const suffix = AnimalDisplayFormatter.formatAnimalTitleSuffix(enclosureName);

   assert.equal(suffix, enclosureName);
});


test('Test_FormatAnimalTitleSuffix_TestIndoor_ExpectSuffix', () => {
   const enclosureName = 'Indoor';

   const suffix = AnimalDisplayFormatter.formatAnimalTitleSuffix(enclosureName);

   assert.equal(suffix, `${TimelineLayoutConstants.DETAIL_SEPARATOR}${enclosureName}`);
});
