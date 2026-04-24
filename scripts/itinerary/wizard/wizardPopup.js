import {
   createItineraryPopupLayout,
   mountDismissablePopup,
} from '../panel/components/popup.js';

export function showItineraryWizardPopup({
   mountEl,
   title = 'Heads up',
   message = '',
   buttonText = 'OK',
} = {}) {
   if (!mountEl) return;

   const existingPopup = mountEl.querySelector('.tzg-popup');
   existingPopup?.__tzgPopupCleanup?.();
   existingPopup?.remove();

   const {
      root,
      overlay,
      buttonEls,
   } = createItineraryPopupLayout({
      title,
      message,
      actionButtons: [
         {
            key: 'ok',
            className: 'itin-next tzg-popup-ok',
            text: buttonText,
         },
      ],
   });

   const { close } = mountDismissablePopup({
      mountEl,
      root,
      overlay,
      initialFocusEl: buttonEls.ok,
   });

   buttonEls.ok?.addEventListener('click', close);
}
