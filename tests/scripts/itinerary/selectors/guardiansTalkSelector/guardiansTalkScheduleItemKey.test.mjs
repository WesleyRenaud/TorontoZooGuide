import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkScheduleItemKey } from '../../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';

test('Test_FromWire_TestParts_ExpectKeyOrNull', () => {
   assert.deepEqual(
      GuardiansTalkScheduleItemKey.fromWire('Amur Tiger||11:30||12:00'),
      new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30', '12:00')
   );
   assert.deepEqual(
      GuardiansTalkScheduleItemKey.fromWire('Amur Tiger||11:30'),
      new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30')
   );
   assert.equal(GuardiansTalkScheduleItemKey.fromWire('Amur Tiger'), null);
   assert.equal(GuardiansTalkScheduleItemKey.fromWire('Amur Tiger||'), null);
   assert.equal(GuardiansTalkScheduleItemKey.fromWire('Amur Tiger||11:30||'), null);
});

test('Test_FromRow_TestAliases_ExpectKeyOrNull', () => {
   assert.deepEqual(
      GuardiansTalkScheduleItemKey.fromRow({
         name: 'Amur Tiger',
         start_time: '11:30',
         end_time: '12:00',
      }),
      new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30', '12:00')
   );
   assert.deepEqual(
      GuardiansTalkScheduleItemKey.fromRow({
         talk_name: 'Lion Talk',
         start_time: '1:00 PM',
      }),
      new GuardiansTalkScheduleItemKey('Lion Talk', '1:00 PM')
   );
   assert.equal(GuardiansTalkScheduleItemKey.fromRow({ name: 'Amur Tiger' }), null);
});

test('Test_ToWire_TestWithAndWithoutEnd_ExpectJoined', () => {
   assert.equal(
      new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30', '12:00').toWire(),
      'Amur Tiger||11:30||12:00'
   );
   assert.equal(
      new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30').toWire(),
      'Amur Tiger||11:30'
   );
});

test('Test_Equals_TestMatchingAndMismatch_ExpectBoolean', () => {
   const key = new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30', '12:00');
   assert.equal(key.equals(new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30', '12:00')), true);
   assert.equal(key.equals(new GuardiansTalkScheduleItemKey('Amur Tiger', '11:30')), false);
   assert.equal(key.equals(null), false);
   assert.equal(
      key.equals(new WildEncounterScheduleItemKey('Amur Tiger', '11:30', '12:00')),
      false
   );
});
