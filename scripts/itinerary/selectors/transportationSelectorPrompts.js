import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { Strings } from '../../strings.js';
import { TransportationSelectorModel } from './transportationSelector/transportationSelectorModel.js';

export class TransportationSelectorPrompts {
   static promptForAddAsTransportationSelection(row, proceed) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.addAsTransportationTitle,
         message: TransportationSelectorModel.buildAddAsTransportationMessage(row),
         confirmText: Strings.itinerary.actions.confirm,
         cancelText: Strings.animalsPage.back,
         onConfirm: proceed,
      });
   }
}
