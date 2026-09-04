import assert from 'node:assert/strict';
import { test } from 'node:test';

import { SpeciesExhibitKey } from '../../../scripts/itinerary/speciesExhibitKey.js';
import { EnclosureType } from '../../../scripts/shared/enums/enclosureType.js';

test('Test_BuildSpeciesExhibitKey_TestNormalizedFields_ExpectJoinedKey', () => {
   assert.equal(
      SpeciesExhibitKey.buildSpeciesExhibitKey({
         species: '  African Lion  ',
         exhibit: ' Africa Savanna ',
      }),
      'african lion|africa savanna'
   );
   assert.equal(
      SpeciesExhibitKey.buildSpeciesExhibitKey({ species: 'Tiger' }),
      ''
   );
   assert.equal(
      SpeciesExhibitKey.buildSpeciesExhibitKey(
         { species: 'Tiger' },
         { requireExhibit: false }
      ),
      'tiger|'
   );
});

test('Test_BuildAnimalViewingSpotKey_TestEnclosureName_ExpectSuffix', () => {
   assert.equal(
      SpeciesExhibitKey.buildAnimalViewingSpotKey({
         species: 'Giraffe',
         exhibit: 'African Savanna',
         enclosure_name: 'Giraffe House',
      }),
      'giraffe|african savanna|giraffe house'
   );
   assert.equal(
      SpeciesExhibitKey.buildAnimalViewingSpotKey({
         species: 'Giraffe',
         exhibit: 'African Savanna',
         enclosure_type: EnclosureType.INDOOR,
      }),
      'giraffe|african savanna|indoor'
   );
});

test('Test_BuildUniqueSpeciesExhibitEntries_TestDuplicates_ExpectMerged', () => {
   const entries = SpeciesExhibitKey.buildUniqueSpeciesExhibitEntries(
      [
         { species: 'Lion', exhibit: 'Savanna', likelihood: 0.4 },
         { species: 'Lion', exhibit: 'Savanna', likelihood: 0.8 },
         { species: 'Zebra', exhibit: 'Savanna' },
      ],
      {
         mergeAnimals: (existing, animal) => ({
            ...existing,
            likelihood: Math.max(existing.likelihood ?? 0, animal.likelihood ?? 0),
         }),
      }
   );

   assert.equal(entries.length, 2);
   assert.equal(entries[0].item.likelihood, 0.8);
   assert.equal(entries[1].item.species, 'Zebra');
});
