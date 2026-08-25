import { el } from '../dom.js';
import { APP_STRINGS } from '../../../strings.js';

export function getItineraryOverlayMountEl() {
   return document.getElementById('itineraryFlow')
      ?? document.querySelector('.map-container');
}

export function getItineraryPanelMountEl() {
   return document.querySelector('.itinerary-panel');
}

function joinClassNames(...classNames) {
   return classNames.filter(Boolean).join(' ');
}

function createPopupButton({
   className,
   text,
} = {}) {
   const button = el('button', className, text);
   button.type = 'button';
   return button;
}

export function createItineraryPopupLayout({
   popupClassName = '',
   title = APP_STRINGS.common.headsUp,
   message = '',
   bodyContent = null,
   actionsClassName = '',
   actionButtons = [],
   showCloseButton = false,
   closeAriaLabel = APP_STRINGS.itinerary.aria.closeBuilder,
} = {}) {
   const root = el('div', joinClassNames('tzg-popup', popupClassName));
   const overlay = el('div', 'itin-overlay');

   const card = el('section', 'itin-card tzg-popup-card');
   card.setAttribute('role', 'dialog');
   card.setAttribute('aria-modal', 'true');
   card.setAttribute('aria-label', title);

   const topbar = el(
      'div',
      showCloseButton
         ? 'itin-card-topbar itin-card-topbar-with-close'
         : 'itin-card-topbar'
   );
   topbar.appendChild(
      el('div', 'itin-top-title', title)
   );

   const closeButton = showCloseButton
      ? el('button', 'itin-close', APP_STRINGS.common.closeSymbol)
      : null;

   if (closeButton) {
      closeButton.type = 'button';
      closeButton.setAttribute('aria-label', closeAriaLabel);
      topbar.appendChild(closeButton);
   }

   const body = el('div', 'itin-card-body tzg-popup-body');

   if (bodyContent) {
      body.appendChild(bodyContent);
   }
   else {
      body.appendChild(
         el('div', 'tzg-popup-message', message)
      );
   }

   const actions = el('div', 'itin-card-actions');
   const actionsRight = el(
      'div',
      joinClassNames('itin-actions-right', actionsClassName)
   );

   const buttonEls = {};

   actionButtons.forEach((buttonConfig) => {
      const buttonEl = createPopupButton(buttonConfig);

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

export function mountDismissablePopup({
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
