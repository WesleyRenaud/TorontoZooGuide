import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkScheduleItemKey } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { TimedScheduleItemKey } from '../../../../scripts/itinerary/selectors/timedScheduleItemKey.js';
import { ScheduleItemKeySeparator } from '../../../../scripts/itinerary/scheduleItemKeySeparator.js';


test('Test_Constructor_TestUntrimmedValues_ExpectFrozenTrimmedKey', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';

   const key = new TimedScheduleItemKey(`  ${name}  `, ` ${startTime} `, ` ${endTime} `);

   assert.equal(key.name, name);
   assert.equal(key.startTime, startTime);
   assert.equal(key.endTime, endTime);
   assert.equal(Object.isFrozen(key), true);
});


test('Test_Constructor_TestNoArguments_ExpectEmptyStrings', () => {
   const key = new TimedScheduleItemKey();

   assert.equal(key.name, '');
   assert.equal(key.startTime, '');
   assert.equal(key.endTime, '');
});


test('Test_FromWire_TestNameStartAndEnd_ExpectKey', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const wire = [name, startTime, endTime].join(ScheduleItemKeySeparator.VALUE);

   const key = TimedScheduleItemKey.fromWire(wire);

   assert.deepEqual(key, new TimedScheduleItemKey(name, startTime, endTime));
});


test('Test_FromWire_TestNameAndStart_ExpectKey', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const wire = [name, startTime].join(ScheduleItemKeySeparator.VALUE);

   const key = TimedScheduleItemKey.fromWire(wire);

   assert.deepEqual(key, new TimedScheduleItemKey(name, startTime));
});


test('Test_FromWire_TestNameOnly_ExpectNull', () => {
   const wire = 'Otter Feed';

   const key = TimedScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestEmptyStart_ExpectNull', () => {
   const name = 'Otter Feed';
   const wire = `${name}${ScheduleItemKeySeparator.VALUE}`;

   const key = TimedScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestEmptyEnd_ExpectNull', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const wire = [name, startTime, ''].join(ScheduleItemKeySeparator.VALUE);

   const key = TimedScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestNull_ExpectNull', () => {
   const wire = null;

   const key = TimedScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestSubclass_ExpectSubclassInstance', () => {
   const name = 'Amur Tiger';
   const startTime = '11:30';
   const wire = [name, startTime].join(ScheduleItemKeySeparator.VALUE);

   const key = GuardiansTalkScheduleItemKey.fromWire(wire);

   assert.equal(key instanceof GuardiansTalkScheduleItemKey, true);
});


test('Test_FromRow_TestDefaultNameField_ExpectKey', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const row = {
      name,
      start_time: startTime,
      end_time: endTime,
   };

   const key = TimedScheduleItemKey.fromRow(row);

   assert.deepEqual(key, new TimedScheduleItemKey(name, startTime, endTime));
});


test('Test_FromRow_TestMissingName_ExpectNull', () => {
   const startTime = '1:00 PM';
   const row = { start_time: startTime };

   const key = TimedScheduleItemKey.fromRow(row);

   assert.equal(key, null);
});


test('Test_FromRow_TestMissingStart_ExpectNull', () => {
   const name = 'Otter Feed';
   const row = { name };

   const key = TimedScheduleItemKey.fromRow(row);

   assert.equal(key, null);
});


test('Test_FromRow_TestNull_ExpectNull', () => {
   const row = null;

   const key = TimedScheduleItemKey.fromRow(row);

   assert.equal(key, null);
});


test('Test_FromRow_TestSubclassPreferredName_ExpectFirstPresentField', () => {
   const preferred = 'Preferred';
   const fallback = 'Fallback';
   const startTime = '11:30';
   const row = {
      name: preferred,
      talk_name: fallback,
      start_time: startTime,
   };

   const key = GuardiansTalkScheduleItemKey.fromRow(row);

   assert.equal(key.name, preferred);
});


test('Test_FromRow_TestSubclassFallbackName_ExpectTalkName', () => {
   const fallback = 'Fallback';
   const startTime = '11:30';
   const row = {
      talk_name: fallback,
      start_time: startTime,
   };

   const key = GuardiansTalkScheduleItemKey.fromRow(row);

   assert.equal(key.name, fallback);
});


test('Test_ToWire_TestWithEnd_ExpectJoined', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new TimedScheduleItemKey(name, startTime, endTime);

   const wire = key.toWire();

   assert.equal(wire, [name, startTime, endTime].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_ToWire_TestWithoutEnd_ExpectJoined', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const key = new TimedScheduleItemKey(name, startTime);

   const wire = key.toWire();

   assert.equal(wire, [name, startTime].join(ScheduleItemKeySeparator.VALUE));
});


test('Test_Equals_TestMatchingKey_ExpectTrue', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new TimedScheduleItemKey(name, startTime, endTime);
   const other = new TimedScheduleItemKey(name, startTime, endTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, true);
});


test('Test_Equals_TestMissingEndTime_ExpectFalse', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new TimedScheduleItemKey(name, startTime, endTime);
   const other = new TimedScheduleItemKey(name, startTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, false);
});


test('Test_Equals_TestDifferentName_ExpectFalse', () => {
   const name = 'Otter Feed';
   const otherName = 'Kangaroo';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new TimedScheduleItemKey(name, startTime, endTime);
   const other = new TimedScheduleItemKey(otherName, startTime, endTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, false);
});


test('Test_Equals_TestDifferentStart_ExpectFalse', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const otherStart = '2:00 PM';
   const endTime = '1:30 PM';
   const key = new TimedScheduleItemKey(name, startTime, endTime);
   const other = new TimedScheduleItemKey(name, otherStart, endTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, false);
});


test('Test_Equals_TestDifferentType_ExpectFalse', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new TimedScheduleItemKey(name, startTime, endTime);
   const other = new GuardiansTalkScheduleItemKey(name, startTime, endTime);

   const isEqual = key.equals(other);

   assert.equal(isEqual, false);
});


test('Test_Equals_TestNull_ExpectFalse', () => {
   const name = 'Otter Feed';
   const startTime = '1:00 PM';
   const endTime = '1:30 PM';
   const key = new TimedScheduleItemKey(name, startTime, endTime);

   const isEqual = key.equals(null);

   assert.equal(isEqual, false);
});
