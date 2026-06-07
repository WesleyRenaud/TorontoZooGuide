export function buildSpeciesExhibitKey(animal = {}, { requireExhibit = true } = {}) {
   const species = String(animal?.species ?? '').trim().toLowerCase();
   const exhibit = String(animal?.exhibit ?? '').trim().toLowerCase();

   if (!species || (requireExhibit && !exhibit)) {
      return '';
   }

   return `${species}|${exhibit}`;
}

export function buildUniqueSpeciesExhibitEntries(
   animals = [],
   {
      includeAnimal = () => true,
      mergeAnimals = null,
      requireExhibit = true,
   } = {}
) {
   const entries = [];
   const entriesBySpeciesExhibit = new Map();

   animals.forEach((animal, index) => {
      if (!includeAnimal(animal, index)) {
         return;
      }

      const key = buildSpeciesExhibitKey(animal, { requireExhibit });

      if (!key) {
         return;
      }

      const existing = entriesBySpeciesExhibit.get(key);

      if (!existing) {
         const entry = { item: animal, index };

         entries.push(entry);
         entriesBySpeciesExhibit.set(key, entry);
         return;
      }

      if (typeof mergeAnimals === 'function') {
         existing.item = mergeAnimals(existing.item, animal);
      }
   });

   return entries;
}
