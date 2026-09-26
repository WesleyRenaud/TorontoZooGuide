import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationScheduleItemKey } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';
import { ScheduleItemKeySeparator } from '../../../../../scripts/itinerary/scheduleItemKeySeparator.js';


test('Test_FromRow_TestValidFlag_ExpectKey', () => {
   const name = 'Zoomobile';
   const addedAsAttraction = true;
   const row = { name, added_as_attraction: addedAsAttraction };

   const key = TransportationScheduleItemKey.fromRow(row);

   assert.deepEqual(key, new TransportationScheduleItemKey(name, addedAsAttraction));
});


test('Test_FromRow_TestMissingFlag_ExpectNull', () => {
   const name = 'Zoomobile';
   const row = { name };

   const key = TransportationScheduleItemKey.fromRow(row);

   assert.equal(key, null);
});


test('Test_FromRow_TestBlankName_ExpectNull', () => {
   const row = { name: '', added_as_attraction: false };

   const key = TransportationScheduleItemKey.fromRow(row);

   assert.equal(key, null);
});


test('Test_FromWire_TestZero_ExpectNotAttraction', () => {
   const name = 'Zoomobile';
   const attractionFlag = '0';
   const wire = [name, attractionFlag].join(ScheduleItemKeySeparator.VALUE);

   const key = TransportationScheduleItemKey.fromWire(wire);

   assert.deepEqual(key, new TransportationScheduleItemKey(name, Boolean(Number(attractionFlag))));
});


test('Test_FromWire_TestOne_ExpectAttraction', () => {
   const name = 'Zoomobile';
   const attractionFlag = '1';
   const wire = [name, attractionFlag].join(ScheduleItemKeySeparator.VALUE);

   const key = TransportationScheduleItemKey.fromWire(wire);

   assert.deepEqual(key, new TransportationScheduleItemKey(name, Boolean(Number(attractionFlag))));
});


test('Test_FromWire_TestNameOnly_ExpectNull', () => {
   const wire = 'Zoomobile';

   const key = TransportationScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestMissingName_ExpectNull', () => {
   const attractionFlag = '0';
   const wire = `${ScheduleItemKeySeparator.VALUE}${attractionFlag}`;

   const key = TransportationScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_FromWire_TestInvalidFlag_ExpectNull', () => {
   const name = 'Zoomobile';
   const attractionFlag = 'yes';
   const wire = [name, attractionFlag].join(ScheduleItemKeySeparator.VALUE);

   const key = TransportationScheduleItemKey.fromWire(wire);

   assert.equal(key, null);
});


test('Test_ToWire_TestNotAttraction_ExpectJoined', () => {
   const name = 'Zoomobile';
   const addedAsAttraction = false;
   const key = new TransportationScheduleItemKey(name, addedAsAttraction);

   const wire = key.toWire();

   assert.equal(wire, TransportationScheduleItemKey.fromWire(
      [name, '0'].join(ScheduleItemKeySeparator.VALUE)
   ).toWire());
});


test('Test_ToWire_TestAttraction_ExpectJoined', () => {
   const name = 'Zoomobile';
   const addedAsAttraction = true;
   const key = new TransportationScheduleItemKey(name, addedAsAttraction);

   const wire = key.toWire();

   assert.equal(wire, TransportationScheduleItemKey.fromWire(
      [name, '1'].join(ScheduleItemKeySeparator.VALUE)
   ).toWire());
});
