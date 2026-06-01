import assert from 'node:assert/strict';
import { test } from 'node:test';

import { getItineraryItemKey } from '../../scripts/itinerary/panel/scheduleItemSearch.js';

test('getItineraryItemKey resolves keys for itinerary item types', () => {
   assert.equal(
      getItineraryItemKey('animals', {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      'African Lion||Africa Savanna'
   );
   assert.equal(
      getItineraryItemKey('attractions', { name: 'Zoomobile' }),
      'Zoomobile'
   );
   assert.equal(
      getItineraryItemKey('guardians_talks', { name: 'Amur Tiger' }),
      'Amur Tiger'
   );
   assert.equal(
      getItineraryItemKey('wild_encounters', { name: 'African Rainforest' }),
      'African Rainforest'
   );
});
