import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationStationNameResolver } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationStationNameResolver.js';
import { TransportationSelectorModel } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { ItineraryTransportationStationRoles } from '../../../../../scripts/itinerary/itineraryTransportationStationRoles.js';

test('Test_AsObjectAndUniqueNames_TestValues_ExpectNormalized', () => {
   assert.deepEqual(TransportationStationNameResolver.asObject(null), {});
   assert.deepEqual(TransportationStationNameResolver.uniqueNames(['A', '', 'A', 'B']), ['A', 'B']);
});

test('Test_NamesForRoles_TestStations_ExpectFiltered', () => {
   assert.deepEqual(
      TransportationStationNameResolver.namesForRoles(
         [
            { name: 'Main', role: 'on' },
            { name: 'Side', role: 'off' },
            { name: 'Main', role: 'on' },
         ],
         ['on']
      ),
      ['Main']
   );
});

test('Test_BoardingAndOffboardingStationNames_TestStations_ExpectRoles', () => {
   const originalStations = TransportationSelectorModel.getTransportationStations;
   const originalOn = ItineraryTransportationStationRoles.getItineraryTransportationStationOnboardingRoles;
   const originalOff = ItineraryTransportationStationRoles.getItineraryTransportationStationOffboardingRoles;

   TransportationSelectorModel.getTransportationStations = () => [
      { name: 'Board', role: 'board' },
      { name: 'Exit', role: 'exit' },
   ];
   ItineraryTransportationStationRoles.getItineraryTransportationStationOnboardingRoles = () => ['board'];
   ItineraryTransportationStationRoles.getItineraryTransportationStationOffboardingRoles = () => ['exit'];

   try {
      assert.deepEqual(
         TransportationStationNameResolver.boardingStationNames({ name: 'Zoomobile' }),
         ['Board']
      );
      assert.deepEqual(
         TransportationStationNameResolver.offboardingStationNames({ name: 'Zoomobile' }),
         ['Exit']
      );
   } finally {
      TransportationSelectorModel.getTransportationStations = originalStations;
      ItineraryTransportationStationRoles.getItineraryTransportationStationOnboardingRoles = originalOn;
      ItineraryTransportationStationRoles.getItineraryTransportationStationOffboardingRoles = originalOff;
   }
});

test('Test_FallbackStationNames_TestLegsAndAttraction_ExpectNames', () => {
   const originalAdded = TransportationSelectorModel.isTransportationAddedAsAttraction;
   TransportationSelectorModel.isTransportationAddedAsAttraction = () => true;

   try {
      assert.deepEqual(
         TransportationStationNameResolver.fallbackStationNames(
            { legs: [{ from_station: 'A', to_station: 'B' }] },
            (legs) => legs[0].from_station
         ),
         ['A']
      );
      assert.deepEqual(
         TransportationStationNameResolver.fallbackStationNames(
            { main_station: 'Hub' },
            () => ''
         ),
         ['Hub']
      );
   } finally {
      TransportationSelectorModel.isTransportationAddedAsAttraction = originalAdded;
   }
});

test('Test_CreateStoredTransportation_TestStringAndObject_ExpectStored', () => {
   assert.deepEqual(
      TransportationStationNameResolver.createStoredTransportationFromString('Zoomobile'),
      {
         id: 'Zoomobile',
         name: 'Zoomobile',
         subtitle: '',
         infoLink: null,
         imageSrc: null,
         addedAsAttraction: false,
      }
   );
   assert.equal(TransportationStationNameResolver.createStoredTransportationFromString('  '), null);

   assert.deepEqual(
      TransportationStationNameResolver.createStoredTransportationFromObject({
         id: 'z1',
         name: 'Zoomobile',
         subtitle: 'Loop',
         infoLink: 'https://example.com',
         imageSrc: 'img.png',
         addedAsAttraction: true,
      }),
      {
         id: 'z1',
         name: 'Zoomobile',
         subtitle: 'Loop',
         infoLink: 'https://example.com',
         imageSrc: 'img.png',
         addedAsAttraction: true,
      }
   );
});
