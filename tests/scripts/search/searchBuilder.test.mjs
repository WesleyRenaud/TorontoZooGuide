import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchBuilder } from '../../../scripts/search/searchBuilder.js';

test('Test_FlattenSearchRows_TestNormalizedGroups_ExpectTypedRows', () => {
   const rows = SearchBuilder.flattenSearchRows({
      animals: [{ species: 'African Lion' }],
      gift_shops: [{ name: 'Zootique' }],
      attractions: [{ name: 'Conservation Carousel' }],
      guardians_talks: [{ name: 'Amur Tiger' }],
      wild_encounters: [{ name: 'African Rainforest' }],
      unsupported: [{ name: 'Not a search group' }],
   });

   assert.deepEqual(rows, [
      { species: 'African Lion', type: 'animal' },
      { name: 'Zootique', type: 'giftShop' },
      { name: 'Conservation Carousel', type: 'attraction' },
      { name: 'Amur Tiger', type: 'guardiansTalk' },
      { name: 'African Rainforest', type: 'wildEncounter' },
   ]);
});

test('Test_FlattenSearchRows_TestMissingGroups_ExpectEmpty', () => {
   assert.deepEqual(SearchBuilder.flattenSearchRows(null), []);
   assert.deepEqual(SearchBuilder.flattenSearchRows({ attractions: 'Conservation Carousel' }), []);
});
