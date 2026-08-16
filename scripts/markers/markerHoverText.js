import { APP_STRINGS } from '../strings.js';

const HIDDEN_HOVER_TYPES = new Set([
   'zoomobileRouteMarker',
]);

function readItemText(item, field, fallback) {
   return item?.[field] || fallback;
}

function formatCountedHoverText(itemsAtPoint, getTitle) {
   const firstTitle = getTitle(itemsAtPoint[0]);

   if (itemsAtPoint.length === 1) {
      return firstTitle;
   }

   return `${firstTitle} + ${itemsAtPoint.length - 1}`;
}

function formatGuardiansTalkHoverText(itemsAtPoint) {
   return formatCountedHoverText(itemsAtPoint, (item) => {
      const name = item?.name || '';
      return name
         ? APP_STRINGS.map.hover.guardiansTalkWithName(name)
         : APP_STRINGS.entityLabels.guardiansTalk;
   });
}

function formatWildEncounterHoverText(itemsAtPoint) {
   if (itemsAtPoint.length === 1) {
      const name = itemsAtPoint[0]?.name || '';
      return name
         ? APP_STRINGS.map.hover.wildEncounterMeetingSpotWithName(name)
         : APP_STRINGS.map.hover.wildEncounterMeetingSpot;
   }

   const first = itemsAtPoint[0]?.name || APP_STRINGS.map.hover.wildEncounterMeetingSpot;
   return APP_STRINGS.map.hover.wildEncounterMultiple(first, itemsAtPoint.length - 1);
}

const HOVER_FORMATTERS = Object.freeze({
   animal: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'species', APP_STRINGS.entityLabels.animal)
   ),
   pavilion: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', APP_STRINGS.entityLabels.pavilion)
   ),
   restaurant: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', APP_STRINGS.entityLabels.restaurant)
   ),
   restroom: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'title', APP_STRINGS.entityLabels.restroom)
   ),
   giftShop: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', APP_STRINGS.entityLabels.giftShop)
   ),
   attraction: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', APP_STRINGS.entityLabels.attraction)
   ),
   transportation: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', APP_STRINGS.entityLabels.attraction)
   ),
   zoomobileStation: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', APP_STRINGS.entityLabels.zoomobileStation)
   ),
   guardiansTalk: formatGuardiansTalkHoverText,
   wildEncounter: formatWildEncounterHoverText,
   drinkingFountain: (items) => formatCountedHoverText(
      items,
      () => APP_STRINGS.map.hover.drinkingFountain
   ),
   defibrillator: (items) => formatCountedHoverText(
      items,
      () => APP_STRINGS.map.hover.defibrillator
   ),
   emergencyIntercom: (items) => formatCountedHoverText(
      items,
      () => APP_STRINGS.map.hover.emergencyIntercom
   ),
   guestService: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'service_type', APP_STRINGS.map.hover.guestService)
   ),
   picnicSite: (items) => formatCountedHoverText(
      items,
      () => APP_STRINGS.map.hover.picnicSite
   ),
   eventSite: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', APP_STRINGS.map.hover.eventSite)
   ),
});

export function buildHoverText(itemsAtPoint) {
   if (!itemsAtPoint || itemsAtPoint.length === 0) {
      return '';
   }

   const type = String(itemsAtPoint[0].type || '');
   const formatter = HOVER_FORMATTERS[type];

   if (HIDDEN_HOVER_TYPES.has(type) || !formatter) {
      return '';
   }

   return formatter(itemsAtPoint);
}
