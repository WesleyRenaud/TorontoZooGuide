import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';
import {
   buildClosedAttractionMessage,
   buildAttractionImageSrc,
   getAttractionId,
   getAttractionInfoLink,
   getAttractionSubtitle,
   getAttractionTitle,
   makeAttractionSelection,
   migrateStoredAttractions,
   shouldConfirmClosedAttraction,
} from './attractionSelector/model.js';
import { renderIncludeClosedAttractionsToggle } from './attractionSelector/view.js';

const STORAGE_KEY = 'tzg.itineraryAttractions';

function promptForClosedAttractionSelection(row, proceed) {
   showItineraryConfirmPopup({
      title: 'Attraction May Be Closed',
      message: buildClosedAttractionMessage(row),
      confirmText: 'Add',
      cancelText: 'Cancel',
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

      topTitle: 'Itinerary Builder',
      h1: 'Add Attractions',
      subtitle: 'Search and add attractions to your plan.',
      emptyText: 'No attractions found.',

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
