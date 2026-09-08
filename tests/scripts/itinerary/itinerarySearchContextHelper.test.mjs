import assert from 'node:assert/strict';
import test from 'node:test';

import { DraftStore } from '../../../scripts/itinerary/draftStore.js';
import { ItinerarySearchContextHelper } from '../../../scripts/itinerary/itinerarySearchContextHelper.js';
import { VisitDateResolver } from '../../../scripts/itinerary/visitDateResolver.js';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';

test('Test_ResolveItinerarySearchDate_TestOverrideStoredAndFallback_ExpectDate', async () => {
   globalThis.localStorage = createLocalStorageMock();

   assert.equal(
      await ItinerarySearchContextHelper.resolveItinerarySearchDate('2026-09-08'),
      '2026-09-08'
   );

   DraftStore.setStoredItineraryDate('2026-09-09');
   assert.equal(
      await ItinerarySearchContextHelper.resolveItinerarySearchDate(''),
      '2026-09-09'
   );

   DraftStore.setStoredItineraryDate('');
   const original = VisitDateResolver.resolveEffectiveItineraryHoursDateIso;
   VisitDateResolver.resolveEffectiveItineraryHoursDateIso = async () => '2026-09-10';
   try {
      assert.equal(
         await ItinerarySearchContextHelper.resolveItinerarySearchDate(''),
         '2026-09-10'
      );
   } finally {
      VisitDateResolver.resolveEffectiveItineraryHoursDateIso = original;
   }
});
