import {
   buildAlsoTransportationAttractionMessage,
   buildAttractionImageSrc,
   buildClosedAttractionMessage,
   getAttractionId,
   getAttractionInfoLink,
   getAttractionSubtitle,
   getAttractionTitle,
   makeAttractionSelection,
   migrateStoredAttractions,
   shouldConfirmAlsoTransportationAttraction,
   shouldConfirmClosedAttraction,
} from './attractionSelector/model.js';
import { renderIncludeClosedAttractionsToggle } from './attractionSelector/view.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
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

function promptForAlsoTransportationAttractionSelection(row, proceed) {
   showItineraryConfirmPopup({
      title: APP_STRINGS.itinerary.confirmation.attractionAlsoTransportationTitle,
      message: buildAlsoTransportationAttractionMessage(row),
      confirmText: APP_STRINGS.itinerary.actions.confirm,
      cancelText: APP_STRINGS.animalsPage.back,
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

      getContext: () => ItinerarySearchContext.getItineraryDateSearchContext({ includeTemp: false }),

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
      getInfoLink: () => null,
      onTitleClick: (row) => {
         const link = getAttractionInfoLink(row);

         if (link) {
            window.open(link, '_blank');
         }
      },
      shouldEnableTitleClick: (row) => Boolean(getAttractionInfoLink(row)),

      makeSelection: makeAttractionSelection,

      topTitle: APP_STRINGS.itinerary.selectors.builderTitle,
      h1: APP_STRINGS.itinerary.selectors.titleAttractions,
      subtitle: APP_STRINGS.itinerary.selectors.attractionSubtitle,
      emptyText: APP_STRINGS.itinerary.emptyText.attractions,

      onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
         const continueAdd = () => {
            if (!shouldConfirmAlsoTransportationAttraction({
               row,
               isSelected,
            })) {
               proceed();
               return;
            }

            promptForAlsoTransportationAttractionSelection(row, proceed);
         };

         if (!shouldConfirmClosedAttraction({
            row,
            isSelected,
            includeClosedAttractions,
         })) {
            continueAdd();
            return;
         }

         promptForClosedAttractionSelection(row, continueAdd);
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
