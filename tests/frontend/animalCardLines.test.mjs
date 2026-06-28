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
});

test('formatExhibitEnclosureTypeLine omits enclosure type labels', () => {
   assert.equal(formatExhibitEnclosureTypeLine('Americas Pavilion', 'Indoor'), 'Americas Pavilion');
   assert.equal(formatExhibitEnclosureTypeLine('Africa Savanna', 'Outdoor'), 'Africa Savanna');
   assert.equal(formatExhibitEnclosureTypeLine('Indo-Malaya Outdoor', 'Outdoor'), 'Indo-Malaya Outdoor');
});

test('formatSpeciesEnclosureLine omits indoor and outdoor viewing spot names', () => {
   assert.equal(
      formatSpeciesEnclosureLine('Golden Lion Tamarin', 'Indoor'),
      'Golden Lion Tamarin'
   );
   assert.equal(
      formatSpeciesEnclosureLine('Golden Lion Tamarin', 'Outdoor'),
      'Golden Lion Tamarin'
   );
   assert.equal(
      formatSpeciesEnclosureLine('Marabou Stork', 'White Rhino Viewing'),
      'Marabou Stork \u2022 White Rhino Viewing'
   );
});

test('formatExhibitEnclosureTypeLine joins exhibit and enclosure type', () => {
   assert.equal(
      formatExhibitEnclosureTypeLine('Africa Savanna', 'Aviary'),
      'Africa Savanna \u2022 Aviary'
   );
});
