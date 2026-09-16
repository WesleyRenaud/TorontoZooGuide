import { AnimalsClient } from '../../../api/animalsClient.js';
import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { SpeciesSourceNormalizer } from './speciesSourceNormalizer.js';

export class SpeciesProvider {
   static async fetchOffDisplaySpecies() {
      const result = await ConsoleOperationsClient.getOffDisplayAnimalOptions();
      return result.species;
   }

   static async fetchOffDisplaySpeciesInExhibit(exhibit) {
      const result = await ConsoleOperationsClient.getOffDisplayAnimalOptions({ exhibit });
      return result.species;
   }

   static createOffDisplayAnimalSpeciesSource() {
      return SpeciesProvider.createAnimalSpeciesSource({
         fetchAllSpecies: SpeciesProvider.fetchOffDisplaySpecies,
         fetchSpeciesForExhibit: SpeciesProvider.fetchOffDisplaySpeciesInExhibit,
         cacheLists: false,
      });
   }

   static async fetchVisibilityScheduleSpecies() {
      const result = await ConsoleOperationsClient.getAnimalVisibilityScheduleOptions();
      return result.species;
   }

   static async fetchVisibilityScheduleSpeciesInExhibit(exhibit) {
      const result = await ConsoleOperationsClient.getAnimalVisibilityScheduleOptions({ exhibit });
      return result.species;
   }

   static createVisibilityScheduleAnimalSpeciesSource() {
      return SpeciesProvider.createAnimalSpeciesSource({
         fetchAllSpecies: SpeciesProvider.fetchVisibilityScheduleSpecies,
         fetchSpeciesForExhibit: SpeciesProvider.fetchVisibilityScheduleSpeciesInExhibit,
         cacheLists: false,
      });
   }

   static createAnimalSpeciesSource({
      fetchAllSpecies = ConsoleOptionsLoader.loadSpecies,
      fetchSpeciesForExhibit = AnimalsClient.getAnimalsInExhibit,
      cacheLists = true,
   } = {}) {
      let allSpecies = [];
      let allSpeciesLoaded = false;
      const speciesByExhibit = new Map();

      async function ensureAllSpeciesLoaded() {
         if (cacheLists && allSpeciesLoaded) {
            return allSpecies;
         }

         const rawSpecies = await fetchAllSpecies();
         allSpecies = SpeciesSourceNormalizer.normalizeSpeciesList(rawSpecies);

         if (cacheLists) {
            allSpeciesLoaded = true;
         }

         return allSpecies;
      }

      async function loadForExhibit(exhibit) {
         const exhibitKey = SpeciesSourceNormalizer.normalizeExhibitKey(exhibit);

         if (!exhibitKey) {
            return ensureAllSpeciesLoaded();
         }

         if (cacheLists && speciesByExhibit.has(exhibitKey)) {
            return speciesByExhibit.get(exhibitKey);
         }

         const animals = await fetchSpeciesForExhibit(exhibitKey);
         const species = SpeciesSourceNormalizer.normalizeSpeciesList(animals);

         if (cacheLists) {
            speciesByExhibit.set(exhibitKey, species);
         }

         return species;
      }

      return {
         loadForExhibit,
      };
   }
}
