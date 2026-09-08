import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
import { DraftStore } from '../../../scripts/itinerary/draftStore.js';
import { ItineraryServiceHelper } from '../../../scripts/itinerary/itineraryServiceHelper.js';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';

test('Test_FetchSavedItineraryVisitDate_TestResponse_ExpectStored', async () => {
   globalThis.localStorage = createLocalStorageMock();
   const original = ItineraryClient.getItineraryDateRequest;
   ItineraryClient.getItineraryDateRequest = async () => ({ date: '2026-09-08' });

   try {
      const date = await ItineraryServiceHelper.fetchSavedItineraryVisitDate();
      assert.equal(date, '2026-09-08');
      assert.equal(DraftStore.getStoredItineraryDate(), '2026-09-08');
   } finally {
      ItineraryClient.getItineraryDateRequest = original;
   }
});
