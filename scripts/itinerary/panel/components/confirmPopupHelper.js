import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';

export class ConfirmPopupHelper {
   static createConfirmPopupBody(message, doNotShowAgainLabel) {
      const body = ItineraryPanelHelper.el('div', 'tzg-popup-confirm-body');

      body.appendChild(
         ItineraryPanelHelper.el('div', 'tzg-popup-message', message)
      );

      if (!doNotShowAgainLabel) {
         return body;
      }

      const label = ItineraryPanelHelper.el('label', 'toggle-row tzg-popup-do-not-show-again');
      const checkbox = ItineraryPanelHelper.el('input');
      checkbox.type = 'checkbox';

      label.append(checkbox, ` ${doNotShowAgainLabel}`);
      body.appendChild(label);

      return {
         body,
         checkbox,
      };
   }
}
