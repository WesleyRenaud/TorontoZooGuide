import assert from 'node:assert/strict';
import test from 'node:test';

import { LayerRequest } from '../../../scripts/map/layerRequest.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';

const africanLion = { species: 'African Lion' };
const cheetahSavanna = { species: 'Cheetah', exhibit: 'Africa Savanna' };
const cheetahIndoMalaya = { species: 'Cheetah', exhibit: 'Indo-Malaya Outdoor' };
const conservationCarousel = { name: 'Conservation Carousel' };
const zoomobile = { name: 'Zoomobile', added_as_attraction: false, legs: [] };
const zoomobileAttraction = { name: 'Zoomobile', added_as_attraction: true, legs: [] };
const zooShuttle = { name: 'Zoo Shuttle', added_as_attraction: false, legs: [] };
const amurTigerTalk = { name: 'Amur Tiger' };
const africanRainforestEncounter = { name: 'African Rainforest' };
const mainStation = {
   name: 'Main Zoomobile Station',
   transportation: 'Zoomobile',
   role: 'onboarding_station',
};
const africaStation = {
   name: 'Africa Zoomobile Station',
   transportation: 'Zoomobile',
   role: 'offboarding_station',
};
const eurasiaStation = {
   name: 'Eurasia Zoomobile Station',
   transportation: 'Zoomobile',
   role: 'offboarding_station',
};


test('Test_BuildItineraryRows_TestFocusCandidates_ExpectTypedRows', () => {
   const itinerary = {
      animals: [africanLion, cheetahSavanna, cheetahIndoMalaya],
      attractions: [conservationCarousel],
      transportations: [zoomobile],
      transportationStations: [],
      guardiansTalks: [amurTigerTalk],
      wildEncounters: [africanRainforestEncounter],
   };

   const rows = LayerRequest.buildItineraryRows(itinerary);

   assert.deepEqual(rows, [
      { ...africanLion, type: ItemType.ANIMAL },
      { ...cheetahSavanna, type: ItemType.ANIMAL },
      { ...cheetahIndoMalaya, type: ItemType.ANIMAL },
      { ...conservationCarousel, type: ItemType.ATTRACTION },
      { ...zoomobile, type: ItemType.TRANSPORTATION },
      { ...amurTigerTalk, type: ItemType.GUARDIANS_TALK },
      { ...africanRainforestEncounter, type: ItemType.WILD_ENCOUNTER },
   ]);
});


test('Test_BuildItineraryRows_TestScheduledRideStations_ExpectStationMarkersOnly', () => {
   const scheduledZoomobile = {
      name: 'Zoomobile',
      added_as_attraction: false,
      legs: [{
         from_station: mainStation.name,
         to_station: africaStation.name,
      }],
   };
   const itinerary = {
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [scheduledZoomobile, zooShuttle],
      transportationStations: [mainStation, africaStation],
   };

   const rows = LayerRequest.buildItineraryRows(itinerary);

   assert.deepEqual(rows, [
      { ...zooShuttle, type: ItemType.TRANSPORTATION },
      { ...mainStation, type: ItemType.TRANSPORTATION_STATION },
      { ...africaStation, type: ItemType.TRANSPORTATION_STATION },
   ]);
});


test('Test_BuildItineraryRows_TestUnscheduledTransport_ExpectGenericMarkers', () => {
   const itinerary = {
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [zoomobileAttraction, zoomobile],
      transportationStations: [],
   };

   const rows = LayerRequest.buildItineraryRows(itinerary);

   assert.deepEqual(rows, [
      { ...zoomobileAttraction, type: ItemType.TRANSPORTATION },
   ]);
});


test('Test_BuildItineraryRows_TestEitherRoleScheduled_ExpectHideGenericMarker', () => {
   const scheduledZoomobile = {
      name: 'Zoomobile',
      added_as_attraction: false,
      legs: [{
         from_station: mainStation.name,
         to_station: eurasiaStation.name,
      }],
   };
   const itinerary = {
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [zoomobileAttraction, scheduledZoomobile],
      transportationStations: [mainStation, eurasiaStation],
   };

   const rows = LayerRequest.buildItineraryRows(itinerary);

   assert.deepEqual(rows, [
      { ...mainStation, type: ItemType.TRANSPORTATION_STATION },
      { ...eurasiaStation, type: ItemType.TRANSPORTATION_STATION },
   ]);
});


