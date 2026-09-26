import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkScheduleItemKey } from '../../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ScheduleItemKeySeparator } from '../../../../../scripts/itinerary/scheduleItemKeySeparator.js';


test('Test_FromWire_TestNameStartAndEnd_ExpectKey', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const wire = [name, startTime, endTime].join(ScheduleItemKeySeparator.VALUE);

   const key = WildEncounterScheduleItemKey.fromWire(wire);

   assert.deepEqual(key, new WildEncounterScheduleItemKey(name, startTime, endTime));
});


test('Test_FromWire_TestNameAndStart_ExpectKey', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const wire = [name, startTime].join(ScheduleItemKeySeparator.VALUE);

   const key = WildEncounterScheduleItemKey.fromWire(wire);

   assert.deepEqual(key, new WildEncounterScheduleItemKey(name, startTime));
});


test('Test_FromWire_TestNameOnly_ExpectNull', () => {
   const wire = 'Giraffe';

   const key = WildEncounterScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestEmptyStart_ExpectNull', () => {
   const name = 'Giraffe';
   const wire = `${name}${ScheduleItemKeySeparator.VALUE}`;

   const key = WildEncounterScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestEmptyEnd_ExpectNull', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const wire = [name, startTime, ''].join(ScheduleItemKeySeparator.VALUE);

   const key = WildEncounterScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromRow_TestNameFields_ExpectKey', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const row = {
      name,
      start_time: startTime,
      end_time: endTime,
   };

   const key = WildEncounterScheduleItemKey.fromRow(row);

   assert.deepEqual(key, new WildEncounterScheduleItemKey(name, startTime, endTime));
});


test('Test_FromRow_TestWildEncounterAlias_ExpectKey', () => {
   const encounterName = 'Otter Feed';
   const startTime = '2:00 PM';
   const row = {
      wild_encounter: encounterName,
      start_time: startTime,
   };

   const key = WildEncounterScheduleItemKey.fromRow(row);

   assert.deepEqual(key, new WildEncounterScheduleItemKey(encounterName, startTime));
});


test('Test_FromRow_TestMissingStart_ExpectNull', () => {
   const name = 'Giraffe';
   const row = { name };

   const key = WildEncounterScheduleItemKey.fromRow(row);

   assert.equal(key, null);
});


test('Test_ToWire_TestWithEnd_ExpectJoined', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new WildEncounterScheduleItemKey(name, startTime, endTime);

   const wire = key.toWire();

   assert.equal(wire, [name, startTime, endTime].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_ToWire_TestWithoutEnd_ExpectJoined', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const key = new WildEncounterScheduleItemKey(name, startTime);

   const wire = key.toWire();

   assert.equal(wire, [name, startTime].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_Equals_TestMatchingKey_ExpectTrue', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new WildEncounterScheduleItemKey(name, startTime, endTime);
   const other = new WildEncounterScheduleItemKey(name, startTime, endTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, true);
});


test('Test_Equals_TestMissingEndTime_ExpectFalse', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new WildEncounterScheduleItemKey(name, startTime, endTime);
   const other = new WildEncounterScheduleItemKey(name, startTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, false);
});


test('Test_Equals_TestNull_ExpectFalse', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new WildEncounterScheduleItemKey(name, startTime, endTime);

   const isEqual = key.equals(null);

   assert.equal(isEqual, false);
});


test('Test_Equals_TestDifferentType_ExpectFalse', () => {
   const name = 'Giraffe';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new WildEncounterScheduleItemKey(name, startTime, endTime);
   const other = new GuardiansTalkScheduleItemKey(name, startTime, endTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, false);
});
