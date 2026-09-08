import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkLinkedAnimalNormalizer } from '../../../scripts/guardians/guardiansTalkLinkedAnimalNormalizer.js';

test('Test_NormalizeGuardiansTalkLinkedAnimals_TestValidRows_ExpectTrimmed', () => {
   assert.deepEqual(
      GuardiansTalkLinkedAnimalNormalizer.normalizeGuardiansTalkLinkedAnimals([
         { species: '  African Lion  ', exhibit: '  African Savanna  ' },
         { species: 'Amur Tiger', exhibit: 'Eurasia' },
      ]),
      [
         { species: 'African Lion', exhibit: 'African Savanna' },
         { species: 'Amur Tiger', exhibit: 'Eurasia' },
      ]
   );
});

test('Test_NormalizeGuardiansTalkLinkedAnimals_TestIncompleteRows_ExpectFiltered', () => {
   assert.deepEqual(
      GuardiansTalkLinkedAnimalNormalizer.normalizeGuardiansTalkLinkedAnimals([
         { species: 'African Lion', exhibit: '' },
         { species: '', exhibit: 'Eurasia' },
         null,
         'skip',
      ]),
      []
   );
});
