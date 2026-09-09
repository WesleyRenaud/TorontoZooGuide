import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemSearcher } from '../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { GuardiansTalkScheduleItemKey } from '../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { TransportationScheduleItemKey } from '../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';

test('Test_GetItineraryItemKey_TestItemTypes_ExpectResolvedKeys', () => {
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey('animals', {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      'African Lion||Africa Savanna'
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey('attractions', { name: 'Zoomobile' }),
      'Zoomobile'
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey('transportations', { name: 'Zoomobile' }),
      ''
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey('transportations', {
         name: 'Zoomobile',
         added_as_attraction: false,
      }),
      new TransportationScheduleItemKey('Zoomobile', false).toWire()
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey('guardians_talks', { name: 'Amur Tiger' }),
      ''
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey('guardians_talks', {
         name: 'Amur Tiger',
         start_time: '14:00',
      }),
      new GuardiansTalkScheduleItemKey('Amur Tiger', '14:00').toWire()
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey('wild_encounters', { name: 'African Rainforest' }),
      null
   );
   assert.deepEqual(
      ScheduleItemSearcher.getItineraryItemKey('wild_encounters', {
         name: 'Masai Giraffe',
         start_time: '14:00',
      }),
      new WildEncounterScheduleItemKey('Masai Giraffe', '14:00')
   );
});

test('Test_GuardiansTalkScheduleItemKey_TestWireRoundTrip_ExpectSameKey', () => {
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

test('Test_WildEncounterScheduleItemKey_TestWireRoundTrip_ExpectSameKey', () => {
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

test('Test_TransportationScheduleItemKey_TestWireRoundTrip_ExpectSameKey', () => {
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
