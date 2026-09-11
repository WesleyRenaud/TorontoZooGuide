import { ItineraryPanelHelper } from './itinerary/panel/itineraryPanelHelper.js';
import { TimelineLayoutConstants } from './shared/timelineLayoutConstants.js';
import { ValidationBubbleHelper } from './validationBubbleHelper.js';

export class ValidationBubbleFragment {
   static createValidationBubbleController({
      anchorEl,
      classNames = {},
      iconText = '!',
      dismissMs = TimelineLayoutConstants.DAY_PLANNER_ACTION_FEEDBACK_DISMISS_MS,
   } = {}) {
      const classes = ValidationBubbleHelper.resolveClassNames(classNames);
      let bubbleEl = null;
      let repositionHandler = null;
      let dismissTimeoutId = null;

      function clearDismissTimer() {
         if (dismissTimeoutId === null) {
            return;
         }

         clearTimeout(dismissTimeoutId);
         dismissTimeoutId = null;
      }

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
         clearDismissTimer();
         unbindRepositionListeners();

         const el = bubbleEl;
         bubbleEl = null;

         if (!el) {
            return;
         }

         if (typeof el.remove === 'function') {
            el.remove();
            return;
         }

         el.parentElement?.removeChild?.(el);
         el.parent?.removeChild?.(el);
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

         if (dismissMs > 0) {
            dismissTimeoutId = setTimeout(() => {
               dismissTimeoutId = null;
               dismiss();
            }, dismissMs);
         }
      }

      return {
         dismiss,
         show,
      };
   }
}
