import assert from 'node:assert/strict';
import { test } from 'node:test';

import { AnimalDisplayLines } from '../../../scripts/animals/animalDisplayLines.js';

test('Test_FormatSpeciesEnclosureLine_TestOmitsSeparatorWhenEnclosureNameIsBlank_ExpectOk', () => {
   assert.equal(AnimalDisplayLines.formatSpeciesEnclosureLine('Marabou Stork', null), 'Marabou Stork');
   assert.equal(AnimalDisplayLines.formatSpeciesEnclosureLine('Marabou Stork', ''), 'Marabou Stork');
});

test('Test_FormatSpeciesEnclosureLine_TestJoinsSpeciesAndEnclosureName_ExpectOk', () => {
   assert.equal(
      AnimalDisplayLines.formatSpeciesEnclosureLine('Marabou Stork', 'White Rhino Viewing'),
      'Marabou Stork \u2022 White Rhino Viewing'
   );
   assert.equal(
      AnimalDisplayLines.formatSpeciesEnclosureLine('Golden Lion Tamarin', 'Indoor'),
      'Golden Lion Tamarin \u2022 Indoor'
   );
});

test('Test_FormatExhibitEnclosureTypeLine_TestJoinsExhibitAndEnclosureType_ExpectOk', () => {
   assert.equal(
      AnimalDisplayLines.formatExhibitEnclosureTypeLine('Americas Pavilion', 'Indoor'),
      'Americas Pavilion \u2022 Indoor'
   );
   assert.equal(
      AnimalDisplayLines.formatExhibitEnclosureTypeLine('Africa Savanna', 'Outdoor'),
      'Africa Savanna \u2022 Outdoor'
   );
   assert.equal(
      AnimalDisplayLines.formatExhibitEnclosureTypeLine('Africa Savanna', 'Aviary'),
      'Africa Savanna \u2022 Aviary'
   );
});
