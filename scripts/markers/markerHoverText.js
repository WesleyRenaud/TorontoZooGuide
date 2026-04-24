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
      return name ? `${name} Meet The Guardians Talk` : 'Meet The Guardians Talk';
   });
}

function formatWildEncounterHoverText(itemsAtPoint) {
   if (itemsAtPoint.length === 1) {
      const name = itemsAtPoint[0]?.name || '';
      return name
         ? `Wild Encounter • ${name} - Meeting Spot`
         : 'Wild Encounter Meeting Spot';
   }

   const first = itemsAtPoint[0]?.name || 'Wild Encounter Meeting Spot';
   return `Wild Encounter • ${first} + ${itemsAtPoint.length - 1} more - Meeting Spot`;
}

const HOVER_FORMATTERS = Object.freeze({
   animal: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'species', 'Animal')
   ),
   pavilion: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', 'Pavilion')
   ),
   restaurant: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', 'Restaurant')
   ),
   restroom: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'title', 'Restroom')
   ),
   giftShop: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', 'Gift Shop')
   ),
   attraction: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', 'Attraction')
   ),
   zoomobileStation: (items) => formatCountedHoverText(
      items,
      (item) => readItemText(item, 'name', 'Zoomobile Station')
   ),
   guardiansTalk: formatGuardiansTalkHoverText,
   wildEncounter: formatWildEncounterHoverText,
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
