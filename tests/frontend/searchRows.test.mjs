import assert from 'node:assert/strict';
import test from 'node:test';

import { flattenSearchRows } from '../../scripts/search/searchRows.js';

test('flattens normalized search groups into typed result rows', () => {
   const rows = flattenSearchRows({
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

test('ignores missing or malformed search groups', () => {
   assert.deepEqual(flattenSearchRows(null), []);
   assert.deepEqual(flattenSearchRows({ attractions: 'Conservation Carousel' }), []);
});
