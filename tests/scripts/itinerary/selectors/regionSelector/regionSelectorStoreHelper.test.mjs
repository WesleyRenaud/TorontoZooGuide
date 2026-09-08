import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionSelectorStoreHelper } from '../../../../../scripts/itinerary/selectors/regionSelector/regionSelectorStoreHelper.js';
import { ItinerarySearchContext } from '../../../../../scripts/itinerary/itinerarySearchContext.js';
import { SearchContext } from '../../../../../scripts/search/searchContext.js';
import { VisitDateValidator } from '../../../../../scripts/visitDates/visitDateValidator.js';

test('Test_ResolveAnimalsByExhibitQueryContext_TestExistingDate_ExpectSameContext', async () => {
   const original = ItinerarySearchContext.getItineraryDateSearchContext;
   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({
      month: 'JUN',
      day: 15,
   });

   try {
      const context = await RegionSelectorStoreHelper.resolveAnimalsByExhibitQueryContext();
      assert.deepEqual(context, { month: 'JUN', day: 15 });
   } finally {
      ItinerarySearchContext.getItineraryDateSearchContext = original;
   }
});

test('Test_ResolveAnimalsByExhibitQueryContext_TestMissingDate_ExpectBuiltContext', async () => {
   const originalItinerary = ItinerarySearchContext.getItineraryDateSearchContext;
   const originalSearch = SearchContext.buildDateSearchContext;
   const originalToday = VisitDateValidator.getToday;
   const originalIso = VisitDateValidator.toISODate;

   ItinerarySearchContext.getItineraryDateSearchContext = async () => ({ month: null, day: null });
   VisitDateValidator.getToday = () => new Date(2026, 5, 15, 12);
   VisitDateValidator.toISODate = () => '2026-06-15';
   SearchContext.buildDateSearchContext = async (isoDate) => ({
      month: 'JUN',
      day: 15,
      isoDate,
   });

   try {
      const context = await RegionSelectorStoreHelper.resolveAnimalsByExhibitQueryContext();
      assert.deepEqual(context, {
         month: 'JUN',
         day: 15,
         isoDate: '2026-06-15',
      });
   } finally {
      ItinerarySearchContext.getItineraryDateSearchContext = originalItinerary;
      SearchContext.buildDateSearchContext = originalSearch;
      VisitDateValidator.getToday = originalToday;
      VisitDateValidator.toISODate = originalIso;
   }
});
