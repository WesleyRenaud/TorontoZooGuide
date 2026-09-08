import assert from 'node:assert/strict';
import test from 'node:test';

import { PastItineraryClearer } from '../../../../scripts/itinerary/pastItinerary/pastItineraryClearer.js';
import { RenderView } from '../../../../scripts/itinerary/panel/renderView.js';

test('Test_ClearPastItinerary_TestInjectedClear_ExpectCalled', async () => {
   const calls = [];
   await PastItineraryClearer.clearPastItinerary({
      clearItinerary: async (deps) => { calls.push(deps); },
      reason: 'past',
   });
   assert.equal(calls.length, 1);
   assert.equal(calls[0].reason, 'past');
});

test('Test_ClearPastItinerary_TestDefaultClear_ExpectRenderView', async () => {
   const original = RenderView.clearStoredItinerary;
   const calls = [];
   RenderView.clearStoredItinerary = async (deps) => { calls.push(deps); };

   try {
      await PastItineraryClearer.clearPastItinerary({ source: 'test' });
      assert.equal(calls.length, 1);
      assert.equal(calls[0].source, 'test');
   } finally {
      RenderView.clearStoredItinerary = original;
   }
});
