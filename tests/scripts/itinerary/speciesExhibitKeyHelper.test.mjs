import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesExhibitKeyHelper } from '../../../scripts/itinerary/speciesExhibitKeyHelper.js';
import { EnclosureType } from '../../../scripts/shared/enums/enclosureType.js';

test('Test_BuildViewingSpotSuffix_TestEnclosureName_ExpectLowercaseName', () => {
   assert.equal(
      SpeciesExhibitKeyHelper.buildViewingSpotSuffix({ enclosure_name: '  White Rhino Viewing  ' }),
      'white rhino viewing'
   );
});

test('Test_BuildViewingSpotSuffix_TestEnclosureTypeFallback_ExpectLowercaseType', () => {
   assert.equal(
      SpeciesExhibitKeyHelper.buildViewingSpotSuffix({ enclosure_type: EnclosureType.INDOOR }),
      'indoor'
   );
});

test('Test_BuildViewingSpotSuffix_TestMissing_ExpectEmpty', () => {
   assert.equal(SpeciesExhibitKeyHelper.buildViewingSpotSuffix({}), '');
});
