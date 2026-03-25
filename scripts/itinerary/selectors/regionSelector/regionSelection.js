export function normalizeRegion(region) {
   const name = region?.name ?? region?.NAME ?? '';
   const exhibits = Array.isArray(region?.exhibits) ? region.exhibits : [];

   return {
      name,
      exhibits: exhibits.filter(Boolean),
   };
}

export function shouldHideDuplicateSingleExhibit(region) {
   const regionName = String(region?.name ?? '').trim().toLowerCase();
   const exhibits = Array.isArray(region?.exhibits) ? region.exhibits : [];

   if (exhibits.length !== 1) return false;

   const exhibitName = String(exhibits[0] ?? '').trim().toLowerCase();
   return Boolean(regionName) && regionName === exhibitName;
}

export function getSpecies(animal) {
   if (typeof animal === 'string') return animal;
   return animal?.species ?? animal?.SPECIES ?? animal?.name ?? animal?.species_name ?? '';
}

export function getExhibit(animal) {
   if (typeof animal === 'string') return '';
   return animal?.exhibit ?? animal?.EXHIBIT ?? animal?.exhibit_name ?? '';
}

export function makeSelectedAnimal(fullAnimal) {
   const species = getSpecies(fullAnimal);
   const exhibit = getExhibit(fullAnimal);

   return {
      id: `${species}||${exhibit}`,
      species,
      exhibit,
      imageSrc: fullAnimal?.imageSrc ?? fullAnimal?.image_src ?? null,
   };
}

export function buildSelectedAnimalKey(animal) {
   if (!animal || typeof animal !== 'object') return '';

   const id = String(animal.id ?? '').trim().toLowerCase();
   if (id) return id;

   const species = getSpecies(animal).trim().toLowerCase();
   const exhibit = getExhibit(animal).trim().toLowerCase();

   if (!species) return '';

   return `${species}||${exhibit}`;
}

export function mergeAnimals(existingAnimals = [], newAnimals = []) {
   const merged = [];
   const seen = new Set();

   [...existingAnimals, ...newAnimals].forEach((animal) => {
      const key = buildSelectedAnimalKey(animal);
      if (!key || seen.has(key)) return;

      seen.add(key);
      merged.push(animal);
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

export function syncSelectionsFromCurrentAnimals(
   regions,
   selectedRegionNames,
   selectedExhibitNames,
   currentAnimals
) {
   selectedRegionNames.clear();
   selectedExhibitNames.clear();

   if (!regions.length || !currentAnimals.length) {
      return;
   }

   const currentExhibits = new Set(
      currentAnimals
         .map((animal) => getExhibit(animal).trim())
         .filter(Boolean)
   );

   regions.forEach((region) => {
      const exhibits = Array.isArray(region?.exhibits) ? region.exhibits : [];
      if (!exhibits.length) return;

      let allExhibitsSelected = true;

      exhibits.forEach((exhibitName) => {
         if (currentExhibits.has(exhibitName)) {
            selectedExhibitNames.add(exhibitName);
         } else {
            allExhibitsSelected = false;
         }
      });

      if (allExhibitsSelected) {
         selectedRegionNames.add(region.name);
      }
   });
}