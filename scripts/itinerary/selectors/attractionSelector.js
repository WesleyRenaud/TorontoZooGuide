import { AttractionSelectorModel } from './attractionSelector/attractionSelectorModel.js';
import { View } from './attractionSelector/view.js';
import { CreateSelectorController } from './createSelectorController.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { APP_STRINGS } from '../../strings.js';

const STORAGE_KEY = 'tzg.itineraryAttractions';

function promptForClosedAttractionSelection(row, proceed) {
   ConfirmPopup.showItineraryConfirmPopup({
      title: APP_STRINGS.itinerary.confirmation.attractionMayBeClosed,
      message: AttractionSelectorModel.buildClosedAttractionMessage(row),
      confirmText: APP_STRINGS.itinerary.actions.add,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      onConfirm: proceed,
   });
}

function promptForAlsoTransportationAttractionSelection(row, proceed) {
   ConfirmPopup.showItineraryConfirmPopup({
      title: APP_STRINGS.itinerary.confirmation.attractionAlsoTransportationTitle,
      message: AttractionSelectorModel.buildAlsoTransportationAttractionMessage(row),
      confirmText: APP_STRINGS.itinerary.actions.confirm,
      cancelText: APP_STRINGS.animalsPage.back,
      onConfirm: proceed,
   });
}

export class AttractionSelector {
   static createItineraryAttractionSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
   onClose,
} = {}) {
      let includeClosedAttractions = false;

      return CreateSelectorController.createItinerarySelectorController({
         mountEl,
         onNext,
         onPrev,
         onFinish,
         onClose,

         storageKey: STORAGE_KEY,
         migrateSelected: AttractionSelectorModel.migrateStoredAttractions,

         getContext: () => ItinerarySearchContext.getItineraryDateSearchContext({ includeTemp: false }),

         buildSearchPayload: query => ({
            query,
            includeAttractions: true,
            includeClosedAttractions,
         }),

         extractRows: response => response.attractions,

         getId: AttractionSelectorModel.getAttractionId,
         getTitle: AttractionSelectorModel.getAttractionTitle,
         getSubtitle: AttractionSelectorModel.getAttractionSubtitle,
         getImageSrc: AttractionSelectorModel.buildAttractionImageSrc,
         getInfoLink: () => null,
         onTitleClick: (row) => {
            const link = AttractionSelectorModel.getAttractionInfoLink(row);

            if (link) {
               window.open(link, '_blank');
            }
         },
         shouldEnableTitleClick: (row) => Boolean(AttractionSelectorModel.getAttractionInfoLink(row)),

         makeSelection: AttractionSelectorModel.makeAttractionSelection,

         topTitle: APP_STRINGS.itinerary.selectors.builderTitle,
         h1: APP_STRINGS.itinerary.selectors.titleAttractions,
         subtitle: APP_STRINGS.itinerary.selectors.attractionSubtitle,
         emptyText: APP_STRINGS.itinerary.emptyText.attractions,

         onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
            const continueAdd = () => {
               if (!AttractionSelectorModel.shouldConfirmAlsoTransportationAttraction({
                  row,
                  isSelected,
               })) {
                  proceed();
                  return;
               }

               promptForAlsoTransportationAttractionSelection(row, proceed);
            };

            if (!AttractionSelectorModel.shouldConfirmClosedAttraction({
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
            View.renderIncludeClosedAttractionsToggle({
               bodyEl,
               rerunSearch,
               onChange: (checked) => {
                  includeClosedAttractions = checked;
               },
            });
         },
      });
   }
}
