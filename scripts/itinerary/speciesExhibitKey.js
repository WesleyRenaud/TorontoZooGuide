export function buildSpeciesExhibitKey(animal = {}) {
   const species = String(animal?.species ?? '').trim().toLowerCase();
   const exhibit = String(animal?.exhibit ?? '').trim().toLowerCase();

   if (!species || !exhibit) {
      return '';
   }

   return `${species}|${exhibit}`;
}
