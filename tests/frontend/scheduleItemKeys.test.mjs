import assert from 'node:assert/strict';
import { test } from 'node:test';

import { getItineraryItemKey } from '../../scripts/itinerary/panel/scheduleItemSearch.js';
import { WildEncounterScheduleItemKey } from '../../scripts/itinerary/selectors/wildEncounterSelector/scheduleItemKey.js';

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
      null
   );
   assert.deepEqual(
      getItineraryItemKey('wild_encounters', {
         name: 'Masai Giraffe',
         start_time: '14:00',
      }),
      new WildEncounterScheduleItemKey('Masai Giraffe', '14:00')
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
