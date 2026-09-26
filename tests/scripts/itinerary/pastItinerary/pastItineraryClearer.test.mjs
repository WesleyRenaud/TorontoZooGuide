import assert from 'node:assert/strict';
import test from 'node:test';

import { PastItineraryClearer } from '../../../../scripts/itinerary/pastItinerary/pastItineraryClearer.js';
import { RenderView } from '../../../../scripts/itinerary/panel/renderView.js';
import { Position } from '../../../../scripts/shared/enums/position.js';


test('Test_ClearPastItinerary_TestInjectedClear_ExpectCalled', async () => {
   const calls = [];
   const reason = 'past';
   const clearItinerary = async (deps) => { calls.push(deps); };

   await PastItineraryClearer.clearPastItinerary({
      clearItinerary,
      reason,
   });

   assert.equal(calls.length, 1);
   assert.equal(calls[Position.FIRST].reason, reason);
});


test('Test_ClearPastItinerary_TestDefaultClear_ExpectRenderView', async () => {
   const original = RenderView.clearStoredItinerary;
   const calls = [];
   const source = 'test';
   RenderView.clearStoredItinerary = async (deps) => { calls.push(deps); };

   try {
      await PastItineraryClearer.clearPastItinerary({ source });

      assert.equal(calls.length, 1);
      assert.equal(calls[Position.FIRST].source, source);
   } finally {
      RenderView.clearStoredItinerary = original;
   }
});
