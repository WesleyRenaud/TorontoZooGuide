import { createItinerarySelectorController } from './createSelectorController.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { APP_STRINGS } from '../../strings.js';
import { TransportationSelectorModel } from './transportationSelector/transportationSelectorModel.js';

const STORAGE_KEY = 'tzg.itineraryTransportations';

function promptForAddAsTransportationSelection(row, proceed) {
   ConfirmPopup.showItineraryConfirmPopup({
      title: APP_STRINGS.itinerary.confirmation.addAsTransportationTitle,
      message: TransportationSelectorModel.buildAddAsTransportationMessage(row),
      confirmText: APP_STRINGS.itinerary.actions.confirm,
      cancelText: APP_STRINGS.animalsPage.back,
      onConfirm: proceed,
   });
}

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
      migrateSelected: TransportationSelectorModel.migrateStoredTransportations,

      getContext: () => ItinerarySearchContext.getItineraryDateSearchContext({ includeTemp: false }),

      buildSearchPayload: query => ({
         query,
         includeTransportations: true,
      }),

      extractRows: response => (
         Array.isArray(response.transportations) ? response.transportations : []
      ),

      getId: TransportationSelectorModel.getTransportationId,
      getTitle: TransportationSelectorModel.getTransportationTitle,
      getSubtitle: TransportationSelectorModel.getTransportationSubtitle,
      getImageSrc: TransportationSelectorModel.buildTransportationImageSrc,
      getInfoLink: () => null,
      onTitleClick: (row) => {
         const link = TransportationSelectorModel.getTransportationInfoLink(row);

         if (link) {
            window.open(link, '_blank');
         }
      },
      shouldEnableTitleClick: (row) => Boolean(TransportationSelectorModel.getTransportationInfoLink(row)),

      makeSelection: TransportationSelectorModel.makeTransportationSelection,

      topTitle: APP_STRINGS.itinerary.selectors.builderTitle,
      h1: APP_STRINGS.itinerary.selectors.titleTransportations,
      subtitle: APP_STRINGS.itinerary.selectors.transportationSubtitle,
      emptyText: APP_STRINGS.itinerary.emptyText.transportations,

      onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
         if (!TransportationSelectorModel.shouldConfirmAddAsTransportation({
            row,
            isSelected,
         })) {
            proceed();
            return;
         }

         promptForAddAsTransportationSelection(row, proceed);
      },
   });
}
