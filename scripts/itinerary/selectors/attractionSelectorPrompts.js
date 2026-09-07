import { AttractionSelectorModel } from './attractionSelector/attractionSelectorModel.js';
import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { Strings } from '../../strings.js';

export class AttractionSelectorPrompts {
   static promptForClosedAttractionSelection(row, proceed) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.attractionMayBeClosed,
         message: AttractionSelectorModel.buildClosedAttractionMessage(row),
         confirmText: Strings.itinerary.actions.add,
         cancelText: Strings.itinerary.actions.cancel,
         onConfirm: proceed,
      });
   }

   static promptForAlsoTransportationAttractionSelection(row, proceed) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.attractionAlsoTransportationTitle,
         message: AttractionSelectorModel.buildAlsoTransportationAttractionMessage(row),
         confirmText: Strings.itinerary.actions.confirm,
         cancelText: Strings.animalsPage.back,
         onConfirm: proceed,
      });
   }
}
