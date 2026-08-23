import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildItineraryRows,
   buildLayerRequest,
   buildSelectedTypes,
   resolveItineraryTransportationRouteMarkers,
} from '../../scripts/map/layerRequest.js';

test('builds typed itinerary rows for map focus candidates', () => {
   assert.deepEqual(buildItineraryRows({
      animals: [
         { species: 'African Lion' },
         { species: 'Cheetah', exhibit: 'Africa Savanna' },
         { species: 'Cheetah', exhibit: 'Indo-Malaya Outdoor' },
      ],
      attractions: [{ name: 'Conservation Carousel' }],
      transportations: [{ name: 'Zoomobile', added_as_attraction: false, legs: [] }],
      transportationStations: [],
      guardiansTalks: [{ name: 'Amur Tiger' }],
      wildEncounters: [{ name: 'African Rainforest' }],
   }), [
      { species: 'African Lion', type: 'animal' },
      { species: 'Cheetah', exhibit: 'Africa Savanna', type: 'animal' },
      { species: 'Cheetah', exhibit: 'Indo-Malaya Outdoor', type: 'animal' },
      { name: 'Conservation Carousel', type: 'attraction' },
      { name: 'Zoomobile', added_as_attraction: false, legs: [], type: 'transportation' },
      { name: 'Amur Tiger', type: 'guardiansTalk' },
      { name: 'African Rainforest', type: 'wildEncounter' },
   ]);
});

test('includes transportation markers and station markers for scheduled rides', () => {
   assert.deepEqual(buildItineraryRows({
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [
         {
            name: 'Zoomobile',
            added_as_attraction: false,
            legs: [{
               from_station: 'Main Zoomobile Station',
               to_station: 'Africa Zoomobile Station',
            }],
         },
         {
            name: 'Zoo Shuttle',
            added_as_attraction: false,
            legs: [],
         },
      ],
      transportationStations: [{
         name: 'Main Zoomobile Station',
         transportation: 'Zoomobile',
         role: 'onboarding_station',
      }, {
         name: 'Africa Zoomobile Station',
         transportation: 'Zoomobile',
         role: 'offboarding_station',
      }],
   }), [
      {
         name: 'Zoomobile',
         added_as_attraction: false,
         legs: [{
            from_station: 'Main Zoomobile Station',
            to_station: 'Africa Zoomobile Station',
         }],
         type: 'transportation',
      },
      { name: 'Zoo Shuttle', added_as_attraction: false, legs: [], type: 'transportation' },
      {
         name: 'Main Zoomobile Station',
         transportation: 'Zoomobile',
         role: 'onboarding_station',
         type: 'transportationStation',
      },
      {
         name: 'Africa Zoomobile Station',
         transportation: 'Zoomobile',
         role: 'offboarding_station',
         type: 'transportationStation',
      },
   ]);
});

test('includes only transportations added as transportation', () => {
   assert.deepEqual(buildItineraryRows({
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [
         { name: 'Zoomobile', added_as_attraction: true, legs: [] },
         { name: 'Zoomobile', added_as_attraction: false, legs: [] },
      ],
      transportationStations: [],
   }), [
      {
         name: 'Zoomobile',
         added_as_attraction: false,
         legs: [],
         type: 'transportation',
      },
   ]);
});

test('resolves itinerary transportation route markers from scheduled legs', () => {
   assert.equal(
      resolveItineraryTransportationRouteMarkers({
         transportations: [{ name: 'Zoomobile', legs: [] }],
      }),
      null
   );
   assert.deepEqual(
      resolveItineraryTransportationRouteMarkers({
         transportations: [{
            name: 'Zoomobile',
            route: 'summer',
            route_marker_sequences: [['zm-s-005', 'zm-s-006']],
            legs: [{
               from_station: 'Main Zoomobile Station',
               to_station: 'Canadian Domain Zoomobile Station',
            }],
         }],
      }),
      {
         route: 'summer',
         markerSequences: [['zm-s-005', 'zm-s-006']],
      }
   );
   assert.deepEqual(
      resolveItineraryTransportationRouteMarkers({
         transportations: [{
            name: 'Zoo Shuttle',
            route: 'summer',
            route_marker_sequences: [['zm-s-005']],
            legs: [{ from_station: 'A', to_station: 'B' }],
         }],
      }),
      {
         route: 'summer',
         markerSequences: [['zm-s-005']],
      }
   );
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
