import { likelihoodToFraction } from '../likelihood/likelihoodValues.js';
import { normalizeNonNegativeNumber } from './panel/format.js';
import {
   hasAddedItems,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
} from './wizard/itineraryDiff.js';

function buildSpeciesExhibitKey(animal) {
   const species = String(animal?.species ?? '').trim().toLowerCase();
   const exhibit = String(animal?.exhibit ?? '').trim().toLowerCase();

   if (!species) {
      return '';
   }

   return `${species}|${exhibit}`;
}

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

function buildRemovedAnimals(animals = []) {
   return animals
      .filter((animal) => likelihoodToFraction(animal.likelihood) === 0)
      .map(withVisibilityFields);
}

function buildReducedVisibilityAnimals(animals = [], visibilityChangeThreshold) {
   return animals
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
   return animals.filter((animal) => animal.is_added === true);
}

function buildRemovedAttractions(attractions = []) {
   return attractions
      .filter((attraction) => likelihoodToFraction(attraction.likelihood) === 0)
      .map(withVisibilityFields);
}

function buildRemovedScheduledItems(items = []) {
   return items.filter((item) => item.is_deleted === true);
}

export function buildItineraryValidationState(
   itinerary = {},
   { animalVisibilityChangeThreshold } = {}
) {
   const visibilityChangeThreshold = normalizeNonNegativeNumber(
      animalVisibilityChangeThreshold
   );
   const visibilityAnimals = aggregateAnimalsForVisibilityComparison(
      itinerary.animals
   );
   const removed = {
      animals: buildRemovedAnimals(visibilityAnimals),
      attractions: buildRemovedAttractions(itinerary.attractions),
      guardiansTalks: buildRemovedScheduledItems(itinerary.guardiansTalks),
      wildEncounters: buildRemovedScheduledItems(itinerary.wildEncounters),
   };
   const added = {
      animals: buildAddedAnimals(itinerary.animals),
   };
   const reducedVisibility = {
      animals: buildReducedVisibilityAnimals(
         visibilityAnimals,
         visibilityChangeThreshold
      ),
   };
   const improvedVisibility = {
      animals: buildImprovedVisibilityAnimals(
         visibilityAnimals,
         visibilityChangeThreshold
      ),
   };

   return {
      removed,
      added,
      reducedVisibility,
      improvedVisibility,
      hasChanges: (
         hasAddedItems(added)
         || hasRemovedItems(removed)
         || hasReducedVisibility(reducedVisibility)
         || hasImprovedVisibility(improvedVisibility)
      ),
   };
}
