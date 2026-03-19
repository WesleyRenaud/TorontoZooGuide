export function buildHoverText(itemsAtPoint) {
   if (!itemsAtPoint || itemsAtPoint.length === 0 || itemsAtPoint[0].type === 'zoomobileRouteMarker') return '';

   const type = String(itemsAtPoint[0].type || '');

   if (type === 'animal') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].species ?? itemsAtPoint[0].SPECIES ?? 'Animal';
      }
      const first = itemsAtPoint[0].species ?? itemsAtPoint[0].SPECIES ?? 'Animal';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   if (type === 'pavilion') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].name || 'Pavilion';
      }
      const first = itemsAtPoint[0].name || 'Pavilion';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   if (type === 'restaurant') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].name || 'Restaurant';
      }
      const first = itemsAtPoint[0].name || 'Restaurant';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   if (type === 'restroom') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].title || 'Restroom';
      }
      const first = itemsAtPoint[0].title || 'Restroom';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   if (type === 'giftShop') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].name || 'Gift Shop';
      }
      const first = itemsAtPoint[0].name || 'Gift Shop';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   if (type === 'attraction') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].name || 'Attraction';
      }
      const first = itemsAtPoint[0].name || 'Attraction';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   if (type === 'zoomobileStation') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].name || 'Zoomobile Station';
      }
      const first = itemsAtPoint[0].name || 'Zoomobile Station';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   if (type === 'guardiansTalk') {
      if (itemsAtPoint.length === 1) {
         return `${itemsAtPoint[0].name} Meet The Guardians Talk` || 'Meet The Guardians Talk';
      }
      const first = itemsAtPoint[0].name || 'Meet The Guardians Talk';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   if (type === 'wildEncounter') {
      if (itemsAtPoint.length === 1) {
         return `Wild Encounter • ${itemsAtPoint[0].name} - Meeting Spot` || 'Wild Encounter Meeting Spot';
      }
      const first = itemsAtPoint[0].name || 'Wild Encounter Meeting Spot';
      return `Wild Encounter • ${first} + ${itemsAtPoint.length - 1} more - Meeting Spot`;
   }
}