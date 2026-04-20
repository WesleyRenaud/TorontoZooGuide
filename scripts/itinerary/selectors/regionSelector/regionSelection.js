export function normalizeRegion(region) {
   const name = typeof region?.name === 'string'
      ? region.name.trim()
      : '';
   const exhibits = Array.isArray(region?.exhibits) ? region.exhibits : [];

   return {
      name,
      exhibits: exhibits
         .map((exhibit) => typeof exhibit === 'string' ? exhibit.trim() : '')
         .filter(Boolean),
   };
}

export function shouldHideDuplicateSingleExhibit(region) {
   const regionName = String(region?.name ?? '').trim().toLowerCase();
   const exhibits = Array.isArray(region?.exhibits) ? region.exhibits : [];

   if (exhibits.length !== 1) return false;

   const exhibitName = String(exhibits[0] ?? '').trim().toLowerCase();
   return Boolean(regionName) && regionName === exhibitName;
}

export function normalizeSelectedAnimal(animal) {
   if (!animal || typeof animal !== 'object') {
      return null;
   }

   const species = typeof animal.species === 'string'
      ? animal.species.trim()
      : '';
   const exhibit = typeof animal.exhibit === 'string'
      ? animal.exhibit.trim()
      : '';
   const imageSrc = typeof animal.imageSrc === 'string'
      ? animal.imageSrc.trim()
      : '';

   if (!species) {
      return null;
   }

   return {
      ...animal,
      species,
      exhibit,
      imageSrc: imageSrc || null,
      id: typeof animal.id === 'string' && animal.id.trim()
         ? animal.id.trim()
         : `${species}||${exhibit}`,
   };
}

export function makeSelectedAnimal(fullAnimal) {
   return normalizeSelectedAnimal({
      species: fullAnimal?.species,
      exhibit: fullAnimal?.exhibit,
      imageSrc: fullAnimal?.imageSrc ?? null,
   });
}

export function buildSelectedAnimalKey(animal) {
   const normalizedAnimal = normalizeSelectedAnimal(animal);

   if (!normalizedAnimal) {
      return '';
   }

   const id = normalizedAnimal.id.trim().toLowerCase();
   if (id) return id;

   const species = normalizedAnimal.species.trim().toLowerCase();
   const exhibit = normalizedAnimal.exhibit.trim().toLowerCase();

   if (!species) return '';

   return `${species}||${exhibit}`;
}

export function mergeAnimals(existingAnimals = [], newAnimals = []) {
   const merged = [];
   const seen = new Set();

   [...existingAnimals, ...newAnimals].forEach((animal) => {
      const normalizedAnimal = normalizeSelectedAnimal(animal);
      const key = buildSelectedAnimalKey(normalizedAnimal);

      if (!key || seen.has(key)) return;

      seen.add(key);
      merged.push(normalizedAnimal);
   });

   return merged;
}

export function isRegionFullySelected(region, selectedExhibitNames) {
   const exhibits = Array.isArray(region?.exhibits) ? region.exhibits : [];
   if (!exhibits.length) return false;

   return exhibits.every((exhibit) => selectedExhibitNames.has(exhibit));
}

export function syncRegionSelection(region, selectedRegionNames, selectedExhibitNames) {
   const regionName = region?.name;
   if (!regionName) return;

   if (isRegionFullySelected(region, selectedExhibitNames)) {
      selectedRegionNames.add(regionName);
   } else {
      selectedRegionNames.delete(regionName);
   }
}
