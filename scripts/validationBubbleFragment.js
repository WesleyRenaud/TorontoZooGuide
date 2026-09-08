import { ItineraryPanelHelper } from './itinerary/panel/itineraryPanelHelper.js';
import { ValidationBubbleHelper } from './validationBubbleHelper.js';

export class ValidationBubbleFragment {
   static createValidationBubbleController({
      anchorEl,
      classNames = {},
      iconText = '!',
   } = {}) {
      const classes = ValidationBubbleHelper.resolveClassNames(classNames);
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
               ValidationBubbleHelper.positionValidationBubble(bubbleEl, anchorEl);
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

         bubbleEl = ItineraryPanelHelper.el('div', classes.bubble);
         bubbleEl.setAttribute('role', 'alert');

         const icon = ItineraryPanelHelper.el('span', classes.icon, iconText);
         icon.setAttribute('aria-hidden', 'true');
         bubbleEl.appendChild(icon);
         bubbleEl.appendChild(ItineraryPanelHelper.el('span', classes.text, message));
         document.body.appendChild(bubbleEl);
         ValidationBubbleHelper.positionValidationBubble(bubbleEl, anchorEl);
         bindRepositionListeners();
      }

      return {
         dismiss,
         show,
      };
   }
}
