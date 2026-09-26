import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemSearcher } from '../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { ScheduleItemKeySeparator } from '../../scripts/itinerary/scheduleItemKeySeparator.js';
import { GuardiansTalkScheduleItemKey } from '../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { TransportationScheduleItemKey } from '../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';


test('Test_GetItineraryItemKey_TestAnimal_ExpectSpeciesExhibit', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const item = { species, exhibit };

   const key = ScheduleItemSearcher.getItineraryItemKey(ScheduleItemKind.ANIMAL.itemType, item);

   assert.equal(key, [species, exhibit].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_GetItineraryItemKey_TestAttraction_ExpectName', () => {
   const name = 'Zoomobile';
   const item = { name };

   const key = ScheduleItemSearcher.getItineraryItemKey(ScheduleItemKind.ATTRACTION.itemType, item);

   assert.equal(key, name);
});


test('Test_GetItineraryItemKey_TestTransportationWithoutFlag_ExpectEmpty', () => {
   const item = { name: 'Zoomobile' };

   const key = ScheduleItemSearcher.getItineraryItemKey(ScheduleItemKind.TRANSPORTATION.itemType, item);

   assert.equal(key, '');
});


test('Test_GetItineraryItemKey_TestTransportation_ExpectWireKey', () => {
   const name = 'Zoomobile';
   const addedAsAttraction = false;
   const item = { name, added_as_attraction: addedAsAttraction };

   const key = ScheduleItemSearcher.getItineraryItemKey(ScheduleItemKind.TRANSPORTATION.itemType, item);

   assert.equal(key, new TransportationScheduleItemKey(name, addedAsAttraction).toWire());
});


test('Test_GetItineraryItemKey_TestGuardiansTalkWithoutTime_ExpectEmpty', () => {
   const item = { name: 'Amur Tiger' };

   const key = ScheduleItemSearcher.getItineraryItemKey(ScheduleItemKind.GUARDIANS_TALK.itemType, item);

   assert.equal(key, '');
});


test('Test_GetItineraryItemKey_TestGuardiansTalk_ExpectWireKey', () => {
   const name = 'Amur Tiger';
   const startTime = '14:00';
   const item = { name, start_time: startTime };

   const key = ScheduleItemSearcher.getItineraryItemKey(ScheduleItemKind.GUARDIANS_TALK.itemType, item);

   assert.equal(key, new GuardiansTalkScheduleItemKey(name, startTime).toWire());
});


test('Test_GetItineraryItemKey_TestWildEncounterWithoutTime_ExpectNull', () => {
   const item = { name: 'African Rainforest' };

   const key = ScheduleItemSearcher.getItineraryItemKey(ScheduleItemKind.WILD_ENCOUNTER.itemType, item);

   assert.equal(key, null);
});


test('Test_GetItineraryItemKey_TestWildEncounter_ExpectKey', () => {
   const name = 'Masai Giraffe';
   const startTime = '14:00';
   const item = { name, start_time: startTime };

   const key = ScheduleItemSearcher.getItineraryItemKey(ScheduleItemKind.WILD_ENCOUNTER.itemType, item);

   assert.deepEqual(key, new WildEncounterScheduleItemKey(name, startTime));
});


test('Test_GuardiansTalkScheduleItemKey_TestToWire_ExpectJoined', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new GuardiansTalkScheduleItemKey(name, startTime, endTime);

   const wire = key.toWire();

   assert.equal(wire, [name, startTime, endTime].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_GuardiansTalkScheduleItemKey_TestFromWire_ExpectSameKey', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new GuardiansTalkScheduleItemKey(name, startTime, endTime);

   const parsed = GuardiansTalkScheduleItemKey.fromWire(key.toWire());

   assert.deepEqual(parsed, key);
});


test('Test_GuardiansTalkScheduleItemKey_TestFromRow_ExpectSameKey', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new GuardiansTalkScheduleItemKey(name, startTime, endTime);

   const parsed = GuardiansTalkScheduleItemKey.fromRow({
      name,
      start_time: startTime,
      end_time: endTime,
   });

   assert.deepEqual(parsed, key);
});


test('Test_WildEncounterScheduleItemKey_TestToWire_ExpectJoined', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new WildEncounterScheduleItemKey(name, startTime, endTime);

   const wire = key.toWire();

   assert.equal(wire, [name, startTime, endTime].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_WildEncounterScheduleItemKey_TestFromWire_ExpectSameKey', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new WildEncounterScheduleItemKey(name, startTime, endTime);

   const parsed = WildEncounterScheduleItemKey.fromWire(key.toWire());

   assert.deepEqual(parsed, key);
});


test('Test_WildEncounterScheduleItemKey_TestFromRow_ExpectSameKey', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new WildEncounterScheduleItemKey(name, startTime, endTime);

   const parsed = WildEncounterScheduleItemKey.fromRow({
      name,
      start_time: startTime,
      end_time: endTime,
   });

   assert.deepEqual(parsed, key);
});


test('Test_TransportationScheduleItemKey_TestWireRoundTrip_ExpectSameKey', () => {
   const name = 'Zoomobile';
   const addedAsAttraction = false;
   const key = new TransportationScheduleItemKey(name, addedAsAttraction);

   const parsed = TransportationScheduleItemKey.fromWire(key.toWire());

   assert.deepEqual(parsed, key);
   assert.equal(key.toWire(), parsed.toWire());
});


test('Test_TransportationScheduleItemKey_TestFromRow_ExpectSameKey', () => {
   const name = 'Zoomobile';
   const addedAsAttraction = false;
   const key = new TransportationScheduleItemKey(name, addedAsAttraction);

   const parsed = TransportationScheduleItemKey.fromRow({
      name,
      added_as_attraction: addedAsAttraction,
   });

   assert.deepEqual(parsed, key);
});


test('Test_TransportationScheduleItemKey_TestFromWireNameOnly_ExpectNull', () => {
   const name = 'Zoomobile';

   const parsed = TransportationScheduleItemKey.fromWire(name);

   assert.equal(parsed, null);
});


test('Test_TransportationScheduleItemKey_TestFromRowWithoutFlag_ExpectNull', () => {
   const item = { name: 'Zoomobile' };

   const parsed = TransportationScheduleItemKey.fromRow(item);

   assert.equal(parsed, null);
});
