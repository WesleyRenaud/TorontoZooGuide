import assert from 'node:assert/strict';
import test from 'node:test';

import { SpeciesMatcher } from '../../../../../scripts/consoleOperations/animals/autocomplete/speciesMatcher.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';

const AFRICAN_LION = 'African Lion';
const AMUR_TIGER = 'Amur Tiger';
const GIANT_PANDA = 'Giant Panda';
const SNOW_LEOPARD = 'Snow Leopard';
const SPECIES = [AFRICAN_LION, AMUR_TIGER, GIANT_PANDA, SNOW_LEOPARD];


test('Test_FilterSpeciesMatches_TestBlankQuery_ExpectEmpty', () => {
   const query = '  ';

   const matches = SpeciesMatcher.filterSpeciesMatches(SPECIES, query);

   assert.deepEqual(matches, []);
});


test('Test_FilterSpeciesMatches_TestEmptyQuery_ExpectEmpty', () => {
   const query = '';

   const matches = SpeciesMatcher.filterSpeciesMatches(SPECIES, query);

   assert.deepEqual(matches, []);
});


test('Test_FilterSpeciesMatches_TestStartsWithBeforeContains_ExpectOrdered', () => {
   const query = 'a';

   const matches = SpeciesMatcher.filterSpeciesMatches(SPECIES, query);

   assert.deepEqual(matches, SPECIES);
});


test('Test_FilterSpeciesMatches_TestMaxResults_ExpectSliced', () => {
   const query = 'a';
   const maxResults = 2;

   const matches = SpeciesMatcher.filterSpeciesMatches(SPECIES, query, maxResults);

   assert.deepEqual(matches, SPECIES.slice(Position.FIRST, maxResults));
});


test('Test_FilterSpeciesMatches_TestContainsOnly_ExpectMatches', () => {
   const query = 'opard';

   const matches = SpeciesMatcher.filterSpeciesMatches(SPECIES, query);

   assert.deepEqual(matches, [SNOW_LEOPARD]);
});
