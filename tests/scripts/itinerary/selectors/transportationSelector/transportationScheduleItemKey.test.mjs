import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationScheduleItemKey } from '../../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';

test('Test_FromRow_TestValidAndInvalid_ExpectKeyOrNull', () => {
   assert.deepEqual(
      TransportationScheduleItemKey.fromRow({ name: 'Zoomobile', added_as_attraction: true }),
      new TransportationScheduleItemKey('Zoomobile', true)
   );
   assert.equal(TransportationScheduleItemKey.fromRow({ name: 'Zoomobile' }), null);
   assert.equal(TransportationScheduleItemKey.fromRow({ name: '', added_as_attraction: false }), null);
});

test('Test_FromWire_TestTokens_ExpectKeyOrNull', () => {
   assert.deepEqual(
      TransportationScheduleItemKey.fromWire('Zoomobile||0'),
      new TransportationScheduleItemKey('Zoomobile', false)
   );
   assert.deepEqual(
      TransportationScheduleItemKey.fromWire('Zoomobile||1'),
      new TransportationScheduleItemKey('Zoomobile', true)
   );
   assert.equal(TransportationScheduleItemKey.fromWire('Zoomobile'), null);
   assert.equal(TransportationScheduleItemKey.fromWire('||0'), null);
   assert.equal(TransportationScheduleItemKey.fromWire('Zoomobile||yes'), null);
});

test('Test_ToWire_TestFlags_ExpectJoined', () => {
   assert.equal(
      new TransportationScheduleItemKey('Zoomobile', false).toWire(),
      TransportationScheduleItemKey.fromWire('Zoomobile||0').toWire()
   );
   assert.equal(
      new TransportationScheduleItemKey('Zoomobile', true).toWire(),
      TransportationScheduleItemKey.fromWire('Zoomobile||1').toWire()
   );
});
