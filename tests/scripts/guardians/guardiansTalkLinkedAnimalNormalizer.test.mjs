import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkLinkedAnimalNormalizer } from '../../../scripts/guardians/guardiansTalkLinkedAnimalNormalizer.js';


test('Test_NormalizeGuardiansTalkLinkedAnimals_TestValidRows_ExpectTrimmed', () => {
   const lion = 'African Lion';
   const savanna = 'African Savanna';
   const tiger = 'Amur Tiger';
   const eurasia = 'Eurasia';
   const rows = [
      { species: `  ${lion}  `, exhibit: `  ${savanna}  ` },
      { species: tiger, exhibit: eurasia },
   ];

   const linked = GuardiansTalkLinkedAnimalNormalizer.normalizeGuardiansTalkLinkedAnimals(rows);

   assert.deepEqual(linked, [
      { species: lion, exhibit: savanna },
      { species: tiger, exhibit: eurasia },
   ]);
});


test('Test_NormalizeGuardiansTalkLinkedAnimals_TestIncompleteRows_ExpectFiltered', () => {
   const rows = [
      { species: 'African Lion', exhibit: '' },
      { species: '', exhibit: 'Eurasia' },
      null,
      'skip',
   ];

   const linked = GuardiansTalkLinkedAnimalNormalizer.normalizeGuardiansTalkLinkedAnimals(rows);

   assert.deepEqual(linked, []);
});
