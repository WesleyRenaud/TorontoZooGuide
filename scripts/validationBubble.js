import { ItineraryPanelDom } from './itinerary/panel/itineraryPanelDom.js';
import { ValidationBubbleHelpers } from './validationBubbleHelpers.js';

export class ValidationBubble {
   static createValidationBubbleController({
      anchorEl,
      classNames = {},
      iconText = '!',
   } = {}) {
      const classes = ValidationBubbleHelpers.resolveClassNames(classNames);
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
               ValidationBubbleHelpers.positionValidationBubble(bubbleEl, anchorEl);
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

         bubbleEl = ItineraryPanelDom.el('div', classes.bubble);
         bubbleEl.setAttribute('role', 'alert');

         const icon = ItineraryPanelDom.el('span', classes.icon, iconText);
         icon.setAttribute('aria-hidden', 'true');
         bubbleEl.appendChild(icon);
         bubbleEl.appendChild(ItineraryPanelDom.el('span', classes.text, message));
         document.body.appendChild(bubbleEl);
         ValidationBubbleHelpers.positionValidationBubble(bubbleEl, anchorEl);
         bindRepositionListeners();
      }

      return {
         dismiss,
         show,
      };
   }
}
