import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { APP_STRINGS } from '../../strings.js';
import {
   buildTransportationImageSrc,
   getTransportationId,
   getTransportationInfoLink,
   getTransportationSubtitle,
   getTransportationTitle,
   makeTransportationSelection,
   migrateStoredTransportations,
} from './transportationSelector/model.js';

const STORAGE_KEY = 'tzg.itineraryTransportations';

export function createItineraryTransportationSelectorController({
   mountEl,
   onPrev,
   onFinish,
   onClose,
} = {}) {
   return createItinerarySelectorController({
      mountEl,
      onPrev,
      onFinish,
      onClose,
      hideNextButton: true,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateStoredTransportations,

      getContext: () => getItineraryDateSearchContext({ includeTemp: false }),

      buildSearchPayload: query => ({
         query,
         includeTransportations: true,
      }),

      extractRows: response => (
         Array.isArray(response.transportations) ? response.transportations : []
      ),

      getId: getTransportationId,
      getTitle: getTransportationTitle,
      getSubtitle: getTransportationSubtitle,
      getImageSrc: buildTransportationImageSrc,
      getInfoLink: () => null,
      onTitleClick: (row) => {
         const link = getTransportationInfoLink(row);

         if (link) {
            window.open(link, '_blank');
         }
      },
      shouldEnableTitleClick: (row) => Boolean(getTransportationInfoLink(row)),

      makeSelection: makeTransportationSelection,

      topTitle: APP_STRINGS.itinerary.selectors.builderTitle,
      h1: APP_STRINGS.itinerary.selectors.titleTransportations,
      subtitle: APP_STRINGS.itinerary.selectors.transportationSubtitle,
      emptyText: APP_STRINGS.itinerary.emptyText.transportations,
   });
}
