import { getPavilionName } from '../utils/dom.js';

export function buildHoverText(itemsAtPoint) {
   if (!itemsAtPoint || itemsAtPoint.length === 0) return '';

   const animals = itemsAtPoint.filter(i => String(i.type || '').toLowerCase() === 'animal');
   const pavilions = itemsAtPoint.filter(i => String(i.type || '').toLowerCase() === 'pavilion');

   if (animals.length > 0 && pavilions.length === 0) {
      if (animals.length === 1) return animals[0].species ?? animals[0].SPECIES ?? 'Animal';
      const first = animals[0].species ?? animals[0].SPECIES ?? 'Animal';
      return `${first} + ${animals.length - 1}`;
   }

   if (pavilions.length > 0 && animals.length === 0) {
      if (pavilions.length === 1) return getPavilionName(pavilions[0]) || 'Pavilion';
      const first = getPavilionName(pavilions[0]) || 'Pavilion';
      return `${first} + ${pavilions.length - 1}`;
   }

   return `${animals.length} Animals + ${pavilions.length} Pavilions`;
}