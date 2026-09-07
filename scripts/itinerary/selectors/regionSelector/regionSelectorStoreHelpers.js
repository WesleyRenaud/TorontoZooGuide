import { ItinerarySearchContext } from '../../itinerarySearchContext.js';
import { SearchContext } from '../../../search/searchContext.js';
import { VisitDateRules } from '../../../visitDates/visitDateRules.js';

export class RegionSelectorStoreHelpers {
   static async resolveAnimalsByExhibitQueryContext() {
      let context = await ItinerarySearchContext.getItineraryDateSearchContext();

      if (!context.month || context.day == null) {
         context = await SearchContext.buildDateSearchContext(VisitDateRules.toISODate(VisitDateRules.getToday()));
      }

      return context;
   }
}
