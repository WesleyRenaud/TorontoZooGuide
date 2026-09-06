import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { Strings } from '../../strings.js';

export class AttractionOutsideOperatingHoursConfirmation {
   static showAttractionOutsideOperatingHoursConfirmation({
      onConfirm,
      onCancel,
   } = {}) {
      const strings = Strings.itinerary.confirmation;

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.attractionOutsideOperatingHoursTitle,
         message: strings.attractionOutsideOperatingHoursMessage,
         confirmText: Strings.itinerary.actions.adjust,
         cancelText: Strings.itinerary.actions.cancel,
         mountEl: Popup.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
