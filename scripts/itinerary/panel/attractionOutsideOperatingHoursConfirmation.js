import { ConfirmPopup } from './components/confirmPopup.js';
import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { Strings } from '../../strings.js';

export class AttractionOutsideOperatingHoursConfirmation {
   static showAttractionOutsideOperatingHoursConfirmation({
      onConfirm,
      onCancel,
   } = {}) {
      ConfirmPopup.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.attractionOutsideOperatingHoursTitle,
         message: Strings.itinerary.confirmation.attractionOutsideOperatingHoursMessage,
         confirmText: Strings.itinerary.actions.adjust,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: ItineraryPanelPopup.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
