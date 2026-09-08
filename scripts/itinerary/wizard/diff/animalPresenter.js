import { AnimalVisibilityHelper } from './animalVisibilityHelper.js';

export class AnimalPresenter {
   static buildAnimalVisibilityChanges(
      previousAnimals = [],
      validatedAnimals = [],
      removedAnimals = [],
      minDelta = 0.2
   ) {
      const previousBySpecies = AnimalVisibilityHelper.buildAnimalsBySpecies(previousAnimals);
      const validatedBySpecies = AnimalVisibilityHelper.buildAnimalsBySpecies(validatedAnimals);
      const removedSpeciesKeys = AnimalVisibilityHelper.buildRemovedSpeciesKeys(removedAnimals);

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

         const likelihoodBefore = AnimalVisibilityHelper.getAnimalLikelihood(previousAnimal);
         const likelihoodAfter = AnimalVisibilityHelper.getAnimalLikelihood(validatedAnimal);

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
}
