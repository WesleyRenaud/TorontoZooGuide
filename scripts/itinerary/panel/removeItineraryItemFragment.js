import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { RemoveItineraryItemConfirmationHelper } from './removeItineraryItemConfirmationHelper.js';
import { Strings } from '../../strings.js';

export class RemoveItineraryItemFragment {
   static showRemoveItineraryItemConfirmation({
      itemType = null,
      key = null,
      onConfirm,
      onCancel,
   } = {}) {
      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.removeItemTitle,
         message: RemoveItineraryItemConfirmationHelper.removeConfirmationMessage(itemType, key),
         confirmText: Strings.itinerary.dayPlanner.remove,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelFragment.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
