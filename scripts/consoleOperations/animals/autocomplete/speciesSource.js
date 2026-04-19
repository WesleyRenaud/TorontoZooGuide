import { loadSpecies } from '../../options/loaders.js';
import { getAnimalsInExhibit } from '../../../api/animalsApi.js';

function normalizeSpeciesList(species) {
   return [...new Set(
      (species || [])
         .map((value) => String(value || '').trim())
         .filter(Boolean)
   )].sort((a, b) => a.localeCompare(b));
}

function normalizeExhibitKey(exhibit) {
   return String(exhibit || '').trim();
}

export function createAnimalSpeciesSource() {
   let allSpecies = [];
   let allSpeciesLoaded = false;
   const speciesByExhibit = new Map();

   async function ensureAllSpeciesLoaded() {
      if (allSpeciesLoaded) {
         return allSpecies;
      }

      const rawSpecies = await loadSpecies();
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

      const animals = await getAnimalsInExhibit(exhibitKey);
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
