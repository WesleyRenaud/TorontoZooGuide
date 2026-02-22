export function buildHoverText(itemsAtPoint) {
   if (!itemsAtPoint || itemsAtPoint.length === 0) return '';

   const type = String(itemsAtPoint[0].type || '').toLowerCase();

   // Animals
   if (type === 'animal') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].species ?? itemsAtPoint[0].SPECIES ?? 'Animal';
      }
      const first = itemsAtPoint[0].species ?? itemsAtPoint[0].SPECIES ?? 'Animal';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   // Pavilions
   if (type === 'pavilion') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].name || 'Pavilion';
      }
      const first = itemsAtPoint[0].name || 'Pavilion';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   // Restaurants ✅
   if (type === 'restaurant') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].name || 'Restaurant';
      }
      const first = itemsAtPoint[0].name || 'Restaurant';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   // Restrooms ✅
   if (type === 'restroom') {
      if (itemsAtPoint.length === 1) {
         return itemsAtPoint[0].title || 'Restroom';
      }
      const first = itemsAtPoint[0].title || 'Restroom';
      return `${first} + ${itemsAtPoint.length - 1}`;
   }

   // Fallback
   return type ? `${type} (${itemsAtPoint.length})` : String(itemsAtPoint.length);
}