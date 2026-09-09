import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkScheduleItemKey } from '../../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';

test('Test_FromWire_TestParts_ExpectKeyOrNull', () => {
   assert.deepEqual(
      WildEncounterScheduleItemKey.fromWire('Giraffe||1:00 PM||1:30 PM'),
      new WildEncounterScheduleItemKey('Giraffe', '1:00 PM', '1:30 PM')
   );
   assert.deepEqual(
      WildEncounterScheduleItemKey.fromWire('Giraffe||1:00 PM'),
      new WildEncounterScheduleItemKey('Giraffe', '1:00 PM')
   );
   assert.equal(WildEncounterScheduleItemKey.fromWire('Giraffe'), null);
   assert.equal(WildEncounterScheduleItemKey.fromWire('Giraffe||'), null);
   assert.equal(WildEncounterScheduleItemKey.fromWire('Giraffe||1:00 PM||'), null);
});

test('Test_FromRow_TestAliases_ExpectKeyOrNull', () => {
   assert.deepEqual(
      WildEncounterScheduleItemKey.fromRow({
         name: 'Giraffe',
         start_time: '1:00 PM',
         end_time: '1:30 PM',
      }),
      new WildEncounterScheduleItemKey('Giraffe', '1:00 PM', '1:30 PM')
   );
   assert.deepEqual(
      WildEncounterScheduleItemKey.fromRow({
         wild_encounter: 'Otter Feed',
         start_time: '2:00 PM',
      }),
      new WildEncounterScheduleItemKey('Otter Feed', '2:00 PM')
   );
   assert.equal(WildEncounterScheduleItemKey.fromRow({ name: 'Giraffe' }), null);
});

test('Test_ToWire_TestWithAndWithoutEnd_ExpectJoined', () => {
   assert.equal(
      new WildEncounterScheduleItemKey('Giraffe', '1:00 PM', '1:30 PM').toWire(),
      'Giraffe||1:00 PM||1:30 PM'
   );
   assert.equal(
      new WildEncounterScheduleItemKey('Giraffe', '1:00 PM').toWire(),
      'Giraffe||1:00 PM'
   );
});

test('Test_Equals_TestMatchingAndMismatch_ExpectBoolean', () => {
   const key = new WildEncounterScheduleItemKey('Giraffe', '1:00 PM', '1:30 PM');
   assert.equal(key.equals(new WildEncounterScheduleItemKey('Giraffe', '1:00 PM', '1:30 PM')), true);
   assert.equal(key.equals(new WildEncounterScheduleItemKey('Giraffe', '1:00 PM')), false);
   assert.equal(key.equals(null), false);
   assert.equal(
      key.equals(new GuardiansTalkScheduleItemKey('Giraffe', '1:00 PM', '1:30 PM')),
      false
   );
});
