import { DayPlannerTimelinePillPlacement } from './dayPlannerTimelinePillPlacement.js';
import { ItineraryEventTypes } from '../../itineraryEventTypes.js';
import { OpenTimelinePill } from './openTimelinePill.js';
import { makeScheduledPill } from './scheduledTimelinePill.js';
import { Constants } from '../../../shared/constants.js';

function applyPointPillStripPlacement(pillStrip, placement = '') {
   if (!pillStrip || !placement) {
      return;
   }

   pillStrip.setAttribute('data-visit-boundary-placement', placement);
}

function insertPointPillInStrip(strip, pill) {
   strip.appendChild(pill);
}

function resolveTimePillOptions(
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

export class DayPlannerTimelinePillAppend {
   static appendTimelinePill(
      gridLine,
      label,
      offsetFraction = 0,
      pillOptions = {}
   ) {
      if (!label) {
         return;
      }

      const pill = pillOptions.visitBoundaryPlacement
         ? OpenTimelinePill.makeBoundaryMarker(label, pillOptions)
         : OpenTimelinePill.makeOpenPill(label, pillOptions);

      if (!pill) {
         return;
      }

      const strip = DayPlannerTimelinePillPlacement.getOrCreatePointPillStrip(
         gridLine,
         offsetFraction
      );

      applyPointPillStripPlacement(strip, pillOptions.visitBoundaryPlacement);
      insertPointPillInStrip(strip, pill);
   }

   static appendScheduledDurationPill(
      gridLine,
      {
         label,
         offsetFraction = 0,
         durationMinutes,
         displayDurationMinutes = durationMinutes,
         slotSpanMinutes = Constants.TIMELINE_SLOT_MINUTES,
         startTime,
         endTime,
         groupItems = [],
         menuItems = [],
         menuAriaLabel = '',
         onLabelClick = null,
         item = null,
      }
   ) {
      const pill = makeScheduledPill(label, durationMinutes, {
         startTime,
         endTime,
         groupItems,
         menuItems,
         menuAriaLabel,
         onLabelClick,
         item,
         slotSpanMinutes,
         displayDurationMinutes,
      });

      if (!pill) {
         return;
      }

      const strip = DayPlannerTimelinePillPlacement.createScheduledPillStrip(
         gridLine,
         offsetFraction,
         displayDurationMinutes,
         slotSpanMinutes
      );

      strip.appendChild(pill);
   }

   static appendItineraryTimeMarkers(
      gridLine,
      markersByAnchorSlot,
      slotStart,
      timeHandlers = {},
      strings = {},
      visitBoundaryEventTypes = {}
   ) {
      (markersByAnchorSlot.get(slotStart) ?? []).forEach((marker) => {
         DayPlannerTimelinePillAppend.appendTimelinePill(
            gridLine,
            marker.label,
            marker.offsetFraction,
            resolveTimePillOptions(
               marker,
               timeHandlers,
               strings,
               visitBoundaryEventTypes
            )
         );
      });
   }
}
