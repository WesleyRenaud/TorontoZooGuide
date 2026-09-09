import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryPanelScheduleHandlersHelper } from '../../../../scripts/itinerary/panel/itineraryPanelScheduleHandlersHelper.js';

test('Test_NotifyItineraryUpdated_TestSuccessAndFailure_ExpectDispatch', async () => {
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });

   const itinerary = { date: '2026-09-08' };
   let dispatched = null;

   assert.equal(
      await ItineraryPanelScheduleHandlersHelper.notifyItineraryUpdated({
         result: { errorType: 'save_failed' },
         dispatchUpdated: (value) => { dispatched = value; },
         loadItinerary: async () => itinerary,
      }),
      false
   );
   assert.equal(dispatched, null);

   assert.equal(
      await ItineraryPanelScheduleHandlersHelper.notifyItineraryUpdated({
         result: { errorType: 'success' },
         dispatchUpdated: (value) => { dispatched = value; },
         loadItinerary: async () => itinerary,
      }),
      true
   );
   assert.equal(dispatched, itinerary);
});
