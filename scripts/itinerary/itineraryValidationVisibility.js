import { LikelihoodValues } from '../likelihood/likelihoodValues.js';
import { SpeciesExhibitKey } from './speciesExhibitKey.js';

export class ItineraryValidationVisibility {
   static maxStoredLikelihood(...values) {
      const likelihoods = values
         .map((value) => (
            value == null || value === '' ? NaN : Number(value)
         ))
         .filter((value) => Number.isFinite(value));

      if (!likelihoods.length) {
         return null;
      }

      return Math.max(...likelihoods);
   }

   static aggregateAnimalsForVisibilityComparison(animals = []) {
      const aggregatedBySpeciesExhibit = new Map();

      animals.forEach((animal) => {
         const key = SpeciesExhibitKey.buildSpeciesExhibitKey(animal);

         if (!key) {
            return;
         }

         const existing = aggregatedBySpeciesExhibit.get(key);

         if (!existing) {
            aggregatedBySpeciesExhibit.set(key, { ...animal });
            return;
         }

         aggregatedBySpeciesExhibit.set(key, {
            ...existing,
            likelihood: ItineraryValidationVisibility.maxStoredLikelihood(existing.likelihood, animal.likelihood),
            old_likelihood: ItineraryValidationVisibility.maxStoredLikelihood(
               existing.old_likelihood,
               animal.old_likelihood
            ),
         });
      });

      return Array.from(aggregatedBySpeciesExhibit.values());
   }

   static hasMeaningfulVisibilityChange(item, visibilityChangeThreshold) {
      const before = LikelihoodValues.likelihoodToFraction(item.old_likelihood);
      const after = LikelihoodValues.likelihoodToFraction(item.likelihood);
      const threshold = LikelihoodValues.likelihoodToFraction(visibilityChangeThreshold);

      if (before == null || after == null || threshold == null) {
         return false;
      }

      return Math.abs(after - before) >= threshold;
   }

   static withVisibilityFields(item) {
      return {
         ...item,
         likelihoodBefore: item.old_likelihood,
         likelihoodAfter: item.likelihood,
      };
   }

   static hasStoredOldLikelihood(item) {
      return item.old_likelihood != null;
   }

   static isRemovedForValidation(item, animalMinLikelihood) {
      const after = LikelihoodValues.likelihoodToPercent(item.likelihood);

      return (
         ItineraryValidationVisibility.hasStoredOldLikelihood(item)
         && after != null
         && animalMinLikelihood != null
         && after < animalMinLikelihood
      );
   }

   static buildRemovedAnimals(animals = [], animalMinLikelihood) {
      return animals
         .filter((animal) => ItineraryValidationVisibility.isRemovedForValidation(animal, animalMinLikelihood))
         .map(ItineraryValidationVisibility.withVisibilityFields);
   }

   static buildReducedVisibilityAnimals(
      animals = [],
      visibilityChangeThreshold,
      animalMinLikelihood
   ) {
      return animals
         .filter((animal) => animal.is_added !== true)
         .filter((animal) => !ItineraryValidationVisibility.isRemovedForValidation(animal, animalMinLikelihood))
         .filter((animal) => {
            const before = LikelihoodValues.likelihoodToFraction(animal.old_likelihood);
            const after = LikelihoodValues.likelihoodToFraction(animal.likelihood);

            return (
               ItineraryValidationVisibility.hasMeaningfulVisibilityChange(animal, visibilityChangeThreshold)
               && after < before
            );
         })
         .map(ItineraryValidationVisibility.withVisibilityFields);
   }

   static buildImprovedVisibilityAnimals(animals = [], visibilityChangeThreshold) {
      return animals
         .filter((animal) => animal.is_added !== true)
         .filter((animal) => {
            const before = LikelihoodValues.likelihoodToFraction(animal.old_likelihood);
            const after = LikelihoodValues.likelihoodToFraction(animal.likelihood);

            return (
               ItineraryValidationVisibility.hasMeaningfulVisibilityChange(animal, visibilityChangeThreshold)
               && after > before
            );
         })
         .map(ItineraryValidationVisibility.withVisibilityFields);
   }

   static buildAddedAnimals(animals = []) {
      return animals
         .filter((animal) => animal.is_added === true)
         .map(ItineraryValidationVisibility.withVisibilityFields);
   }

   static buildRemovedAttractions(attractions = [], animalMinLikelihood) {
      return attractions
         .filter((attraction) => ItineraryValidationVisibility.isRemovedForValidation(attraction, animalMinLikelihood))
         .map(ItineraryValidationVisibility.withVisibilityFields);
   }

   static buildRemovedScheduledItems(items = []) {
      return items.filter((item) => item.is_deleted === true);
   }
}
