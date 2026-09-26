import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkScheduleItemKey } from '../../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ScheduleItemKeySeparator } from '../../../../../scripts/itinerary/scheduleItemKeySeparator.js';


test('Test_FromWire_TestNameStartAndEnd_ExpectKey', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const wire = [name, startTime, endTime].join(ScheduleItemKeySeparator.VALUE);

   const key = GuardiansTalkScheduleItemKey.fromWire(wire);

   assert.deepEqual(key, new GuardiansTalkScheduleItemKey(name, startTime, endTime));
});


test('Test_FromWire_TestNameAndStart_ExpectKey', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const wire = [name, startTime].join(ScheduleItemKeySeparator.VALUE);

   const key = GuardiansTalkScheduleItemKey.fromWire(wire);

   assert.deepEqual(key, new GuardiansTalkScheduleItemKey(name, startTime));
});


test('Test_FromWire_TestNameOnly_ExpectNull', () => {
   const wire = 'Amur Tiger';

   const key = GuardiansTalkScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestEmptyStart_ExpectNull', () => {
   const name = 'Amur Tiger';
   const wire = `${name}${ScheduleItemKeySeparator.VALUE}`;

   const key = GuardiansTalkScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestEmptyEnd_ExpectNull', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const wire = [name, startTime, ''].join(ScheduleItemKeySeparator.VALUE);

   const key = GuardiansTalkScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromRow_TestNameFields_ExpectKey', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const row = {
      name,
      start_time: startTime,
      end_time: endTime,
   };

   const key = GuardiansTalkScheduleItemKey.fromRow(row);

   assert.deepEqual(key, new GuardiansTalkScheduleItemKey(name, startTime, endTime));
});


test('Test_FromRow_TestTalkNameAlias_ExpectKey', () => {
   const talkName = 'Lion Talk';
   const startTime = '1:00 PM';
   const row = {
      talk_name: talkName,
      start_time: startTime,
   };

   const key = GuardiansTalkScheduleItemKey.fromRow(row);

   assert.deepEqual(key, new GuardiansTalkScheduleItemKey(talkName, startTime));
});


test('Test_FromRow_TestMissingStart_ExpectNull', () => {
   const name = 'Amur Tiger';
   const row = { name };

   const key = GuardiansTalkScheduleItemKey.fromRow(row);

   assert.equal(key, null);
});


test('Test_ToWire_TestWithEnd_ExpectJoined', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new GuardiansTalkScheduleItemKey(name, startTime, endTime);

   const wire = key.toWire();

   assert.equal(wire, [name, startTime, endTime].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_ToWire_TestWithoutEnd_ExpectJoined', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const key = new GuardiansTalkScheduleItemKey(name, startTime);

   const wire = key.toWire();

   assert.equal(wire, [name, startTime].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_Equals_TestMatchingKey_ExpectTrue', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new GuardiansTalkScheduleItemKey(name, startTime, endTime);
   const other = new GuardiansTalkScheduleItemKey(name, startTime, endTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, true);
});


test('Test_Equals_TestMissingEndTime_ExpectFalse', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new GuardiansTalkScheduleItemKey(name, startTime, endTime);
   const other = new GuardiansTalkScheduleItemKey(name, startTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, false);
});


test('Test_Equals_TestNull_ExpectFalse', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new GuardiansTalkScheduleItemKey(name, startTime, endTime);

   const isEqual = key.equals(null);

   assert.equal(isEqual, false);
});


test('Test_Equals_TestDifferentType_ExpectFalse', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const endTime = '12:00';
   const key = new GuardiansTalkScheduleItemKey(name, startTime, endTime);
   const other = new WildEncounterScheduleItemKey(name, startTime, endTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, false);
});
