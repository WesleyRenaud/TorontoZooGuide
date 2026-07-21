import {
   likelihoodToFraction,
   likelihoodToPercent,
} from '../likelihood/likelihoodValues.js';
import { normalizeNonNegativeNumber } from './panel/format.js';
import { buildSpeciesExhibitKey } from './speciesExhibitKey.js';
import {
   hasAddedItems,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   hasUnscheduledItems,
} from './wizard/itineraryDiff.js';

function maxStoredLikelihood(...values) {
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

function aggregateAnimalsForVisibilityComparison(animals = []) {
   const aggregatedBySpeciesExhibit = new Map();

   animals.forEach((animal) => {
      const key = buildSpeciesExhibitKey(animal);

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
         likelihood: maxStoredLikelihood(existing.likelihood, animal.likelihood),
         old_likelihood: maxStoredLikelihood(
            existing.old_likelihood,
            animal.old_likelihood
         ),
      });
   });

   return Array.from(aggregatedBySpeciesExhibit.values());
}

function hasMeaningfulVisibilityChange(item, visibilityChangeThreshold) {
   const before = likelihoodToFraction(item.old_likelihood);
   const after = likelihoodToFraction(item.likelihood);
   const threshold = likelihoodToFraction(visibilityChangeThreshold);

   if (before == null || after == null || threshold == null) {
      return false;
   }

   return Math.abs(after - before) >= threshold;
}

function withVisibilityFields(item) {
   return {
      ...item,
      likelihoodBefore: item.old_likelihood,
      likelihoodAfter: item.likelihood,
   };
}

function hasStoredOldLikelihood(item) {
   return item.old_likelihood != null;
}

function isRemovedForValidation(item, animalMinLikelihood) {
   const after = likelihoodToPercent(item.likelihood);

   return (
      hasStoredOldLikelihood(item)
      && after != null
      && animalMinLikelihood != null
      && after < animalMinLikelihood
   );
}

function buildRemovedAnimals(animals = [], animalMinLikelihood) {
   return animals
      .filter((animal) => isRemovedForValidation(animal, animalMinLikelihood))
      .map(withVisibilityFields);
}

function buildReducedVisibilityAnimals(
   animals = [],
   visibilityChangeThreshold,
   animalMinLikelihood
) {
   return animals
      .filter((animal) => animal.is_added !== true)
      .filter((animal) => !isRemovedForValidation(animal, animalMinLikelihood))
      .filter((animal) => {
         const before = likelihoodToFraction(animal.old_likelihood);
         const after = likelihoodToFraction(animal.likelihood);

         return (
            hasMeaningfulVisibilityChange(animal, visibilityChangeThreshold)
            && after < before
         );
      })
      .map(withVisibilityFields);
}

function buildImprovedVisibilityAnimals(animals = [], visibilityChangeThreshold) {
   return animals
      .filter((animal) => animal.is_added !== true)
      .filter((animal) => {
         const before = likelihoodToFraction(animal.old_likelihood);
         const after = likelihoodToFraction(animal.likelihood);

         return (
            hasMeaningfulVisibilityChange(animal, visibilityChangeThreshold)
            && after > before
         );
      })
      .map(withVisibilityFields);
}

function buildAddedAnimals(animals = []) {
   return animals
      .filter((animal) => animal.is_added === true)
      .map(withVisibilityFields);
}

function buildRemovedAttractions(attractions = [], animalMinLikelihood) {
   return attractions
      .filter((attraction) => isRemovedForValidation(attraction, animalMinLikelihood))
      .map(withVisibilityFields);
}

function buildRemovedScheduledItems(items = []) {
   return items.filter((item) => item.is_deleted === true);
}

export function buildItineraryValidationState(
   itinerary = {},
   {
      animalVisibilityChangeThreshold,
      itineraryAnimalMinLikelihood,
   } = {}
) {
   const visibilityChangeThreshold = normalizeNonNegativeNumber(
      animalVisibilityChangeThreshold
   );
   const animalMinLikelihood = normalizeNonNegativeNumber(
      itineraryAnimalMinLikelihood
   );
   const visibilityAnimals = aggregateAnimalsForVisibilityComparison(
      itinerary.animals
   );
   const removed = {
      animals: buildRemovedAnimals(visibilityAnimals, animalMinLikelihood),
      attractions: buildRemovedAttractions(
         itinerary.attractions,
         animalMinLikelihood
      ),
      guardiansTalks: buildRemovedScheduledItems(itinerary.guardiansTalks),
      wildEncounters: buildRemovedScheduledItems(itinerary.wildEncounters),
   };
   const added = {
      animals: buildAddedAnimals(itinerary.animals),
   };
   const reducedVisibility = {
      animals: buildReducedVisibilityAnimals(
         visibilityAnimals,
         visibilityChangeThreshold,
         animalMinLikelihood
      ),
   };
   const improvedVisibility = {
      animals: buildImprovedVisibilityAnimals(
         visibilityAnimals,
         visibilityChangeThreshold
      ),
   };
   const unscheduled = {
      animals: [],
      attractions: [],
   };

   return {
      removed,
      unscheduled,
      added,
      reducedVisibility,
      improvedVisibility,
      adjustments: [],
      hasChanges: (
         hasAddedItems(added)
         || hasRemovedItems(removed)
         || hasUnscheduledItems(unscheduled)
         || hasReducedVisibility(reducedVisibility)
         || hasImprovedVisibility(improvedVisibility)
      ),
   };
}
