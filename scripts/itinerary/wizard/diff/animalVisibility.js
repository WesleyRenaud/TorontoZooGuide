import { buildItemKey } from './itemKey.js';
import { likelihoodToFraction } from '../../../likelihood/likelihoodValues.js';

function getAnimalLikelihood(animal) {
   return likelihoodToFraction(animal?.likelihood);
}

function buildAnimalsBySpecies(animals = []) {
   const bestBySpecies = new Map();

   animals.forEach((animal) => {
      const speciesKey = buildItemKey(animal, 'species');

      if (!speciesKey) {
         return;
      }

      const likelihood = getAnimalLikelihood(animal);
      const currentBest = bestBySpecies.get(speciesKey);

      if (!currentBest) {
         bestBySpecies.set(speciesKey, animal);
         return;
      }

      if (likelihood == null) {
         return;
      }

      const currentBestLikelihood = getAnimalLikelihood(currentBest);

      if (currentBestLikelihood == null || likelihood > currentBestLikelihood) {
         bestBySpecies.set(speciesKey, animal);
      }
   });

   return bestBySpecies;
}

function buildRemovedSpeciesKeys(removedAnimals = []) {
   return new Set(
      removedAnimals
         .map((animal) => buildItemKey(animal, 'species'))
         .filter(Boolean)
   );
}

export function buildAnimalVisibilityChanges(
   previousAnimals = [],
   validatedAnimals = [],
   removedAnimals = [],
   minDelta = 0.2
) {
   const previousBySpecies = buildAnimalsBySpecies(previousAnimals);
   const validatedBySpecies = buildAnimalsBySpecies(validatedAnimals);
   const removedSpeciesKeys = buildRemovedSpeciesKeys(removedAnimals);

   const reduced = [];
   const improved = [];

   previousBySpecies.forEach((previousAnimal, speciesKey) => {
      if (removedSpeciesKeys.has(speciesKey)) {
         return;
      }

      const validatedAnimal = validatedBySpecies.get(speciesKey);

      if (!validatedAnimal) {
         return;
      }

      const likelihoodBefore = getAnimalLikelihood(previousAnimal);
      const likelihoodAfter = getAnimalLikelihood(validatedAnimal);

      if (likelihoodBefore == null || likelihoodAfter == null) {
         return;
      }

      const delta = likelihoodAfter - likelihoodBefore;

      if (minDelta == null || Math.abs(delta) < minDelta) {
         return;
      }

      const changedAnimal = {
         ...validatedAnimal,
         likelihoodBefore,
         likelihoodAfter,
      };

      if (delta < 0) {
         reduced.push(changedAnimal);
      } else if (delta > 0) {
         improved.push(changedAnimal);
      }
   });

   return {
      reduced,
      improved,
   };
}
