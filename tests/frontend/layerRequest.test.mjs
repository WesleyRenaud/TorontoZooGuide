import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildItineraryRows,
   buildLayerRequest,
   buildSelectedTypes,
} from '../../scripts/map/layerRequest.js';

test('builds typed itinerary rows for map focus candidates', () => {
   assert.deepEqual(buildItineraryRows({
      animals: [
         { species: 'African Lion' },
         { species: 'Cheetah', exhibit: 'Africa Savanna' },
         { species: 'Cheetah', exhibit: 'Indo-Malaya Outdoor' },
      ],
      attractions: [{ name: 'Conservation Carousel' }],
      transportations: [{ name: 'Zoomobile' }],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [{ name: 'African Rainforest' }],
   }), [
      { species: 'African Lion', type: 'animal' },
      { species: 'Cheetah', exhibit: 'Africa Savanna', type: 'animal' },
      { species: 'Cheetah', exhibit: 'Indo-Malaya Outdoor', type: 'animal' },
      { name: 'Conservation Carousel', type: 'attraction' },
      { name: 'Zoomobile', type: 'transportation' },
      { name: 'Amur Tiger', type: 'guardiansTalk' },
      { name: 'African Rainforest', type: 'wildEncounter' },
   ]);
});

test('adds focused type to selected types when needed', () => {
   assert.deepEqual(buildSelectedTypes(['animal'], 'giftShop', 'none'), ['giftShop', 'animal']);
   assert.deepEqual(
      buildSelectedTypes(['zoomobileRoute'], 'zoomobileStation', 'summer'),
      ['zoomobileRoute']
   );
});

test('builds layer request context with focused row includes', () => {
   assert.deepEqual(buildLayerRequest({
      dateCtx: {
         month: 'JUN',
         day: 15,
         dayOfWeek: 1,
         temp: 22,
      },
      selectedTypes: ['animal', 'giftShop'],
      zoomobileRoute: 'summer',
      focusType: 'giftShop',
      focusRow: { name: '  Zootique  ' },
      includeOffDisplayAnimals: false,
      includeClosedRestaurants: false,
      includeClosedRestrooms: false,
      includeClosedGiftShops: true,
      includeClosedAttractions: false,
   }), {
      selectedTypes: ['animal', 'giftShop'],
      ctx: {
         month: 'JUN',
         day: 15,
         dayOfWeek: 1,
         temp: 22,
         includeOffDisplayAnimals: false,
         includeClosedRestaurants: false,
         includeClosedRestrooms: false,
         includeClosedGiftShops: true,
         includeClosedAttractions: false,
         zoomobileRoute: 'summer',
         speciesToInclude: [],
         restaurantsToInclude: [],
         giftShopsToInclude: ['Zootique'],
         attractionsToInclude: [],
         zoomobileStationsToInclude: [],
      },
   });
});
