import { WarningIcon } from '../../assets/warningIcon.js';
import { ItineraryPanelPopup } from '../../itinerary/panel/components/itineraryPanelPopup.js';
import { ItineraryPanelDom } from '../../itinerary/panel/itineraryPanelDom.js';
import { OpeningScheduleOverlap } from './openingScheduleOverlap.js';
import { Strings } from '../../strings.js';

const ROOT_SELECTOR = '.console-overlap-dialog-root';

function createDialogWarningIcon() {
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

function createDialogButton(className, text) {
   const button = ItineraryPanelDom.el('button', className, text);
   button.type = 'button';
   return button;
}

function createDialogLayout() {
   const root = ItineraryPanelDom.el('div', 'console-overlap-dialog-root');
   const overlay = ItineraryPanelDom.el('div', 'console-overlap-dialog-overlay');
   const card = ItineraryPanelDom.el('section', 'console-overlap-dialog-card');
   const header = ItineraryPanelDom.el('div', 'console-overlap-dialog-header');
   const body = ItineraryPanelDom.el('div', 'console-overlap-dialog-body');
   const actions = ItineraryPanelDom.el('div', 'console-overlap-dialog-actions');
   const cancelButton = createDialogButton(
      'console-overlap-dialog-cancel',
      Strings.itinerary.actions.cancel
   );
   const replaceButton = createDialogButton(
      'console-overlap-dialog-action',
      Strings.confirm.deleteOldSchedules
   );
   const trimButton = createDialogButton(
      'console-overlap-dialog-action',
      Strings.confirm.trimOldSchedules
   );

   card.setAttribute('role', 'dialog');
   card.setAttribute('aria-modal', 'true');
   card.setAttribute('aria-label', Strings.confirm.openingScheduleOverlapTitle);

   header.append(
      createDialogWarningIcon(),
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

export class OpeningScheduleOverlapDialog {
   static showOpeningScheduleOverlapDialog() {
      document.querySelector(ROOT_SELECTOR)?.__tzgPopupCleanup?.();

      return new Promise((resolve) => {
         const { root, overlay, buttons } = createDialogLayout();
         const { close, dismiss } = ItineraryPanelPopup.mountDismissablePopup({
            mountEl: document.body,
            root,
            overlay,
            initialFocusEl: buttons.cancel,
            onDismiss: () => resolve(null),
         });

         buttons.cancel.addEventListener('click', dismiss);

         buttons.replace.addEventListener('click', () => {
            close();
            resolve(OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE);
         });

         buttons.trim.addEventListener('click', () => {
            close();
            resolve(OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM);
         });
      });
   }
}
