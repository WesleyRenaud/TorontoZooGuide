import {
   buildAttractionImageSrc,
   buildClosedAttractionMessage,
   getAttractionId,
   getAttractionInfoLink,
   getAttractionSubtitle,
   getAttractionTitle,
   makeAttractionSelection,
   migrateStoredAttractions,
   shouldConfirmClosedAttraction,
} from './attractionSelector/model.js';
import { renderIncludeClosedAttractionsToggle } from './attractionSelector/view.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';
import { APP_STRINGS } from '../../strings.js';

const STORAGE_KEY = 'tzg.itineraryAttractions';

function promptForClosedAttractionSelection(row, proceed) {
   showItineraryConfirmPopup({
      title: APP_STRINGS.itinerary.confirmation.attractionMayBeClosed,
      message: buildClosedAttractionMessage(row),
      confirmText: APP_STRINGS.itinerary.actions.add,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      onConfirm: proceed,
   });
}

export function createItineraryAttractionSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
   onClose,
} = {}) {
   let includeClosedAttractions = false;

   return createItinerarySelectorController({
      mountEl,
      onNext,
      onPrev,
      onFinish,
      onClose,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateStoredAttractions,

      getContext: () => getItineraryDateSearchContext({ includeTemp: false }),

      buildSearchPayload: query => ({
         query,
         includeAttractions: true,
         includeClosedAttractions,
      }),

      extractRows: response => response.attractions,

      getId: getAttractionId,
      getTitle: getAttractionTitle,
      getSubtitle: getAttractionSubtitle,
      getImageSrc: buildAttractionImageSrc,
      getInfoLink: getAttractionInfoLink,

      makeSelection: makeAttractionSelection,

      topTitle: APP_STRINGS.itinerary.selectors.builderTitle,
      h1: APP_STRINGS.itinerary.selectors.titleAttractions,
      subtitle: APP_STRINGS.itinerary.selectors.attractionSubtitle,
      emptyText: APP_STRINGS.itinerary.emptyText.attractions,

      onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
         if (!shouldConfirmClosedAttraction({
            row,
            isSelected,
            includeClosedAttractions,
         })) {
            proceed();
            return;
         }

         promptForClosedAttractionSelection(row, proceed);
      },

      renderExtraControls: ({ bodyEl, rerunSearch }) => {
         includeClosedAttractions = false;
         renderIncludeClosedAttractionsToggle({
            bodyEl,
            rerunSearch,
            onChange: (checked) => {
               includeClosedAttractions = checked;
            },
         });
      },
   });
}
