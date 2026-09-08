import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';
import { TimelineLayoutConstants } from '../../../shared/timelineLayoutConstants.js';

export class DayPlannerActionFeedbackFragment {
   static appendDayPlannerActionFeedbackSlot(container) {
      if (!container) {
         return null;
      }

      const slot = ItineraryPanelHelper.el('div', 'itinerary-day-action-feedback-slot');
      slot.setAttribute('aria-live', 'polite');
      container.appendChild(slot);

      return slot;
   }

   static appendDayPlannerActionFeedbackBanner(
      slot,
      {
         variant = 'success',
         message = '',
      } = {},
      {
         dismissMs = TimelineLayoutConstants.DAY_PLANNER_ACTION_FEEDBACK_DISMISS_MS,
         fadeMs = TimelineLayoutConstants.DAY_PLANNER_ACTION_FEEDBACK_FADE_MS,
      } = {}
   ) {
      if (!slot || !message) {
         return null;
      }

      const banner = ItineraryPanelHelper.el(
         'div',
         `itinerary-day-action-feedback itinerary-day-action-feedback--${variant}`,
         message
      );

      banner.setAttribute('role', 'status');
      slot.appendChild(banner);

      requestAnimationFrame(() => {
         banner.classList.add('is-visible');
      });

      let dismissTimeoutId = null;
      let fadeTimeoutId = null;

      const cleanup = () => {
         if (dismissTimeoutId !== null) {
            clearTimeout(dismissTimeoutId);
            dismissTimeoutId = null;
         }

         if (fadeTimeoutId !== null) {
            clearTimeout(fadeTimeoutId);
            fadeTimeoutId = null;
         }

         banner.remove();
      };

      banner.__tzgCleanup = cleanup;

      dismissTimeoutId = setTimeout(() => {
         dismissTimeoutId = null;
         banner.classList.add('is-dismissing');

         fadeTimeoutId = setTimeout(() => {
            fadeTimeoutId = null;
            cleanup();
         }, fadeMs);
      }, dismissMs);

      return banner;
   }
}
