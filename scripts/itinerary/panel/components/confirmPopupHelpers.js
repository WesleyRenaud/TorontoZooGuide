import { ItineraryPanelDom } from '../itineraryPanelDom.js';

export class ConfirmPopupHelpers {
   static createConfirmPopupBody(message, doNotShowAgainLabel) {
      const body = ItineraryPanelDom.el('div', 'tzg-popup-confirm-body');

      body.appendChild(
         ItineraryPanelDom.el('div', 'tzg-popup-message', message)
      );

      if (!doNotShowAgainLabel) {
         return body;
      }

      const label = ItineraryPanelDom.el('label', 'toggle-row tzg-popup-do-not-show-again');
      const checkbox = ItineraryPanelDom.el('input');
      checkbox.type = 'checkbox';

      label.append(checkbox, ` ${doNotShowAgainLabel}`);
      body.appendChild(label);

      return {
         body,
         checkbox,
      };
   }
}
