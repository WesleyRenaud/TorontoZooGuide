import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesExhibitKeyHelper } from '../../../scripts/itinerary/speciesExhibitKeyHelper.js';
import { EnclosureType } from '../../../scripts/shared/enums/enclosureType.js';


test('Test_BuildViewingSpotSuffix_TestEnclosureName_ExpectLowercaseName', () => {
   const enclosureName = 'White Rhino Viewing';
   const animal = { enclosure_name: `  ${enclosureName}  ` };

   const suffix = SpeciesExhibitKeyHelper.buildViewingSpotSuffix(animal);

   assert.equal(suffix, enclosureName.toLowerCase());
});


test('Test_BuildViewingSpotSuffix_TestEnclosureTypeFallback_ExpectLowercaseType', () => {
   const animal = { enclosure_type: EnclosureType.INDOOR };

   const suffix = SpeciesExhibitKeyHelper.buildViewingSpotSuffix(animal);

   assert.equal(suffix, EnclosureType.INDOOR.toLowerCase());
});


test('Test_BuildViewingSpotSuffix_TestMissing_ExpectEmpty', () => {
   const animal = {};

   const suffix = SpeciesExhibitKeyHelper.buildViewingSpotSuffix(animal);

   assert.equal(suffix, '');
});
