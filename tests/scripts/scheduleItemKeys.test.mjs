import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemSearch } from '../../scripts/itinerary/panel/scheduleItemSearch.js';
import { GuardiansTalkScheduleItemKey } from '../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { TransportationScheduleItemKey } from '../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';

test('getItineraryItemKey resolves keys for itinerary item types', () => {
   assert.equal(
      ScheduleItemSearch.getItineraryItemKey('animals', {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      'African Lion||Africa Savanna'
   );
   assert.equal(
      ScheduleItemSearch.getItineraryItemKey('attractions', { name: 'Zoomobile' }),
      'Zoomobile'
   );
   assert.equal(
      ScheduleItemSearch.getItineraryItemKey('transportations', { name: 'Zoomobile' }),
      ''
   );
   assert.equal(
      ScheduleItemSearch.getItineraryItemKey('transportations', {
         name: 'Zoomobile',
         added_as_attraction: false,
      }),
      'Zoomobile||0'
   );
   assert.equal(
      ScheduleItemSearch.getItineraryItemKey('guardians_talks', { name: 'Amur Tiger' }),
      ''
   );
   assert.equal(
      ScheduleItemSearch.getItineraryItemKey('guardians_talks', {
         name: 'Amur Tiger',
         start_time: '14:00',
      }),
      'Amur Tiger||14:00'
   );
   assert.equal(
      ScheduleItemSearch.getItineraryItemKey('wild_encounters', { name: 'African Rainforest' }),
      null
   );
   assert.deepEqual(
      ScheduleItemSearch.getItineraryItemKey('wild_encounters', {
         name: 'Masai Giraffe',
         start_time: '14:00',
      }),
      new WildEncounterScheduleItemKey('Masai Giraffe', '14:00')
   );
});

test('guardians talk schedule item key wire round-trips', () => {
   const key = new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30', '12:00');

   assert.equal(key.toWire(), 'Amur Tiger||11:30||12:00');
   assert.deepEqual(
      GuardiansTalkScheduleItemKey.fromWire('Amur Tiger||11:30||12:00'),
      key
   );
   assert.deepEqual(
      GuardiansTalkScheduleItemKey.fromRow({
         name: 'Amur Tiger',
         start_time: '11:30',
         end_time: '12:00',
      }),
      key
   );
});

test('wild encounter schedule item key wire round-trips', () => {
   const key = new WildEncounterScheduleItemKey('Amur Tiger', '11:30', '12:00');

   assert.equal(key.toWire(), 'Amur Tiger||11:30||12:00');
   assert.deepEqual(
      WildEncounterScheduleItemKey.fromWire('Amur Tiger||11:30||12:00'),
      key
   );
   assert.deepEqual(
      WildEncounterScheduleItemKey.fromRow({
         name: 'Amur Tiger',
         start_time: '11:30',
         end_time: '12:00',
      }),
      key
   );
});

test('transportation schedule item key wire round-trips', () => {
   const key = new TransportationScheduleItemKey('Zoomobile', false);

   assert.equal(key.toWire(), 'Zoomobile||0');
   assert.deepEqual(
      TransportationScheduleItemKey.fromWire('Zoomobile||0'),
      key
   );
   assert.deepEqual(
      TransportationScheduleItemKey.fromRow({
         name: 'Zoomobile',
         added_as_attraction: false,
      }),
      key
   );
   assert.equal(TransportationScheduleItemKey.fromWire('Zoomobile'), null);
   assert.equal(
      TransportationScheduleItemKey.fromRow({ name: 'Zoomobile' }),
      null
   );
});
