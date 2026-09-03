import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   formatExhibitEnclosureTypeLine,
   formatSpeciesEnclosureLine,
} from '../../scripts/animals/animalDisplayLines.js';

test('formatSpeciesEnclosureLine omits separator when enclosure name is blank', () => {
   assert.equal(formatSpeciesEnclosureLine('Marabou Stork', null), 'Marabou Stork');
   assert.equal(formatSpeciesEnclosureLine('Marabou Stork', ''), 'Marabou Stork');
});

test('formatSpeciesEnclosureLine joins species and enclosure name', () => {
   assert.equal(
      formatSpeciesEnclosureLine('Marabou Stork', 'White Rhino Viewing'),
      'Marabou Stork \u2022 White Rhino Viewing'
   );
   assert.equal(
      formatSpeciesEnclosureLine('Golden Lion Tamarin', 'Indoor'),
      'Golden Lion Tamarin \u2022 Indoor'
   );
});

test('formatExhibitEnclosureTypeLine joins exhibit and enclosure type', () => {
   assert.equal(
      formatExhibitEnclosureTypeLine('Americas Pavilion', 'Indoor'),
      'Americas Pavilion \u2022 Indoor'
   );
   assert.equal(
      formatExhibitEnclosureTypeLine('Africa Savanna', 'Outdoor'),
      'Africa Savanna \u2022 Outdoor'
   );
   assert.equal(
      formatExhibitEnclosureTypeLine('Africa Savanna', 'Aviary'),
      'Africa Savanna \u2022 Aviary'
   );
});
