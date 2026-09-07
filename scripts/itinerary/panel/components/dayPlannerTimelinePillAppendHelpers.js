import { ItineraryEventTypes } from '../../itineraryEventTypes.js';

export class DayPlannerTimelinePillAppendHelpers {
   static applyPointPillStripPlacement(pillStrip, placement = '') {
      if (!pillStrip || !placement) {
         return;
      }

      pillStrip.setAttribute('data-visit-boundary-placement', placement);
   }

   static insertPointPillInStrip(strip, pill) {
      strip.appendChild(pill);
   }

   static resolveTimePillOptions(
      marker,
      timeHandlers = {},
      strings = {},
      visitBoundaryEventTypes = {}
   ) {
      const boundaries = ItineraryEventTypes.normalizeVisitBoundaryEventTypes(visitBoundaryEventTypes);

      if (marker.kind === boundaries.arrival) {
         const options = {
            menuAriaLabel: strings.arrivalTimeMenuAria,
            removeLabel: strings.remove,
            visitBoundaryPlacement: 'ends-at-anchor',
         };

         if (typeof timeHandlers.onArrivalTimeChange === 'function') {
            options.onRemove = () => timeHandlers.onArrivalTimeChange('');
         }

         return options;
      }

      if (marker.kind === boundaries.departure) {
         const options = {
            menuAriaLabel: strings.departureTimeMenuAria,
            removeLabel: strings.remove,
            visitBoundaryPlacement: 'starts-at-anchor',
         };

         if (typeof timeHandlers.onDepartureTimeChange === 'function') {
            options.onRemove = () => timeHandlers.onDepartureTimeChange('');
         }

         return options;
      }

      return {};
   }
}
