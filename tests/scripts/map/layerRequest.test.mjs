import assert from 'node:assert/strict';
import test from 'node:test';

import { LayerRequest } from '../../../scripts/map/layerRequest.js';

test('Test_BuildItineraryRows_TestFocusCandidates_ExpectTypedRows', () => {
   assert.deepEqual(LayerRequest.buildItineraryRows({
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

test('Test_BuildItineraryRows_TestScheduledRideStations_ExpectStationMarkersOnly', () => {
   assert.deepEqual(LayerRequest.buildItineraryRows({
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
         name: 'Zoo Shuttle',
         added_as_attraction: false,
         legs: [],
         type: 'transportation',
      },
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

test('Test_BuildItineraryRows_TestUnscheduledTransport_ExpectGenericMarkers', () => {
   assert.deepEqual(LayerRequest.buildItineraryRows({
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
         added_as_attraction: true,
         legs: [],
         type: 'transportation',
      },
   ]);
});

test('Test_BuildItineraryRows_TestEitherRoleScheduled_ExpectHideGenericMarker', () => {
   assert.deepEqual(LayerRequest.buildItineraryRows({
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [
         { name: 'Zoomobile', added_as_attraction: true, legs: [] },
         {
            name: 'Zoomobile',
            added_as_attraction: false,
            legs: [{
               from_station: 'Main Zoomobile Station',
               to_station: 'Eurasia Zoomobile Station',
            }],
         },
      ],
      transportationStations: [{
         name: 'Main Zoomobile Station',
         transportation: 'Zoomobile',
         role: 'onboarding_station',
      }, {
         name: 'Eurasia Zoomobile Station',
         transportation: 'Zoomobile',
         role: 'offboarding_station',
      }],
   }), [
      {
         name: 'Main Zoomobile Station',
         transportation: 'Zoomobile',
         role: 'onboarding_station',
         type: 'transportationStation',
      },
      {
         name: 'Eurasia Zoomobile Station',
         transportation: 'Zoomobile',
         role: 'offboarding_station',
         type: 'transportationStation',
      },
   ]);
});

test('Test_ResolveItineraryTransportationRouteMarkers_TestScheduledLegs_ExpectRouteMarkers', () => {
   assert.equal(
      LayerRequest.resolveItineraryTransportationRouteMarkers({
         transportations: [{ name: 'Zoomobile', legs: [] }],
      }),
      null
   );
   assert.deepEqual(
      LayerRequest.resolveItineraryTransportationRouteMarkers({
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
      LayerRequest.resolveItineraryTransportationRouteMarkers({
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

test('Test_BuildSelectedTypes_TestFocusedType_ExpectAddedWhenNeeded', () => {
   assert.deepEqual(LayerRequest.buildSelectedTypes(['animal'], 'giftShop', 'none'), ['giftShop', 'animal']);
   assert.deepEqual(
      LayerRequest.buildSelectedTypes(['transportationRoute'], 'transportationStation', 'summer'),
      ['transportationRoute']
   );
});

test('Test_BuildLayerRequest_TestFocusedRow_ExpectIncludes', () => {
   assert.deepEqual(LayerRequest.buildLayerRequest({
      dateCtx: {
         month: 'JUN',
         day: 15,
         dayOfWeek: 1,
         temp: 22,
      },
      selectedTypes: ['animal', 'giftShop'],
      transportationRoute: 'summer',
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
         transportationRoute: 'summer',
         speciesToInclude: [],
         restaurantsToInclude: [],
         giftShopsToInclude: ['Zootique'],
         attractionsToInclude: [],
         transportationStationsToInclude: [],
      },
   });
});
