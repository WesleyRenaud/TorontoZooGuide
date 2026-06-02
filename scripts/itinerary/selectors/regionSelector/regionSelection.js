function normalizeRegionName(name = '') {
   return typeof name === 'string'
      ? name.trim()
      : '';
}

function normalizeRegionExhibits(exhibits = []) {
   return exhibits
      .map((exhibit) => normalizeRegionName(exhibit))
      .filter(Boolean);
}

export function createEmptyRegion() {
   return {
      name: '',
      exhibits: [],
   };
}

export function normalizeRegion(region = createEmptyRegion()) {
   const {
      name = '',
      exhibits = [],
   } = region;

   return {
      name: normalizeRegionName(name),
      exhibits: normalizeRegionExhibits(exhibits),
   };
}

export function normalizeRegions(regions = []) {
   return regions
      .map(normalizeRegion)
      .filter((region) => region.name);
}

export function getRegionName(region = createEmptyRegion()) {
   return region.name;
}

export function getRegionExhibits(region = createEmptyRegion()) {
   return region.exhibits;
}

export function shouldHideDuplicateSingleExhibit(region) {
   const regionName = getRegionName(region).toLowerCase();
   const exhibits = getRegionExhibits(region);

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

export function getExhibitNamesFromAnimals(animals = []) {
   return [...new Set(
      animals
         .map(normalizeSelectedAnimal)
         .filter((animal) => animal.exhibit)
         .map((animal) => animal.exhibit)
   )];
}

export function omitRemovedAnimals(animals = [], removedKeys = new Set()) {
   return animals.filter((animal) => {
      const key = buildSelectedAnimalKey(animal);

      return key && !removedKeys.has(key);
   });
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
   const exhibits = getRegionExhibits(region);
   if (!exhibits.length) return false;

   return exhibits.every((exhibit) => selectedExhibitNames.has(exhibit));
}

export function syncRegionSelection(region, selectedRegionNames, selectedExhibitNames) {
   const regionName = getRegionName(region);
   if (!regionName) return;

   if (isRegionFullySelected(region, selectedExhibitNames)) {
      selectedRegionNames.add(regionName);
   } else {
      selectedRegionNames.delete(regionName);
   }
}
