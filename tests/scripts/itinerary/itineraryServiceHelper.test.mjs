import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryClient } from '../../../scripts/api/itineraryClient.js';
import { DraftStore } from '../../../scripts/itinerary/draftStore.js';
import { ItineraryServiceHelper } from '../../../scripts/itinerary/itineraryServiceHelper.js';
import { createLocalStorageMock } from '../helpers/localStorageMock.mjs';


test('Test_FetchSavedItineraryVisitDate_TestResponse_ExpectStored', async () => {
   globalThis.localStorage = createLocalStorageMock();
   const original = ItineraryClient.getItineraryDateRequest;
   const date = '2026-09-08';
   ItineraryClient.getItineraryDateRequest = async () => ({ date });

   try {
      const fetched = await ItineraryServiceHelper.fetchSavedItineraryVisitDate();

      assert.equal(fetched, date);
      assert.equal(DraftStore.getStoredItineraryDate(), date);
   } finally {
      ItineraryClient.getItineraryDateRequest = original;
   }
});
