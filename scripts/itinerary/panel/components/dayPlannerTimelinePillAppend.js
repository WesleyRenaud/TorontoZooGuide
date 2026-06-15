import {
   createScheduledPillStrip,
   getOrCreatePointPillStrip,
} from './dayPlannerTimelinePillPlacement.js';
import { normalizeVisitBoundaryEventTypes } from '../../itineraryEventTypes.js';
import {
   makeBoundaryMarker,
   makeOpenPill,
} from './openTimelinePill.js';
import { makeScheduledPill } from './scheduledTimelinePill.js';
import { TIMELINE_SLOT_MINUTES } from '../../../shared/constants.js';

function applyPointPillStripPlacement(pillStrip, placement = '') {
   if (!pillStrip || !placement) {
      return;
   }

   pillStrip.setAttribute('data-visit-boundary-placement', placement);
}

function insertPointPillInStrip(strip, pill) {
   strip.appendChild(pill);
}

export function appendTimelinePill(
   gridLine,
   label,
   offsetFraction = 0,
   pillOptions = {}
) {
   if (!label) {
      return;
   }

   const pill = pillOptions.visitBoundaryPlacement
      ? makeBoundaryMarker(label, pillOptions)
      : makeOpenPill(label, pillOptions);

   if (!pill) {
      return;
   }

   const strip = getOrCreatePointPillStrip(gridLine, offsetFraction);

   applyPointPillStripPlacement(strip, pillOptions.visitBoundaryPlacement);
   insertPointPillInStrip(strip, pill);
}

export function appendScheduledDurationPill(
   gridLine,
   {
      label,
      offsetFraction = 0,
      durationMinutes,
      displayDurationMinutes = durationMinutes,
      slotSpanMinutes = TIMELINE_SLOT_MINUTES,
      startTime,
      endTime,
      groupItems = [],
      menuItems = [],
      menuAriaLabel = '',
      onLabelClick = null,
   }
) {
   const pill = makeScheduledPill(label, durationMinutes, {
      startTime,
      endTime,
      groupItems,
      menuItems,
      menuAriaLabel,
      onLabelClick,
      slotSpanMinutes,
      displayDurationMinutes,
   });

   if (!pill) {
      return;
   }

   const strip = createScheduledPillStrip(
      gridLine,
      offsetFraction,
      displayDurationMinutes,
      slotSpanMinutes
   );

   strip.appendChild(pill);
}

function resolveTimePillOptions(
   marker,
   timeHandlers = {},
   strings = {},
   visitBoundaryEventTypes = {}
) {
   const boundaries = normalizeVisitBoundaryEventTypes(visitBoundaryEventTypes);

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

export function appendItineraryTimeMarkers(
   gridLine,
   markersByAnchorSlot,
   slotStart,
   timeHandlers = {},
   strings = {},
   visitBoundaryEventTypes = {}
) {
   (markersByAnchorSlot.get(slotStart) ?? []).forEach((marker) => {
      appendTimelinePill(
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
