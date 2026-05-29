import { parseClockTimeMinutes } from './dayPlannerSchedule.js';

export function buildItineraryTimeMarkers(itinerary = {}, strings = {}) {
   return [
      {
         startMinutes: parseClockTimeMinutes(itinerary.arrivalTime),
         label: strings.arrivalLabel,
      },
      {
         startMinutes: parseClockTimeMinutes(itinerary.departureTime),
         label: strings.departureLabel,
      },
   ].filter((marker) => (
      Number.isFinite(marker.startMinutes)
      && marker.label
   ));
}

export function buildMarkersByStart(itineraryTimeMarkers = []) {
   return itineraryTimeMarkers.reduce((markersMap, marker) => {
      const markers = markersMap.get(marker.startMinutes) ?? [];
      markers.push(marker);
      markersMap.set(marker.startMinutes, markers);
      return markersMap;
   }, new Map());
}

export function resolveTimelinePillLabel(
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
