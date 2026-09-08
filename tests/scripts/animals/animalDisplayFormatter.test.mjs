import assert from 'node:assert/strict';
import { test } from 'node:test';

import { AnimalDisplayFormatter } from '../../../scripts/animals/animalDisplayFormatter.js';

test('Test_FormatSpeciesEnclosureLine_TestOmitsSeparatorWhenEnclosureNameIsBlank_ExpectOk', () => {
   assert.equal(AnimalDisplayFormatter.formatSpeciesEnclosureLine('Marabou Stork', null), 'Marabou Stork');
   assert.equal(AnimalDisplayFormatter.formatSpeciesEnclosureLine('Marabou Stork', ''), 'Marabou Stork');
});

test('Test_FormatSpeciesEnclosureLine_TestJoinsSpeciesAndEnclosureName_ExpectOk', () => {
   assert.equal(
      AnimalDisplayFormatter.formatSpeciesEnclosureLine('Marabou Stork', 'White Rhino Viewing'),
      'Marabou Stork \u2022 White Rhino Viewing'
   );
   assert.equal(
      AnimalDisplayFormatter.formatSpeciesEnclosureLine('Golden Lion Tamarin', 'Indoor'),
      'Golden Lion Tamarin \u2022 Indoor'
   );
});

test('Test_FormatExhibitEnclosureTypeLine_TestJoinsExhibitAndEnclosureType_ExpectOk', () => {
   assert.equal(
      AnimalDisplayFormatter.formatExhibitEnclosureTypeLine('Americas Pavilion', 'Indoor'),
      'Americas Pavilion \u2022 Indoor'
   );
   assert.equal(
      AnimalDisplayFormatter.formatExhibitEnclosureTypeLine('Africa Savanna', 'Outdoor'),
      'Africa Savanna \u2022 Outdoor'
   );
   assert.equal(
      AnimalDisplayFormatter.formatExhibitEnclosureTypeLine('Africa Savanna', 'Aviary'),
      'Africa Savanna \u2022 Aviary'
   );
});

test('Test_FormatExhibitEnclosureTypeLine_TestBlankType_ExpectExhibitOnly', () => {
   assert.equal(AnimalDisplayFormatter.formatExhibitEnclosureTypeLine('Africa Savanna', ''), 'Africa Savanna');
   assert.equal(AnimalDisplayFormatter.formatExhibitEnclosureTypeLine('Africa Savanna', null), 'Africa Savanna');
});

test('Test_FormatAnimalTitleSuffix_TestEnclosure_ExpectSuffixOrEmpty', () => {
   assert.equal(AnimalDisplayFormatter.formatAnimalTitleSuffix(''), '');
   assert.equal(AnimalDisplayFormatter.formatAnimalTitleSuffix('Indoor'), ' \u2022 Indoor');
});
