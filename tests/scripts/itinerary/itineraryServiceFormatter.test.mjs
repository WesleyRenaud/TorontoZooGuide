import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
import { ItineraryServiceFormatter } from '../../../scripts/itinerary/itineraryServiceFormatter.js';
import { ItineraryServiceTimeRunner } from '../../../scripts/itinerary/itineraryServiceTimeRunner.js';

test('Test_SetItineraryArrivalTime_TestValue_ExpectTimeRunner', async () => {
   const calls = [];
   const original = ItineraryServiceTimeRunner.setItineraryTimeAndDispatch;

   ItineraryServiceTimeRunner.setItineraryTimeAndDispatch = async (requestFn, time) => {
      calls.push({ requestFn, time });
      return { ok: true };
   };

   try {
      const result = await ItineraryServiceFormatter.setItineraryArrivalTime('10:00 AM');
      assert.deepEqual(result, { ok: true });
      assert.equal(calls.length, 1);
      assert.equal(calls[0].requestFn, ItineraryClient.setItineraryArrivalTimeRequest);
      assert.equal(calls[0].time, '10:00 AM');
   } finally {
      ItineraryServiceTimeRunner.setItineraryTimeAndDispatch = original;
   }
});

test('Test_SetItineraryDepartureTime_TestValue_ExpectTimeRunner', async () => {
   const calls = [];
   const original = ItineraryServiceTimeRunner.setItineraryTimeAndDispatch;

   ItineraryServiceTimeRunner.setItineraryTimeAndDispatch = async (requestFn, time) => {
      calls.push({ requestFn, time });
      return { ok: true };
   };

   try {
      const result = await ItineraryServiceFormatter.setItineraryDepartureTime('4:00 PM');
      assert.deepEqual(result, { ok: true });
      assert.equal(calls.length, 1);
      assert.equal(calls[0].requestFn, ItineraryClient.setItineraryDepartureTimeRequest);
      assert.equal(calls[0].time, '4:00 PM');
   } finally {
      ItineraryServiceTimeRunner.setItineraryTimeAndDispatch = original;
   }
});
