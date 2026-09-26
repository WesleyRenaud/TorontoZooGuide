import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerBuilder.js';
import { DayPlannerView } from '../../../../../scripts/itinerary/panel/components/dayPlannerView.js';


test('Test_MakeDayPlannerPreview_TestArgs_ExpectDelegatesToView', () => {
   const original = DayPlannerView.makeDayPlannerPreview;
   const hours = 'hours';
   const itinerary = { date: '2026-06-15' };
   const handlers = { onArrival: 1 };
   const preview = { preview: true };
   const calls = [];

   DayPlannerView.makeDayPlannerPreview = (...args) => {
      calls.push(args);
      return preview;
   };

   try {
      const result = DayPlannerBuilder.makeDayPlannerPreview(hours, itinerary, handlers);

      assert.equal(result, preview);
      assert.deepEqual(calls, [[hours, itinerary, handlers]]);
   } finally {
      DayPlannerView.makeDayPlannerPreview = original;
   }
});
