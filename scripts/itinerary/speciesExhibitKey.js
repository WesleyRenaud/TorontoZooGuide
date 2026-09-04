import { AnimalIdentity } from './animalIdentity.js';
import { EnclosureType } from '../shared/enums/enclosureType.js';

function buildViewingSpotSuffix(animal = {}) {
   const { enclosure_name: enclosureName } = AnimalIdentity.normalizeAnimalIdentitySearchFields(animal);

   if (enclosureName) {
      return enclosureName;
   }

   const enclosureType = EnclosureType.normalizeEnclosureType(animal?.enclosure_type);

   return enclosureType ? enclosureType.toLowerCase() : '';
}

export class SpeciesExhibitKey {
   static buildSpeciesExhibitKey(animal = {}, { requireExhibit = true } = {}) {
      const { species, exhibit } = AnimalIdentity.normalizeAnimalIdentitySearchFields(animal);

      if (!species || (requireExhibit && !exhibit)) {
         return '';
      }

      return `${species}|${exhibit}`;
   }

   static buildAnimalViewingSpotKey(animal = {}, { requireExhibit = true } = {}) {
      const baseKey = SpeciesExhibitKey.buildSpeciesExhibitKey(animal, { requireExhibit });

      if (!baseKey) {
         return '';
      }

      const viewingSpotSuffix = buildViewingSpotSuffix(animal);

      return viewingSpotSuffix ? `${baseKey}|${viewingSpotSuffix}` : baseKey;
   }

   static buildUniqueSpeciesExhibitEntries(
      animals = [],
      {
         includeAnimal = () => true,
         mergeAnimals = null,
         requireExhibit = true,
         buildKey = SpeciesExhibitKey.buildSpeciesExhibitKey,
      } = {}
   ) {
      const entries = [];
      const entriesByKey = new Map();

      animals.forEach((animal, index) => {
         if (!includeAnimal(animal, index)) {
            return;
         }

         const key = buildKey(animal, { requireExhibit });

         if (!key) {
            return;
         }

         const existing = entriesByKey.get(key);

         if (!existing) {
            const entry = { item: animal, index };

            entries.push(entry);
            entriesByKey.set(key, entry);
            return;
         }

         if (typeof mergeAnimals === 'function') {
            existing.item = mergeAnimals(existing.item, animal);
         }
      });

      return entries;
   }
}
