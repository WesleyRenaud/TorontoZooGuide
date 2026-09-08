import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesMatcher } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesMatcher.js';

const SPECIES = ['African Lion', 'Amur Tiger', 'Giant Panda', 'Snow Leopard'];

test('Test_FilterSpeciesMatches_TestBlankQuery_ExpectEmpty', () => {
   assert.deepEqual(SpeciesMatcher.filterSpeciesMatches(SPECIES, '  '), []);
   assert.deepEqual(SpeciesMatcher.filterSpeciesMatches(SPECIES, ''), []);
});

test('Test_FilterSpeciesMatches_TestStartsWithBeforeContains_ExpectOrdered', () => {
   assert.deepEqual(
      SpeciesMatcher.filterSpeciesMatches(SPECIES, 'a'),
      ['African Lion', 'Amur Tiger', 'Giant Panda', 'Snow Leopard']
   );
});

test('Test_FilterSpeciesMatches_TestMaxResults_ExpectSliced', () => {
   assert.deepEqual(
      SpeciesMatcher.filterSpeciesMatches(SPECIES, 'a', 2),
      ['African Lion', 'Amur Tiger']
   );
});

test('Test_FilterSpeciesMatches_TestContainsOnly_ExpectMatches', () => {
   assert.deepEqual(
      SpeciesMatcher.filterSpeciesMatches(SPECIES, 'opard'),
      ['Snow Leopard']
   );
});
