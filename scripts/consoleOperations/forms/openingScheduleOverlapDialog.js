import { createWarningIcon } from '../../assets/warningIcon.js';
import { mountDismissablePopup } from '../../itinerary/panel/components/popup.js';
import { el } from '../../itinerary/panel/dom.js';
import { OPENING_SCHEDULE_OVERLAP_RESOLUTION } from './openingScheduleOverlap.js';
import { APP_STRINGS } from '../../strings.js';

const ROOT_SELECTOR = '.console-overlap-dialog-root';

function createDialogWarningIcon() {
   const warning = el(
      'span',
      'itin-likelihood-warning medium console-overlap-dialog-icon-wrap'
   );
   const svg = createWarningIcon({
      className: 'itin-warning-icon console-overlap-dialog-icon',
      ariaHidden: true,
      focusable: 'false',
   });

   warning.appendChild(svg);
   return warning;
}

function createDialogButton(className, text) {
   const button = el('button', className, text);
   button.type = 'button';
   return button;
}

function createDialogLayout() {
   const root = el('div', 'console-overlap-dialog-root');
   const overlay = el('div', 'console-overlap-dialog-overlay');
   const card = el('section', 'console-overlap-dialog-card');
   const header = el('div', 'console-overlap-dialog-header');
   const body = el('div', 'console-overlap-dialog-body');
   const actions = el('div', 'console-overlap-dialog-actions');
   const cancelButton = createDialogButton(
      'console-overlap-dialog-cancel',
      APP_STRINGS.itinerary.actions.cancel
   );
   const replaceButton = createDialogButton(
      'console-overlap-dialog-action',
      APP_STRINGS.confirm.deleteOldSchedules
   );
   const trimButton = createDialogButton(
      'console-overlap-dialog-action',
      APP_STRINGS.confirm.trimOldSchedules
   );

   card.setAttribute('role', 'dialog');
   card.setAttribute('aria-modal', 'true');
   card.setAttribute('aria-label', APP_STRINGS.confirm.openingScheduleOverlapTitle);

   header.append(
      createDialogWarningIcon(),
      el('h2', 'console-overlap-dialog-title', APP_STRINGS.confirm.openingScheduleOverlapTitle)
   );
   body.appendChild(
      el('p', 'console-overlap-dialog-message', APP_STRINGS.confirm.openingScheduleOverlapMessage)
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

export function showOpeningScheduleOverlapDialog() {
   document.querySelector(ROOT_SELECTOR)?.__tzgPopupCleanup?.();

   return new Promise((resolve) => {
      const { root, overlay, buttons } = createDialogLayout();
      const { close, dismiss } = mountDismissablePopup({
         mountEl: document.body,
         root,
         overlay,
         initialFocusEl: buttons.cancel,
         onDismiss: () => resolve(null),
      });

      buttons.cancel.addEventListener('click', dismiss);

      buttons.replace.addEventListener('click', () => {
         close();
         resolve(OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE);
      });

      buttons.trim.addEventListener('click', () => {
         close();
         resolve(OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM);
      });
   });
}
