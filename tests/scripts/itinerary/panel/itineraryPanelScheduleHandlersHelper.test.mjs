import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryPanelScheduleHandlersHelper } from '../../../../scripts/itinerary/panel/itineraryPanelScheduleHandlersHelper.js';


test('Test_NotifyItineraryUpdated_TestSaveFailed_ExpectFalse', async () => {
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });
   const itinerary = { date: '2026-09-08' };
   let dispatched = null;

   const updated = await ItineraryPanelScheduleHandlersHelper.notifyItineraryUpdated({
      result: { errorType: ItineraryErrorType.SAVE_FAILED },
      dispatchUpdated: (value) => { dispatched = value; },
      loadItinerary: async () => itinerary,
   });

   assert.equal(updated, false);
   assert.equal(dispatched, null);
});


test('Test_NotifyItineraryUpdated_TestSuccess_ExpectDispatched', async () => {
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: [],
   });
   const itinerary = { date: '2026-09-08' };
   let dispatched = null;

   const updated = await ItineraryPanelScheduleHandlersHelper.notifyItineraryUpdated({
      result: { errorType: ItineraryErrorType.SUCCESS },
      dispatchUpdated: (value) => { dispatched = value; },
      loadItinerary: async () => itinerary,
   });

   assert.equal(updated, true);
   assert.equal(dispatched, itinerary);
});
