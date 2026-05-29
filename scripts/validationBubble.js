import { el } from './itinerary/panel/dom.js';

const DEFAULT_CLASS_NAMES = {
   bubble: 'tzg-validation-bubble',
   icon: 'tzg-validation-bubble-icon',
   text: 'tzg-validation-bubble-text',
};

const VIEWPORT_PADDING = 12;
const ANCHOR_GAP = 12;
const ARROW_SIZE = 14;

function resolveClassNames(classNames = {}) {
   return {
      ...DEFAULT_CLASS_NAMES,
      ...classNames,
   };
}

function positionValidationBubble(bubbleEl, anchorEl) {
   const anchorRect = anchorEl.getBoundingClientRect();
   const bubbleRect = bubbleEl.getBoundingClientRect();
   const viewportWidth = window.innerWidth;
   const viewportHeight = window.innerHeight;

   let left = anchorRect.left;
   const maxLeft = viewportWidth - bubbleRect.width - VIEWPORT_PADDING;

   if (left > maxLeft) {
      left = Math.max(VIEWPORT_PADDING, maxLeft);
   }

   let top = anchorRect.bottom + ANCHOR_GAP;
   const maxTop = viewportHeight - bubbleRect.height - VIEWPORT_PADDING;

   if (top > maxTop) {
      top = Math.max(
         VIEWPORT_PADDING,
         anchorRect.top - bubbleRect.height - ANCHOR_GAP
      );
   }

   bubbleEl.style.left = `${left}px`;
   bubbleEl.style.top = `${top}px`;

   const anchorCenter = anchorRect.left + (anchorRect.width / 2);
   const arrowLeft = Math.max(
      ARROW_SIZE,
      Math.min(
         bubbleRect.width - ARROW_SIZE,
         anchorCenter - left
      )
   );

   bubbleEl.style.setProperty(
      '--tzg-validation-bubble-arrow-left',
      `${arrowLeft}px`
   );
}

export function createValidationBubbleController({
   anchorEl,
   classNames = {},
   iconText = '!',
} = {}) {
   const classes = resolveClassNames(classNames);
   let bubbleEl = null;
   let repositionHandler = null;

   function unbindRepositionListeners() {
      if (!repositionHandler) {
         return;
      }

      window.removeEventListener('scroll', repositionHandler, true);
      window.removeEventListener('resize', repositionHandler);
      repositionHandler = null;
   }

   function bindRepositionListeners() {
      unbindRepositionListeners();
      repositionHandler = () => {
         if (bubbleEl && anchorEl) {
            positionValidationBubble(bubbleEl, anchorEl);
         }
      };

      window.addEventListener('scroll', repositionHandler, true);
      window.addEventListener('resize', repositionHandler);
   }

   function dismiss() {
      unbindRepositionListeners();
      bubbleEl?.remove();
      bubbleEl = null;
   }

   function show(message) {
      if (!anchorEl || !message) {
         return;
      }

      dismiss();

      bubbleEl = el('div', classes.bubble);
      bubbleEl.setAttribute('role', 'alert');

      const icon = el('span', classes.icon, iconText);
      icon.setAttribute('aria-hidden', 'true');
      bubbleEl.appendChild(icon);
      bubbleEl.appendChild(el('span', classes.text, message));
      document.body.appendChild(bubbleEl);
      positionValidationBubble(bubbleEl, anchorEl);
      bindRepositionListeners();
   }

   return {
      dismiss,
      show,
   };
}
