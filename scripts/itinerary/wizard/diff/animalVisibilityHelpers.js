import { ItemKey } from './itemKey.js';
import { LikelihoodValues } from '../../../likelihood/likelihoodValues.js';

export class AnimalVisibilityHelpers {
   static getAnimalLikelihood(animal) {
      return LikelihoodValues.likelihoodToFraction(animal?.likelihood);
   }

   static buildAnimalsBySpecies(animals = []) {
      const bestBySpecies = new Map();

      animals.forEach((animal) => {
         const speciesKey = ItemKey.buildItemKey(animal, 'species');

         if (!speciesKey) {
            return;
         }

         const likelihood = AnimalVisibilityHelpers.getAnimalLikelihood(animal);
         const currentBest = bestBySpecies.get(speciesKey);

         if (!currentBest) {
            bestBySpecies.set(speciesKey, animal);
            return;
         }

         if (likelihood == null) {
            return;
         }

         const currentBestLikelihood = AnimalVisibilityHelpers.getAnimalLikelihood(currentBest);

         if (currentBestLikelihood == null || likelihood > currentBestLikelihood) {
            bestBySpecies.set(speciesKey, animal);
         }
      });

      return bestBySpecies;
   }

   static buildRemovedSpeciesKeys(removedAnimals = []) {
      return new Set(
         removedAnimals
            .map((animal) => ItemKey.buildItemKey(animal, 'species'))
            .filter(Boolean)
      );
   }
}
