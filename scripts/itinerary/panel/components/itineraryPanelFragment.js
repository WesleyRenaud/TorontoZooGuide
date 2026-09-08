import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { ItineraryPanelPopupBuilder } from './itineraryPanelPopupBuilder.js';
import { Strings } from '../../../strings.js';

export class ItineraryPanelFragment {
   static getItineraryOverlayMountEl() {
      return document.getElementById('itineraryFlow')
         ?? document.querySelector('.map-container');

   }

   static getItineraryPanelMountEl() {
      return document.querySelector('.itinerary-panel');

   }

   static createItineraryPopupLayout({
      popupClassName = '',
      title = Strings.common.headsUp,
      message = '',
      bodyContent = null,
      actionsClassName = '',
      actionButtons = [],
      showCloseButton = false,
      closeAriaLabel = Strings.itinerary.aria.closeBuilder,
   } = {}) {
      const root = ItineraryPanelHelper.el('div', ItineraryPanelPopupBuilder.joinClassNames('tzg-popup', popupClassName));
      const overlay = ItineraryPanelHelper.el('div', 'itin-overlay');

      const card = ItineraryPanelHelper.el('section', 'itin-card tzg-popup-card');
      card.setAttribute('role', 'dialog');
      card.setAttribute('aria-modal', 'true');
      card.setAttribute('aria-label', title);

      const topbar = ItineraryPanelHelper.el(
         'div',
         showCloseButton
            ? 'itin-card-topbar itin-card-topbar-with-close'
            : 'itin-card-topbar'
      );
      topbar.appendChild(
         ItineraryPanelHelper.el('div', 'itin-top-title', title)
      );

      const closeButton = showCloseButton
         ? ItineraryPanelHelper.el('button', 'itin-close', Strings.common.closeSymbol)
         : null;

      if (closeButton) {
         closeButton.type = 'button';
         closeButton.setAttribute('aria-label', closeAriaLabel);
         topbar.appendChild(closeButton);
      }

      const body = ItineraryPanelHelper.el('div', 'itin-card-body tzg-popup-body');

      if (bodyContent) {
         body.appendChild(bodyContent);
      }
      else {
         body.appendChild(
            ItineraryPanelHelper.el('div', 'tzg-popup-message', message)
         );
      }

      const actions = ItineraryPanelHelper.el('div', 'itin-card-actions');
      const actionsRight = ItineraryPanelHelper.el(
         'div',
         ItineraryPanelPopupBuilder.joinClassNames('itin-actions-right', actionsClassName)
      );

      const buttonEls = {};

      actionButtons.forEach((buttonConfig) => {
         const buttonEl = ItineraryPanelPopupBuilder.createPopupButton(buttonConfig);

         if (buttonConfig?.key) {
            buttonEls[buttonConfig.key] = buttonEl;
         }

         actionsRight.appendChild(buttonEl);
      });

      actions.appendChild(actionsRight);
      card.append(topbar, body, actions);
      overlay.appendChild(card);
      root.appendChild(overlay);

      return {
         root,
         overlay,
         buttonEls,
         closeButton,
      };

   }

   static mountDismissablePopup({
      mountEl = document.body,
      root,
      overlay,
      initialFocusEl = null,
      onDismiss = null,
      dismissOnOverlayClick = true,
      dismissOnEscape = true,
   } = {}) {
      if (!mountEl || !root || !overlay) {
         return {
            close() {},
            dismiss() {},
         };
      }

      let isClosed = false;

      function cleanup() {
         if (isClosed) {
            return false;
         }

         isClosed = true;
         document.removeEventListener('keydown', onKeyDown);

         if (root.__tzgPopupCleanup === close) {
            delete root.__tzgPopupCleanup;
         }

         root.remove();
         return true;
      }

      function close() {
         cleanup();
      }

      function dismiss() {
         if (!cleanup()) {
            return;
         }

         onDismiss?.();
      }

      function onKeyDown(event) {
         if (!dismissOnEscape || event.key !== 'Escape') {
            return;
         }

         event.preventDefault();
         dismiss();
      }

      if (dismissOnOverlayClick) {
         overlay.addEventListener('click', (event) => {
            if (event.target === overlay) {
               dismiss();
            }
         });
      }

      root.__tzgPopupCleanup = close;

      mountEl.appendChild(root);
      document.addEventListener('keydown', onKeyDown);

      requestAnimationFrame(() => {
         initialFocusEl?.focus?.();
      });

      return {
         close,
         dismiss,
      };
   }
}
