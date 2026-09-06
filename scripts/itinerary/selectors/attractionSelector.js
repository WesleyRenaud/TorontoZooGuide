import { AttractionSelectorModel } from './attractionSelector/attractionSelectorModel.js';
import { View } from './attractionSelector/view.js';
import { CreateSelectorController } from './createSelectorController.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { Strings } from '../../strings.js';

const STORAGE_KEY = 'tzg.itineraryAttractions';

function promptForClosedAttractionSelection(row, proceed) {
   ConfirmPopup.showItineraryConfirmPopup({
      title: Strings.itinerary.confirmation.attractionMayBeClosed,
      message: AttractionSelectorModel.buildClosedAttractionMessage(row),
      confirmText: Strings.itinerary.actions.add,
      cancelText: Strings.itinerary.actions.cancel,
      onConfirm: proceed,
   });
}

function promptForAlsoTransportationAttractionSelection(row, proceed) {
   ConfirmPopup.showItineraryConfirmPopup({
      title: Strings.itinerary.confirmation.attractionAlsoTransportationTitle,
      message: AttractionSelectorModel.buildAlsoTransportationAttractionMessage(row),
      confirmText: Strings.itinerary.actions.confirm,
      cancelText: Strings.animalsPage.back,
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

         topTitle: Strings.itinerary.selectors.builderTitle,
         h1: Strings.itinerary.selectors.titleAttractions,
         subtitle: Strings.itinerary.selectors.attractionSubtitle,
         emptyText: Strings.itinerary.emptyText.attractions,

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
