import { WarningBuilder } from '../../assets/warningBuilder.js';
import { ItineraryPanelHelper } from '../../itinerary/panel/itineraryPanelHelper.js';
import { Strings } from '../../strings.js';

export class OpeningScheduleOverlapDialogBuilder {
   static createDialogWarningIcon() {
      const warning = ItineraryPanelHelper.el(
         'span',
         'itin-likelihood-warning medium console-overlap-dialog-icon-wrap'
      );
      const svg = WarningBuilder.createWarningIcon({
         className: 'itin-warning-icon console-overlap-dialog-icon',
         ariaHidden: true,
         focusable: 'false',
      });

      warning.appendChild(svg);
      return warning;
   }

   static createDialogButton(className, text) {
      const button = ItineraryPanelHelper.el('button', className, text);
      button.type = 'button';
      return button;
   }

   static createDialogLayout() {
      const root = ItineraryPanelHelper.el('div', 'console-overlap-dialog-root');
      const overlay = ItineraryPanelHelper.el('div', 'console-overlap-dialog-overlay');
      const card = ItineraryPanelHelper.el('section', 'console-overlap-dialog-card');
      const header = ItineraryPanelHelper.el('div', 'console-overlap-dialog-header');
      const body = ItineraryPanelHelper.el('div', 'console-overlap-dialog-body');
      const actions = ItineraryPanelHelper.el('div', 'console-overlap-dialog-actions');
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
         ItineraryPanelHelper.el('h2', 'console-overlap-dialog-title', Strings.confirm.openingScheduleOverlapTitle)
      );
      body.appendChild(
         ItineraryPanelHelper.el('p', 'console-overlap-dialog-message', Strings.confirm.openingScheduleOverlapMessage)
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
