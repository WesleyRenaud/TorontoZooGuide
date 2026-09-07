import { ConfirmPopup } from './components/confirmPopup.js';
import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { RemoveItineraryItemConfirmationHelpers } from './removeItineraryItemConfirmationHelpers.js';
import { Strings } from '../../strings.js';

export class RemoveItineraryItemConfirmation {
   static showRemoveItineraryItemConfirmation({
      itemType = null,
      key = null,
      onConfirm,
      onCancel,
   } = {}) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.removeItemTitle,
         message: RemoveItineraryItemConfirmationHelpers.removeConfirmationMessage(itemType, key),
         confirmText: Strings.itinerary.dayPlanner.remove,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelPopup.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
