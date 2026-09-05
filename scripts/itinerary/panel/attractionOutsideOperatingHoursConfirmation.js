import { ConfirmPopup } from './components/confirmPopup.js';
import { Popup } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export class AttractionOutsideOperatingHoursConfirmation {
   static showAttractionOutsideOperatingHoursConfirmation({
      onConfirm,
      onCancel,
   } = {}) {
      const strings = APP_STRINGS.itinerary.confirmation;

      ConfirmPopup.showItineraryConfirmPopup({
         title: strings.attractionOutsideOperatingHoursTitle,
         message: strings.attractionOutsideOperatingHoursMessage,
         confirmText: APP_STRINGS.itinerary.actions.adjust,
         cancelText: APP_STRINGS.itinerary.actions.cancel,
         mountEl: Popup.getItineraryPanelMountEl() ?? document.body,
         onConfirm,
         onCancel,
      });
   }
}
