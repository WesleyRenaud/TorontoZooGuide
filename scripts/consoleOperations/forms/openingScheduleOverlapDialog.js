import { WarningIcon } from '../../assets/warningIcon.js';
import { Popup } from '../../itinerary/panel/components/popup.js';
import { Dom } from '../../itinerary/panel/dom.js';
import { OpeningScheduleOverlap } from './openingScheduleOverlap.js';
import { Strings } from '../../strings.js';

const ROOT_SELECTOR = '.console-overlap-dialog-root';

function createDialogWarningIcon() {
   const warning = Dom.el(
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
   const button = Dom.el('button', className, text);
   button.type = 'button';
   return button;
}

function createDialogLayout() {
   const root = Dom.el('div', 'console-overlap-dialog-root');
   const overlay = Dom.el('div', 'console-overlap-dialog-overlay');
   const card = Dom.el('section', 'console-overlap-dialog-card');
   const header = Dom.el('div', 'console-overlap-dialog-header');
   const body = Dom.el('div', 'console-overlap-dialog-body');
   const actions = Dom.el('div', 'console-overlap-dialog-actions');
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
      Dom.el('h2', 'console-overlap-dialog-title', Strings.confirm.openingScheduleOverlapTitle)
   );
   body.appendChild(
      Dom.el('p', 'console-overlap-dialog-message', Strings.confirm.openingScheduleOverlapMessage)
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
         const { close, dismiss } = Popup.mountDismissablePopup({
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
