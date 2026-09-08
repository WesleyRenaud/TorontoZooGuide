import { ItinerarySearchContext } from '../../itinerarySearchContext.js';
import { SearchContext } from '../../../search/searchContext.js';
import { VisitDateValidator } from '../../../visitDates/visitDateValidator.js';

export class RegionSelectorStoreHelper {
   static async resolveAnimalsByExhibitQueryContext() {
      let context = await ItinerarySearchContext.getItineraryDateSearchContext();

      if (!context.month || context.day == null) {
         context = await SearchContext.buildDateSearchContext(VisitDateValidator.toISODate(VisitDateValidator.getToday()));
      }

      return context;
   }
}
