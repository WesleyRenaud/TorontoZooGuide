import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
import { ItineraryServiceFormatter } from '../../../scripts/itinerary/itineraryServiceFormatter.js';
import { ItineraryServiceTimeRunner } from '../../../scripts/itinerary/itineraryServiceTimeRunner.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_SetItineraryArrivalTime_TestValue_ExpectTimeRunner', async () => {
   const calls = [];
   const original = ItineraryServiceTimeRunner.setItineraryTimeAndDispatch;
   const time = '10:00 AM';
   const dispatched = { ok: true };
   ItineraryServiceTimeRunner.setItineraryTimeAndDispatch = async (requestFn, nextTime) => {
      calls.push({ requestFn, time: nextTime });
      return dispatched;
   };

   try {
      const result = await ItineraryServiceFormatter.setItineraryArrivalTime(time);

      assert.deepEqual(result, dispatched);
      assert.equal(calls.length, 1);
      assert.equal(calls[Position.FIRST].requestFn, ItineraryClient.setItineraryArrivalTimeRequest);
      assert.equal(calls[Position.FIRST].time, time);
   } finally {
      ItineraryServiceTimeRunner.setItineraryTimeAndDispatch = original;
   }
});


test('Test_SetItineraryDepartureTime_TestValue_ExpectTimeRunner', async () => {
   const calls = [];
   const original = ItineraryServiceTimeRunner.setItineraryTimeAndDispatch;
   const time = '4:00 PM';
   const dispatched = { ok: true };
   ItineraryServiceTimeRunner.setItineraryTimeAndDispatch = async (requestFn, nextTime) => {
      calls.push({ requestFn, time: nextTime });
      return dispatched;
   };

   try {
      const result = await ItineraryServiceFormatter.setItineraryDepartureTime(time);

      assert.deepEqual(result, dispatched);
      assert.equal(calls.length, 1);
      assert.equal(calls[Position.FIRST].requestFn, ItineraryClient.setItineraryDepartureTimeRequest);
      assert.equal(calls[Position.FIRST].time, time);
   } finally {
      ItineraryServiceTimeRunner.setItineraryTimeAndDispatch = original;
   }
});
