import { ConfirmFragment } from '../panel/components/confirmFragment.js';
import { Strings } from '../../strings.js';
import { TransportationSelectorModel } from './transportationSelector/transportationSelectorModel.js';

export class TransportationSelectorPrompter {
   static promptForAddAsTransportationSelection(row, proceed) {
      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.addAsTransportationTitle,
         message: TransportationSelectorModel.buildAddAsTransportationMessage(row),
         confirmText: Strings.itinerary.actions.confirm,
         cancelText: Strings.animalsPage.back,
         onConfirm: proceed,
      });
   }
}
