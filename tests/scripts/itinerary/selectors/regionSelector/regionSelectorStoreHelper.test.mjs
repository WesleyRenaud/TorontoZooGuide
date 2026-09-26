import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionSelectorStoreHelper } from '../../../../../scripts/itinerary/selectors/regionSelector/regionSelectorStoreHelper.js';
import { ItinerarySearchContext } from '../../../../../scripts/itinerary/itinerarySearchContext.js';
import { SearchContext } from '../../../../../scripts/search/searchContext.js';
import { VisitDateValidator } from '../../../../../scripts/visitDates/visitDateValidator.js';


test('Test_ResolveAnimalsByExhibitQueryContext_TestExistingDate_ExpectSameContext', async () => {
   const original = ItinerarySearchContext.getItineraryDateSearchContext;
   const existingContext = {
      month: 'JUN',
      day: 15,
   };
   ItinerarySearchContext.getItineraryDateSearchContext = async () => existingContext;

   try {
      const context = await RegionSelectorStoreHelper.resolveAnimalsByExhibitQueryContext();

      assert.deepEqual(context, existingContext);
   } finally {
      ItinerarySearchContext.getItineraryDateSearchContext = original;
   }
});


test('Test_ResolveAnimalsByExhibitQueryContext_TestMissingDate_ExpectBuiltContext', async () => {
   const originalItinerary = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalSearch = SearchContext.buildDateSearchContext;
   const originalToday = VisitDateValidator.getToday;
   const originalIso = VisitDateValidator.toISODate;
   const isoDate = '2026-06-15';
   const month = 'JUN';
   const day = 15;
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ month: null, day: null });
   VisitDateValidator.getToday = () => new Date(2026, 5, day, 12);
   VisitDateValidator.toISODate = () => isoDate;
   SearchContext.buildDateSearchContext = async (value) => ({
      month,
      day,
      isoDate: value,
   });

   try {
      const context = await RegionSelectorStoreHelper.resolveAnimalsByExhibitQueryContext();

      assert.equal(context.month, month);
      assert.equal(context.day, day);
      assert.equal(context.isoDate, isoDate);
   } finally {
      ItinerarySearchContext.getItineraryDateSearchContext = originalItinerary;
      SearchContext.buildDateSearchContext = originalSearch;
      VisitDateValidator.getToday = originalToday;
      VisitDateValidator.toISODate = originalIso;
   }
});
