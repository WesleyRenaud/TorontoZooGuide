import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerBuilder.js';
import { DayPlannerView } from '../../../../../scripts/itinerary/panel/components/dayPlannerView.js';

test('Test_MakeDayPlannerPreview_TestArgs_ExpectDelegatesToView', () => {
   const original = DayPlannerView.makeDayPlannerPreview;
   const calls = [];

   DayPlannerView.makeDayPlannerPreview = (...args) => {
      calls.push(args);
      return { preview: true };
   };

   try {
      const result = DayPlannerBuilder.makeDayPlannerPreview('hours', { date: '2026-06-15' }, { onArrival: 1 });
      assert.deepEqual(result, { preview: true });
      assert.deepEqual(calls, [['hours', { date: '2026-06-15' }, { onArrival: 1 }]]);
   } finally {
      DayPlannerView.makeDayPlannerPreview = original;
   }
});
