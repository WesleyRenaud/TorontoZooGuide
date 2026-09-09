import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkScheduleItemKey } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { TimedScheduleItemKey } from '../../../../scripts/itinerary/selectors/timedScheduleItemKey.js';

test('Test_Constructor_TestUntrimmedValues_ExpectFrozenTrimmedKey', () => {
   const key = new TimedScheduleItemKey('  Otter Feed  ', ' 1:00 PM ', ' 1:30 PM ');

   assert.equal(key.name, 'Otter Feed');
   assert.equal(key.startTime, '1:00 PM');
   assert.equal(key.endTime, '1:30 PM');
   assert.equal(Object.isFrozen(key), true);
});

test('Test_Constructor_TestNoArguments_ExpectEmptyStrings', () => {
   const key = new TimedScheduleItemKey();

   assert.equal(key.name, '');
   assert.equal(key.startTime, '');
   assert.equal(key.endTime, '');
});

test('Test_FromWire_TestParts_ExpectKeyOrNull', () => {
   assert.deepEqual(
      TimedScheduleItemKey.fromWire('Otter Feed||1:00 PM||1:30 PM'),
      new TimedScheduleItemKey('Otter Feed', '1:00 PM', '1:30 PM')
   );
   assert.deepEqual(
      TimedScheduleItemKey.fromWire('Otter Feed||1:00 PM'),
      new TimedScheduleItemKey('Otter Feed', '1:00 PM')
   );
   assert.equal(TimedScheduleItemKey.fromWire('Otter Feed'), null);
   assert.equal(TimedScheduleItemKey.fromWire('Otter Feed||'), null);
   assert.equal(TimedScheduleItemKey.fromWire('Otter Feed||1:00 PM||'), null);
   assert.equal(TimedScheduleItemKey.fromWire(null), null);
});

test('Test_FromWire_TestSubclass_ExpectSubclassInstance', () => {
   const key = GuardiansTalkScheduleItemKey.fromWire('Amur Tiger||11:30');

   assert.equal(key instanceof GuardiansTalkScheduleItemKey, true);
});

test('Test_FromRow_TestDefaultNameField_ExpectKeyOrNull', () => {
   assert.deepEqual(
      TimedScheduleItemKey.fromRow({
         name: 'Otter Feed',
         start_time: '1:00 PM',
         end_time: '1:30 PM',
      }),
      new TimedScheduleItemKey('Otter Feed', '1:00 PM', '1:30 PM')
   );
   assert.equal(TimedScheduleItemKey.fromRow({ start_time: '1:00 PM' }), null);
   assert.equal(TimedScheduleItemKey.fromRow({ name: 'Otter Feed' }), null);
   assert.equal(TimedScheduleItemKey.fromRow(null), null);
});

test('Test_FromRow_TestSubclassNameFieldOrder_ExpectFirstPresentField', () => {
   assert.equal(
      GuardiansTalkScheduleItemKey.fromRow({
         name: 'Preferred',
         talk_name: 'Fallback',
         start_time: '11:30',
      }).name,
      'Preferred'
   );
   assert.equal(
      GuardiansTalkScheduleItemKey.fromRow({
         talk_name: 'Fallback',
         start_time: '11:30',
      }).name,
      'Fallback'
   );
});

test('Test_ToWire_TestWithAndWithoutEnd_ExpectJoined', () => {
   assert.equal(
      new TimedScheduleItemKey('Otter Feed', '1:00 PM', '1:30 PM').toWire(),
      'Otter Feed||1:00 PM||1:30 PM'
   );
   assert.equal(
      new TimedScheduleItemKey('Otter Feed', '1:00 PM').toWire(),
      'Otter Feed||1:00 PM'
   );
});

test('Test_Equals_TestEndTimeAndType_ExpectBoolean', () => {
   const key = new TimedScheduleItemKey('Otter Feed', '1:00 PM', '1:30 PM');

   assert.equal(key.equals(new TimedScheduleItemKey('Otter Feed', '1:00 PM', '1:30 PM')), true);
   assert.equal(key.equals(new TimedScheduleItemKey('Otter Feed', '1:00 PM')), false);
   assert.equal(key.equals(new TimedScheduleItemKey('Kangaroo', '1:00 PM', '1:30 PM')), false);
   assert.equal(key.equals(new TimedScheduleItemKey('Otter Feed', '2:00 PM', '1:30 PM')), false);
   assert.equal(
      key.equals(new GuardiansTalkScheduleItemKey('Otter Feed', '1:00 PM', '1:30 PM')),
      false
   );
   assert.equal(key.equals(null), false);
});
