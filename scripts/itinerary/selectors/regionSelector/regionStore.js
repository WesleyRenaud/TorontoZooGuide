import { AnimalIdentity } from '../../animalIdentity.js';
import { ValueNormalizer } from '../../../api/valueNormalizer.js';

export class RegionStore {
   static createEmptyRegion() {
      return {
         name: '',
         exhibits: [],
      };
   }

   static normalizeRegion(region = RegionStore.createEmptyRegion()) {
      const {
         name = '',
         exhibits = [],
      } = region;

      return {
         name: ValueNormalizer.asTrimmedString(name),
         exhibits: ValueNormalizer.asTrimmedStringList(exhibits),
      };
   }

   static normalizeRegions(regions = []) {
      return regions
         .map(RegionStore.normalizeRegion)
         .filter((region) => region.name);
   }

   static getRegionName(region = RegionStore.createEmptyRegion()) {
      return region.name;
   }

   static getRegionExhibits(region = RegionStore.createEmptyRegion()) {
      return region.exhibits;
   }

   static shouldHideDuplicateSingleExhibit(region) {
      const regionName = RegionStore.getRegionName(region).toLowerCase();
      const exhibits = RegionStore.getRegionExhibits(region);

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
      const imageSrc = ValueNormalizer.asTrimmedString(animal.imageSrc);

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
         id: ValueNormalizer.asTrimmedString(animal.id) || defaultId,
      };
   }

   static makeSelectedAnimal(fullAnimal) {
      return RegionStore.normalizeSelectedAnimal({
         species: fullAnimal?.species,
         exhibit: fullAnimal?.exhibit,
         enclosure_name: fullAnimal?.enclosure_name ?? null,
         imageSrc: fullAnimal?.imageSrc ?? null,
      });
   }

   static buildSelectedAnimalKey(animal) {
      const normalizedAnimal = RegionStore.normalizeSelectedAnimal(animal);

      if (!normalizedAnimal) {
         return '';
      }

      const id = ValueNormalizer.asTrimmedString(normalizedAnimal.id).toLowerCase();
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
      const animal = RegionStore.parseAnimalWireKey(key);

      return animal ? RegionStore.buildSelectedAnimalKey(animal) : '';
   }

   static getExhibitNamesFromAnimals(animals = []) {
      return [...new Set(
         animals
            .map(RegionStore.normalizeSelectedAnimal)
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
            .map((animal) => RegionStore.buildSelectedAnimalKey(
               RegionStore.normalizeSelectedAnimal(animal)
            ))
            .filter(Boolean)
      );

      return catalogAnimals.every((animal) => {
         const key = RegionStore.buildSelectedAnimalKey(
            RegionStore.normalizeSelectedAnimal(animal)
         );

         return Boolean(key) && draftKeys.has(key);
      });
   }

   static omitRemovedAnimals(animals = [], removedKeys = new Set()) {
      return animals.filter((animal) => {
         const key = RegionStore.buildSelectedAnimalKey(animal);

         return key && !removedKeys.has(key);
      });
   }

   static mergeAnimals(existingAnimals = [], newAnimals = []) {
      const merged = [];
      const seen = new Set();

      [...existingAnimals, ...newAnimals].forEach((animal) => {
         const normalizedAnimal = RegionStore.normalizeSelectedAnimal(animal);
         const key = RegionStore.buildSelectedAnimalKey(normalizedAnimal);

         if (!key || seen.has(key)) return;

         seen.add(key);
         merged.push(normalizedAnimal);
      });

      return merged;
   }

   static isRegionFullySelected(region, selectedExhibitNames) {
      const exhibits = RegionStore.getRegionExhibits(region);
      if (!exhibits.length) return false;

      return exhibits.every((exhibit) => selectedExhibitNames.has(exhibit));
   }

   static syncRegionSelection(region, selectedRegionNames, selectedExhibitNames) {
      const regionName = RegionStore.getRegionName(region);
      if (!regionName) return;

      if (RegionStore.isRegionFullySelected(region, selectedExhibitNames)) {
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
         .map(RegionStore.normalizeSelectedAnimal)
         .filter(Boolean);

      if (!animals.length) {
         return true;
      }

      const storedExhibits = new Set(RegionStore.getExhibitNamesFromAnimals(animals));

      for (const exhibitName of selectedExhibitNames) {
         if (!storedExhibits.has(exhibitName)) {
            return true;
         }
      }

      return false;
   }
}
