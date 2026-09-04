import { AnimalIdentity } from '../../animalIdentity.js';

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

export class RegionSelection {
   static createEmptyRegion() {
      return {
         name: '',
         exhibits: [],
      };
   }

   static normalizeRegion(region = RegionSelection.createEmptyRegion()) {
      const {
         name = '',
         exhibits = [],
      } = region;

      return {
         name: normalizeRegionName(name),
         exhibits: normalizeRegionExhibits(exhibits),
      };
   }

   static normalizeRegions(regions = []) {
      return regions
         .map(RegionSelection.normalizeRegion)
         .filter((region) => region.name);
   }

   static getRegionName(region = RegionSelection.createEmptyRegion()) {
      return region.name;
   }

   static getRegionExhibits(region = RegionSelection.createEmptyRegion()) {
      return region.exhibits;
   }

   static shouldHideDuplicateSingleExhibit(region) {
      const regionName = RegionSelection.getRegionName(region).toLowerCase();
      const exhibits = RegionSelection.getRegionExhibits(region);

      if (exhibits.length !== 1) return false;

      const exhibitName = AnimalIdentity.normalizeAnimalIdentitySearchFields({
         exhibit: exhibits[0] ?? '',
      }).exhibit;
      return Boolean(regionName) && regionName === exhibitName;
   }

   static normalizeSelectedAnimal(animal) {
      if (!animal || typeof animal !== 'object') {
         return null;
      }

      const {
         species,
         exhibit,
         enclosure_name: enclosureName,
      } = AnimalIdentity.normalizeAnimalIdentityFields(animal);
      const imageSrc = typeof animal.imageSrc === 'string'
         ? animal.imageSrc.trim()
         : '';

      if (!species) {
         return null;
      }

      const defaultId = enclosureName
         ? `${species}||${exhibit}||${enclosureName}`
         : `${species}||${exhibit}`;

      return {
         ...animal,
         species,
         exhibit,
         ...(enclosureName ? { enclosure_name: enclosureName } : {}),
         imageSrc: imageSrc || null,
         id: typeof animal.id === 'string' && animal.id.trim()
            ? animal.id.trim()
            : defaultId,
      };
   }

   static makeSelectedAnimal(fullAnimal) {
      return RegionSelection.normalizeSelectedAnimal({
         species: fullAnimal?.species,
         exhibit: fullAnimal?.exhibit,
         enclosure_name: fullAnimal?.enclosure_name ?? null,
         imageSrc: fullAnimal?.imageSrc ?? null,
      });
   }

   static buildSelectedAnimalKey(animal) {
      const normalizedAnimal = RegionSelection.normalizeSelectedAnimal(animal);

      if (!normalizedAnimal) {
         return '';
      }

      const id = normalizedAnimal.id.trim().toLowerCase();
      if (id) return id;

      return AnimalIdentity.buildAnimalIdentityStorageKey(normalizedAnimal);
   }

   static parseAnimalWireKey(key) {
      const parts = String(key ?? '').split('||');
      const {
         species,
         exhibit,
         enclosure_name: enclosureName,
      } = AnimalIdentity.normalizeAnimalIdentityFields({
         species: parts[0],
         exhibit: parts[1],
         enclosure_name: parts[2],
      });

      if (!species) {
         return null;
      }

      return {
         species,
         exhibit,
         ...(enclosureName ? { enclosure_name: enclosureName } : {}),
      };
   }

   static buildSelectedAnimalKeyFromWire(key) {
      const animal = RegionSelection.parseAnimalWireKey(key);

      return animal ? RegionSelection.buildSelectedAnimalKey(animal) : '';
   }

   static getExhibitNamesFromAnimals(animals = []) {
      return [...new Set(
         animals
            .map(RegionSelection.normalizeSelectedAnimal)
            .filter((animal) => animal.exhibit)
            .map((animal) => animal.exhibit)
      )];
   }

   static draftAnimalsCoverCatalogAnimals(
      draftAnimals = [],
      catalogAnimals = []
   ) {
      if (!catalogAnimals.length) {
         return true;
      }

      const draftKeys = new Set(
         draftAnimals
            .map((animal) => RegionSelection.buildSelectedAnimalKey(
               RegionSelection.normalizeSelectedAnimal(animal)
            ))
            .filter(Boolean)
      );

      return catalogAnimals.every((animal) => {
         const key = RegionSelection.buildSelectedAnimalKey(
            RegionSelection.normalizeSelectedAnimal(animal)
         );

         return Boolean(key) && draftKeys.has(key);
      });
   }

   static omitRemovedAnimals(animals = [], removedKeys = new Set()) {
      return animals.filter((animal) => {
         const key = RegionSelection.buildSelectedAnimalKey(animal);

         return key && !removedKeys.has(key);
      });
   }

   static mergeAnimals(existingAnimals = [], newAnimals = []) {
      const merged = [];
      const seen = new Set();

      [...existingAnimals, ...newAnimals].forEach((animal) => {
         const normalizedAnimal = RegionSelection.normalizeSelectedAnimal(animal);
         const key = RegionSelection.buildSelectedAnimalKey(normalizedAnimal);

         if (!key || seen.has(key)) return;

         seen.add(key);
         merged.push(normalizedAnimal);
      });

      return merged;
   }

   static isRegionFullySelected(region, selectedExhibitNames) {
      const exhibits = RegionSelection.getRegionExhibits(region);
      if (!exhibits.length) return false;

      return exhibits.every((exhibit) => selectedExhibitNames.has(exhibit));
   }

   static syncRegionSelection(region, selectedRegionNames, selectedExhibitNames) {
      const regionName = RegionSelection.getRegionName(region);
      if (!regionName) return;

      if (RegionSelection.isRegionFullySelected(region, selectedExhibitNames)) {
         selectedRegionNames.add(regionName);
      } else {
         selectedRegionNames.delete(regionName);
      }
   }

   static selectedExhibitsNeedAnimalRebuild(
      selectedExhibitNames,
      storedAnimals = []
   ) {
      if (!selectedExhibitNames?.size) {
         return false;
      }

      const animals = storedAnimals
         .map(RegionSelection.normalizeSelectedAnimal)
         .filter(Boolean);

      if (!animals.length) {
         return true;
      }

      const storedExhibits = new Set(RegionSelection.getExhibitNamesFromAnimals(animals));

      for (const exhibitName of selectedExhibitNames) {
         if (!storedExhibits.has(exhibitName)) {
            return true;
         }
      }

      return false;
   }
}
