import { Strings } from '../strings.js';

const HIDDEN_HOVER_TYPES = new Set([
   'transportationRouteMarker',
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
         ? Strings.map.hover.guardiansTalkWithName(name)
         : Strings.entityLabels.guardiansTalk;
   });
}

function formatWildEncounterHoverText(itemsAtPoint) {
   if (itemsAtPoint.length === 1) {
      const name = itemsAtPoint[0]?.name || '';
      return name
         ? Strings.map.hover.wildEncounterMeetingSpotWithName(name)
         : Strings.map.hover.wildEncounterMeetingSpot;
   }

   const first = itemsAtPoint[0]?.name || Strings.map.hover.wildEncounterMeetingSpot;
   return Strings.map.hover.wildEncounterMultiple(first, itemsAtPoint.length - 1);
}

const HOVER_FORMATTERS = Object.freeze({
   animal: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'species', Strings.entityLabels.animal)
   ),
   pavilion: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', Strings.entityLabels.pavilion)
   ),
   restaurant: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', Strings.entityLabels.restaurant)
   ),
   restroom: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'title', Strings.entityLabels.restroom)
   ),
   giftShop: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', Strings.entityLabels.giftShop)
   ),
   attraction: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', Strings.entityLabels.attraction)
   ),
   transportation: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', Strings.entityLabels.attraction)
   ),
   transportationStation: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', Strings.entityLabels.transportationStation)
   ),
   guardiansTalk: formatGuardiansTalkHoverText,
   wildEncounter: formatWildEncounterHoverText,
   drinkingFountain: (items) => formatCountedHoverText(
      items,
      () => Strings.map.hover.drinkingFountain
   ),
   defibrillator: (items) => formatCountedHoverText(
      items,
      () => Strings.map.hover.defibrillator
   ),
   emergencyIntercom: (items) => formatCountedHoverText(
      items,
      () => Strings.map.hover.emergencyIntercom
   ),
   guestService: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'service_type', Strings.map.hover.guestService)
   ),
   picnicSite: (items) => formatCountedHoverText(
      items,
      () => Strings.map.hover.picnicSite
   ),
   eventSite: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', Strings.map.hover.eventSite)
   ),
});

export class MarkerHoverText {
   static buildHoverText(itemsAtPoint) {
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
}
