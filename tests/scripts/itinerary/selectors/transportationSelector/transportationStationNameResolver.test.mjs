import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationStationNameResolver } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationStationNameResolver.js';
import { TransportationSelectorModel } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { ItineraryTransportationStationRole } from '../../../../../scripts/shared/enums/itineraryTransportationStationRole.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';


test('Test_AsObject_TestNull_ExpectEmptyObject', () => {
   const value = null;

   const object = TransportationStationNameResolver.asObject(value);

   assert.deepEqual(object, {});
});


test('Test_UniqueNames_TestDuplicates_ExpectDeduped', () => {
   const first = 'A';
   const second = 'B';
   const values = [first, '', first, second];

   const names = TransportationStationNameResolver.uniqueNames(values);

   assert.deepEqual(names, [first, second]);
});


test('Test_NamesForRoles_TestStations_ExpectFiltered', () => {
   const main = 'Main';
   const side = 'Side';
   const onRole = 'on';
   const stations = [
      { name: main, role: onRole },
      { name: side, role: 'off' },
      { name: main, role: onRole },
   ];

   const names = TransportationStationNameResolver.namesForRoles(stations, [onRole]);

   assert.deepEqual(names, [main]);
});


test('Test_BoardingStationNames_TestStations_ExpectOnboarding', () => {
   const originalStations = TransportationSelectorModel.getTransportationStations;
   const originalOn = ItineraryTransportationStationRole.onboardingRoleValues;
   const originalOff = ItineraryTransportationStationRole.offboardingRoleValues;
   const board = 'Board';
   const exit = 'Exit';
   const boardRole = 'board';
   const exitRole = 'exit';
   TransportationSelectorModel.getTransportationStations = () => [
      { name: board, role: boardRole },
      { name: exit, role: exitRole },
   ];
   ItineraryTransportationStationRole.onboardingRoleValues = () => [boardRole];
   ItineraryTransportationStationRole.offboardingRoleValues = () => [exitRole];

   try {
      const names = TransportationStationNameResolver.boardingStationNames({ name: 'Zoomobile' });

      assert.deepEqual(names, [board]);
   } finally {
      TransportationSelectorModel.getTransportationStations = originalStations;
      ItineraryTransportationStationRole.onboardingRoleValues = originalOn;
      ItineraryTransportationStationRole.offboardingRoleValues = originalOff;
   }
});


test('Test_OffboardingStationNames_TestStations_ExpectOffboarding', () => {
   const originalStations = TransportationSelectorModel.getTransportationStations;
   const originalOn = ItineraryTransportationStationRole.onboardingRoleValues;
   const originalOff = ItineraryTransportationStationRole.offboardingRoleValues;
   const board = 'Board';
   const exit = 'Exit';
   const boardRole = 'board';
   const exitRole = 'exit';
   TransportationSelectorModel.getTransportationStations = () => [
      { name: board, role: boardRole },
      { name: exit, role: exitRole },
   ];
   ItineraryTransportationStationRole.onboardingRoleValues = () => [boardRole];
   ItineraryTransportationStationRole.offboardingRoleValues = () => [exitRole];

   try {
      const names = TransportationStationNameResolver.offboardingStationNames({ name: 'Zoomobile' });

      assert.deepEqual(names, [exit]);
   } finally {
      TransportationSelectorModel.getTransportationStations = originalStations;
      ItineraryTransportationStationRole.onboardingRoleValues = originalOn;
      ItineraryTransportationStationRole.offboardingRoleValues = originalOff;
   }
});


test('Test_FallbackStationNames_TestLegs_ExpectFromStation', () => {
   const originalAdded = TransportationSelectorModel.isTransportationAddedAsAttraction;
   TransportationSelectorModel.isTransportationAddedAsAttraction = () => true;
   const fromStation = 'A';
   const toStation = 'B';
   const row = { legs: [{ from_station: fromStation, to_station: toStation }] };

   try {
      const names = TransportationStationNameResolver.fallbackStationNames(
         row,
         (legs) => legs.at(Position.FIRST).from_station
      );

      assert.deepEqual(names, [fromStation]);
   } finally {
      TransportationSelectorModel.isTransportationAddedAsAttraction = originalAdded;
   }
});


test('Test_FallbackStationNames_TestMainStation_ExpectHub', () => {
   const originalAdded = TransportationSelectorModel.isTransportationAddedAsAttraction;
   TransportationSelectorModel.isTransportationAddedAsAttraction = () => true;
   const hub = 'Hub';
   const row = { main_station: hub };

   try {
      const names = TransportationStationNameResolver.fallbackStationNames(
         row,
         () => ''
      );

      assert.deepEqual(names, [hub]);
   } finally {
      TransportationSelectorModel.isTransportationAddedAsAttraction = originalAdded;
   }
});


test('Test_CreateStoredTransportationFromString_TestName_ExpectStored', () => {
   const name = 'Zoomobile';

   const stored = TransportationStationNameResolver.createStoredTransportationFromString(name);

   assert.equal(stored.id, name);
   assert.equal(stored.name, name);
   assert.equal(stored.subtitle, '');
   assert.equal(stored.infoLink, null);
   assert.equal(stored.imageSrc, null);
   assert.equal(stored.addedAsAttraction, false);
});


test('Test_CreateStoredTransportationFromString_TestBlank_ExpectNull', () => {
   const value = '  ';

   const stored = TransportationStationNameResolver.createStoredTransportationFromString(value);

   assert.equal(stored, null);
});


test('Test_CreateStoredTransportationFromObject_TestFields_ExpectStored', () => {
   const id = 'z1';
   const name = 'Zoomobile';
   const subtitle = 'Loop';
   const infoLink = 'https://example.com';
   const imageSrc = 'img.png';
   const item = {
      id,
      name,
      subtitle,
      infoLink,
      imageSrc,
      addedAsAttraction: true,
   };

   const stored = TransportationStationNameResolver.createStoredTransportationFromObject(item);

   assert.equal(stored.id, id);
   assert.equal(stored.name, name);
   assert.equal(stored.subtitle, subtitle);
   assert.equal(stored.infoLink, infoLink);
   assert.equal(stored.imageSrc, imageSrc);
   assert.equal(stored.addedAsAttraction, item.addedAsAttraction);
});
