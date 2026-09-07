import { WarningIcon } from '../../assets/warningIcon.js';
import { ItineraryPanelDom } from '../../itinerary/panel/itineraryPanelDom.js';
import { Strings } from '../../strings.js';

export class OpeningScheduleOverlapDialogBuilder {
   static createDialogWarningIcon() {
      const warning = ItineraryPanelDom.el(
         'span',
         'itin-likelihood-warning medium console-overlap-dialog-icon-wrap'
      );
      const svg = WarningIcon.createWarningIcon({
         className: 'itin-warning-icon console-overlap-dialog-icon',
         ariaHidden: true,
         focusable: 'false',
      });

      warning.appendChild(svg);
      return warning;
   }

   static createDialogButton(className, text) {
      const button = ItineraryPanelDom.el('button', className, text);
      button.type = 'button';
      return button;
   }

   static createDialogLayout() {
      const root = ItineraryPanelDom.el('div', 'console-overlap-dialog-root');
      const overlay = ItineraryPanelDom.el('div', 'console-overlap-dialog-overlay');
      const card = ItineraryPanelDom.el('section', 'console-overlap-dialog-card');
      const header = ItineraryPanelDom.el('div', 'console-overlap-dialog-header');
      const body = ItineraryPanelDom.el('div', 'console-overlap-dialog-body');
      const actions = ItineraryPanelDom.el('div', 'console-overlap-dialog-actions');
      const cancelButton = OpeningScheduleOverlapDialogBuilder.createDialogButton(
         'console-overlap-dialog-cancel',
         Strings.itinerary.actions.cancel
      );
      const replaceButton = OpeningScheduleOverlapDialogBuilder.createDialogButton(
         'console-overlap-dialog-action',
         Strings.confirm.deleteOldSchedules
      );
      const trimButton = OpeningScheduleOverlapDialogBuilder.createDialogButton(
         'console-overlap-dialog-action',
         Strings.confirm.trimOldSchedules
      );

      card.setAttribute('role', 'dialog');
      card.setAttribute('aria-modal', 'true');
      card.setAttribute('aria-label', Strings.confirm.openingScheduleOverlapTitle);

      header.append(
         OpeningScheduleOverlapDialogBuilder.createDialogWarningIcon(),
         ItineraryPanelDom.el('h2', 'console-overlap-dialog-title', Strings.confirm.openingScheduleOverlapTitle)
      );
      body.appendChild(
         ItineraryPanelDom.el('p', 'console-overlap-dialog-message', Strings.confirm.openingScheduleOverlapMessage)
      );
      actions.append(cancelButton, replaceButton, trimButton);
      card.append(header, body, actions);
      overlay.appendChild(card);
      root.appendChild(overlay);

      return {
         root,
         overlay,
         buttons: {
            cancel: cancelButton,
            replace: replaceButton,
            trim: trimButton,
         },
      };
   }
}
