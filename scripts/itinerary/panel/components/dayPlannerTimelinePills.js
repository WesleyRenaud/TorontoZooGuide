import { el } from '../dom.js';

function makeTimelinePill(label) {
   return el('span', 'itinerary-day-open-pill', label);
}

function findPillStrip(gridLine, offsetFraction = 0) {
   const offsetKey = String(offsetFraction);

   for (const child of gridLine.children) {
      if (child.className !== 'itinerary-day-pill-strip') {
         continue;
      }

      const childOffset = child.getAttribute?.('data-offset-fraction')
         ?? child.attributes?.['data-offset-fraction']
         ?? '0';

      if (childOffset === offsetKey) {
         return child;
      }
   }

   return null;
}

function getOrCreatePillStrip(gridLine, offsetFraction = 0) {
   const existingStrip = findPillStrip(gridLine, offsetFraction);

   if (existingStrip) {
      return existingStrip;
   }

   const pillStrip = el('div', 'itinerary-day-pill-strip');

   if (offsetFraction > 0) {
      pillStrip.setAttribute('data-offset-fraction', String(offsetFraction));
      pillStrip.style.setProperty(
         '--itinerary-pill-offset-fraction',
         String(offsetFraction)
      );
   }

   gridLine.appendChild(pillStrip);

   return pillStrip;
}

export function appendTimelinePill(gridLine, label, offsetFraction = 0) {
   if (!label) {
      return;
   }

   getOrCreatePillStrip(gridLine, offsetFraction).appendChild(makeTimelinePill(label));
}

export function appendItineraryTimeMarkers(gridLine, markersByAnchorSlot, slotStart) {
   (markersByAnchorSlot.get(slotStart) ?? []).forEach((marker) => {
      appendTimelinePill(gridLine, marker.label, marker.offsetFraction);
   });
}
