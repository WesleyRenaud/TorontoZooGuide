import { ConfirmFragment } from './components/confirmFragment.js';
import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { Strings } from '../../strings.js';

export class AttractionOutsideOperatingHoursFragment {
   static showAttractionOutsideOperatingHoursConfirmation({
      onConfirm,
      onCancel,
   } = {}) {
      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.attractionOutsideOperatingHoursTitle,
         message: Strings.itinerary.confirmation.attractionOutsideOperatingHoursMessage,
         confirmText: Strings.itinerary.actions.adjust,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelFragment.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
