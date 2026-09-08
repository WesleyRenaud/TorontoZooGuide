import { AnimalsClient } from '../../../api/animalsClient.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { SpeciesSourceNormalizer } from './speciesSourceNormalizer.js';

export class SpeciesProvider {
   static createAnimalSpeciesSource() {
      let allSpecies = [];
      let allSpeciesLoaded = false;
      const speciesByExhibit = new Map();

      async function ensureAllSpeciesLoaded() {
         if (allSpeciesLoaded) {
            return allSpecies;
         }

         const rawSpecies = await ConsoleOptionsLoader.loadSpecies();
         allSpecies = SpeciesSourceNormalizer.normalizeSpeciesList(rawSpecies);
         allSpeciesLoaded = true;
         return allSpecies;
      }

      async function loadForExhibit(exhibit) {
         const exhibitKey = SpeciesSourceNormalizer.normalizeExhibitKey(exhibit);

         if (!exhibitKey) {
            return ensureAllSpeciesLoaded();
         }

         if (speciesByExhibit.has(exhibitKey)) {
            return speciesByExhibit.get(exhibitKey);
         }

         const animals = await AnimalsClient.getAnimalsInExhibit(exhibitKey);
         const species = SpeciesSourceNormalizer.normalizeSpeciesList(
            animals.map((animal) => String(animal || ''))
         );

         speciesByExhibit.set(exhibitKey, species);
         return species;
      }

      return {
         loadForExhibit,
      };
   }
}