test('Test_ResolveItineraryTransportationRouteMarkers_TestEmptyLegs_ExpectNull', () => {
   const itinerary = {
      transportations: [{ name: 'Zoomobile', legs: [] }],
   };

   const markers = LayerRequest.resolveItineraryTransportationRouteMarkers(itinerary);

   assert.equal(markers, null);
});


test('Test_ResolveItineraryTransportationRouteMarkers_TestScheduledLegs_ExpectRouteMarkers', () => {
   const route = 'summer';
   const markerSequences = [['zm-s-005', 'zm-s-006']];
   const itinerary = {
      transportations: [{
         name: 'Zoomobile',
         route,
         route_marker_sequences: markerSequences,
         legs: [{
            from_station: 'Main Zoomobile Station',
            to_station: 'Canadian Domain Zoomobile Station',
         }],
      }],
   };

   const markers = LayerRequest.resolveItineraryTransportationRouteMarkers(itinerary);

   assert.deepEqual(markers, {
      route,
      markerSequences,
   });
});


test('Test_ResolveItineraryTransportationRouteMarkers_TestShuttle_ExpectRouteMarkers', () => {
   const route = 'summer';
   const markerSequences = [['zm-s-005']];
   const itinerary = {
      transportations: [{
         name: 'Zoo Shuttle',
         route,
         route_marker_sequences: markerSequences,
         legs: [{ from_station: 'A', to_station: 'B' }],
      }],
   };

   const markers = LayerRequest.resolveItineraryTransportationRouteMarkers(itinerary);

   assert.deepEqual(markers, {
      route,
      markerSequences,
   });
});


test('Test_BuildSelectedTypes_TestFocusedType_ExpectAddedWhenNeeded', () => {
   const selectedTypes = [ItemType.ANIMAL];
   const focusType = ItemType.GIFT_SHOP;

   const types = LayerRequest.buildSelectedTypes(selectedTypes, focusType, 'none');

   assert.deepEqual(types, [focusType, ...selectedTypes]);
});


test('Test_BuildSelectedTypes_TestStationFocusWithRoute_ExpectRouteOnly', () => {
   const selectedTypes = [ItemType.TRANSPORTATION_ROUTE];
   const focusType = ItemType.TRANSPORTATION_STATION;
   const transportationRoute = 'summer';

   const types = LayerRequest.buildSelectedTypes(selectedTypes, focusType, transportationRoute);

   assert.deepEqual(types, selectedTypes);
});


test('Test_BuildLayerRequest_TestFocusedRow_ExpectIncludes', () => {
   const giftShopName = 'Zootique';
   const dateCtx = {
      month: 'JUN',
      day: 15,
      dayOfWeek: 1,
      temp: 22,
   };
   const selectedTypes = [ItemType.ANIMAL, ItemType.GIFT_SHOP];
   const transportationRoute = 'summer';
   const includeOffDisplayAnimals = false;
   const includeClosedRestaurants = false;
   const includeClosedRestrooms = false;
   const includeClosedGiftShops = true;
   const includeClosedAttractions = false;

   const request = LayerRequest.buildLayerRequest({
      dateCtx,
      selectedTypes,
      transportationRoute,
      focusType: ItemType.GIFT_SHOP,
      focusRow: { name: `  ${giftShopName}  ` },
      includeOffDisplayAnimals,
      includeClosedRestaurants,
      includeClosedRestrooms,
      includeClosedGiftShops,
      includeClosedAttractions,
   });

   assert.deepEqual(request, {
      selectedTypes,
      ctx: {
         ...dateCtx,
         includeOffDisplayAnimals,
         includeClosedRestaurants,
         includeClosedRestrooms,
         includeClosedGiftShops,
         includeClosedAttractions,
         transportationRoute,
         speciesToInclude: [],
         restaurantsToInclude: [],
         giftShopsToInclude: [giftShopName],
         attractionsToInclude: [],
         transportationStationsToInclude: [],
      },
   });
});
