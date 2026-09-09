import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { SelectorControllerFactory } from './selectorControllerFactory.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../strings.js';
import { TransportationSelectorModel } from './transportationSelector/transportationSelectorModel.js';
import { TransportationSelectorPrompter } from './transportationSelectorPrompter.js';

export class TransportationSelector {
   static STORAGE_KEY = 'tzg.itineraryTransportations';

   static createItineraryTransportationSelectorController({
   mountEl,
   onPrev,
   onFinish,
   onClose,
} = {}) {
      return SelectorControllerFactory.createItinerarySelectorController({
         mountEl,
         onPrev,
         onFinish,
         onClose,
         hideNextButton: true,

         storageKey: TransportationSelector.STORAGE_KEY,
         migrateSelected: TransportationSelectorModel.migrateStoredTransportations,

         getContext: () => ItinerarySearchContext.getItineraryDateSearchContext({ includeTemp: false }),

         buildSearchPayload: query => ({
            query,
            includeTransportations: true,
         }),

         extractRows: response => {
            const rows = response[ScheduleItemKind.TRANSPORTATION.itemType];

            return Array.isArray(rows) ? rows : [];
         },

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

         topTitle: Strings.itinerary.selectors.builderTitle,
         h1: Strings.itinerary.selectors.titleTransportations,
         subtitle: Strings.itinerary.selectors.transportationSubtitle,
         emptyText: Strings.itinerary.emptyText.transportations,

         onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
            if (!TransportationSelectorModel.shouldConfirmAddAsTransportation({
               row,
               isSelected,
            })) {
               proceed();
               return;
            }

            TransportationSelectorPrompter.promptForAddAsTransportationSelection(row, proceed);
         },
      });
   }
}
