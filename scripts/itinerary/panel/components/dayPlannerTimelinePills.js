import { el } from '../dom.js';

function makeTimelinePill(label) {
   return el('span', 'itinerary-day-open-pill', label);
}

function getOrCreatePillStrip(gridLine) {
   const existingStrip = gridLine.querySelector('.itinerary-day-pill-strip');

   if (existingStrip) {
      return existingStrip;
   }

   const pillStrip = el('div', 'itinerary-day-pill-strip');

   gridLine.appendChild(pillStrip);

   return pillStrip;
}

export function appendTimelinePill(gridLine, label) {
   if (!label) {
      return;
   }

   getOrCreatePillStrip(gridLine).appendChild(makeTimelinePill(label));
}

export function appendItineraryTimeMarkers(gridLine, markersByStart, slotStart) {
   (markersByStart.get(slotStart) ?? []).forEach((marker) => {
      appendTimelinePill(gridLine, marker.label);
   });
}
