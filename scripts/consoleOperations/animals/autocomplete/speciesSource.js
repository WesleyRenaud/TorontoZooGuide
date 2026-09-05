import { AnimalsApi } from '../../../api/animalsApi.js';
import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { Loaders } from '../../options/loaders.js';

function normalizeSpeciesList(species) {
   return [...new Set(
      (species || [])
         .map((value) => ValueNormalizer.asTrimmedString(value))
         .filter(Boolean)
   )].sort((a, b) => a.localeCompare(b));
}

function normalizeExhibitKey(exhibit) {
   return ValueNormalizer.asTrimmedString(exhibit);
}

export class SpeciesSource {
   static createAnimalSpeciesSource() {
      let allSpecies = [];
      let allSpeciesLoaded = false;
      const speciesByExhibit = new Map();

      async function ensureAllSpeciesLoaded() {
         if (allSpeciesLoaded) {
            return allSpecies;
         }

         const rawSpecies = await Loaders.loadSpecies();
         allSpecies = normalizeSpeciesList(rawSpecies);
         allSpeciesLoaded = true;
         return allSpecies;
      }

      async function loadForExhibit(exhibit) {
         const exhibitKey = normalizeExhibitKey(exhibit);

         if (!exhibitKey) {
            return ensureAllSpeciesLoaded();
         }

         if (speciesByExhibit.has(exhibitKey)) {
            return speciesByExhibit.get(exhibitKey);
         }

         const animals = await AnimalsApi.getAnimalsInExhibit(exhibitKey);
         const species = normalizeSpeciesList(
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
