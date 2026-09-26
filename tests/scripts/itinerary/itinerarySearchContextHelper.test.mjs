import assert from 'node:assert/strict';
import test from 'node:test';

import { DraftStore } from '../../../scripts/itinerary/draftStore.js';
import { ItinerarySearchContextHelper } from '../../../scripts/itinerary/itinerarySearchContextHelper.js';
import { VisitDateResolver } from '../../../scripts/itinerary/visitDateResolver.js';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';


test('Test_ResolveItinerarySearchDate_TestOverride_ExpectDate', async () => {
   globalThis.localStorage = createLocalStorageMock();
   const date = '2026-09-08';

   const resolved = await ItinerarySearchContextHelper.resolveItinerarySearchDate(date);

   assert.equal(resolved, date);
});


test('Test_ResolveItinerarySearchDate_TestStored_ExpectStoredDate', async () => {
   globalThis.localStorage = createLocalStorageMock();
   const storedDate = '2026-09-09';
   DraftStore.setStoredItineraryDate(storedDate);

   const resolved = await ItinerarySearchContextHelper.resolveItinerarySearchDate('');

   assert.equal(resolved, storedDate);
});


test('Test_ResolveItinerarySearchDate_TestFallback_ExpectResolvedDate', async () => {
   globalThis.localStorage = createLocalStorageMock();
   DraftStore.setStoredItineraryDate('');
   const original = VisitDateResolver.resolveEffectiveItineraryHoursDateIso;
   const fallbackDate = '2026-09-10';
   VisitDateResolver.resolveEffectiveItineraryHoursDateIso = async () => fallbackDate;

   try {
      const resolved = await ItinerarySearchContextHelper.resolveItinerarySearchDate('');

      assert.equal(resolved, fallbackDate);
   } finally {
      VisitDateResolver.resolveEffectiveItineraryHoursDateIso = original;
   }
});
