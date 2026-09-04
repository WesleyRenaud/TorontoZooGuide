import { DayPlannerSchedule } from './dayPlannerSchedule.js';
import { ItineraryEventTypes } from '../itineraryEventTypes.js';

export class DayPlannerTimelineMarkers {
   static buildItineraryTimeMarkers(itinerary = {}, strings = {}) {
      const visitBoundaryEventTypes = ItineraryEventTypes.normalizeVisitBoundaryEventTypes(
         itinerary.itineraryConfig?.visitBoundaryEventTypes
      );

      return [
         {
            startMinutes: DayPlannerSchedule.parseClockTimeMinutes(itinerary.arrivalTime),
            label: strings.arrivalLabel,
            kind: visitBoundaryEventTypes.arrival,
         },
         {
            startMinutes: DayPlannerSchedule.parseClockTimeMinutes(itinerary.departureTime),
            label: strings.departureLabel,
            kind: visitBoundaryEventTypes.departure,
         },
      ].filter((marker) => (
         Number.isFinite(marker.startMinutes)
         && marker.label
         && marker.kind
      ));
   }

   static findTimelineAnchorSlot(startMinutes, slotStarts = []) {
      if (!Number.isFinite(startMinutes) || slotStarts.length === 0) {
         return null;
      }

      let anchorSlot = slotStarts[0];

      for (const slotStart of slotStarts) {
         if (slotStart > startMinutes) {
            break;
         }

         anchorSlot = slotStart;
      }

      return anchorSlot;
   }

   static findTimelineSlotEndMinutes(anchorSlot, slotStarts = [], fallbackEndMinutes = null) {
      const anchorIndex = slotStarts.indexOf(anchorSlot);

      if (anchorIndex >= 0 && anchorIndex < slotStarts.length - 1) {
         return slotStarts[anchorIndex + 1];
      }

      return fallbackEndMinutes;
   }

   static computeMarkerOffsetFraction(startMinutes, anchorSlot, slotEndMinutes) {
      if (startMinutes === anchorSlot) {
         return 0;
      }

      const slotSpanMinutes = slotEndMinutes - anchorSlot;

      if (!Number.isFinite(slotSpanMinutes) || slotSpanMinutes <= 0) {
         return 0;
      }

      return (startMinutes - anchorSlot) / slotSpanMinutes;
   }

   static buildMarkersByAnchorSlot(
      itineraryTimeMarkers = [],
      slotStarts = [],
      closeMinutes = null
   ) {
      const sortedSlotStarts = [...slotStarts].sort((left, right) => left - right);

      return itineraryTimeMarkers.reduce((markersMap, marker) => {
         const anchorSlot = DayPlannerTimelineMarkers.findTimelineAnchorSlot(marker.startMinutes, sortedSlotStarts);

         if (!Number.isFinite(anchorSlot)) {
            return markersMap;
         }

         const slotEndMinutes = DayPlannerTimelineMarkers.findTimelineSlotEndMinutes(
            anchorSlot,
            sortedSlotStarts,
            closeMinutes
         );
         const offsetFraction = DayPlannerTimelineMarkers.computeMarkerOffsetFraction(
            marker.startMinutes,
            anchorSlot,
            slotEndMinutes
         );
         const markers = markersMap.get(anchorSlot) ?? [];

         markers.push({
            label: marker.label,
            offsetFraction,
            kind: marker.kind,
         });
         markersMap.set(anchorSlot, markers);

         return markersMap;
      }, new Map());
   }

   static resolveTimelinePillLabel(
      slotStart,
      {
         earlyAdmissionMinutes,
         openMinutes,
         lastAdmissionMinutes,
         closeMinutes,
      },
      strings = {}
   ) {
      if (slotStart === earlyAdmissionMinutes) {
         return strings.earlyAdmissionLabel;
      }

      if (slotStart === openMinutes) {
         return strings.openLabel;
      }

      if (slotStart === lastAdmissionMinutes) {
         return strings.lastAdmissionLabel;
      }

      if (slotStart === closeMinutes) {
         return strings.closeLabel;
      }

      return null;
   }

}
