import {
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
} from './wizard/itineraryDiff.js';

function normalizeLikelihood(value) {
   if (value == null || value === '') {
      return null;
   }

   const likelihood = Number(value);

   if (!Number.isFinite(likelihood)) {
      return null;
   }

   return likelihood > 1 ? likelihood / 100 : likelihood;
}

function hasMeaningfulVisibilityChange(item) {
   const before = normalizeLikelihood(item.old_likelihood);
   const after = normalizeLikelihood(item.likelihood);

   if (before == null || after == null) {
      return false;
   }

   return Math.abs(after - before) >= 0.2;
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
      .filter((animal) => normalizeLikelihood(animal.likelihood) === 0)
      .map(withVisibilityFields);
}

function buildReducedVisibilityAnimals(animals = []) {
   return animals
      .filter((animal) => {
         const before = normalizeLikelihood(animal.old_likelihood);
         const after = normalizeLikelihood(animal.likelihood);

         return hasMeaningfulVisibilityChange(animal) && after < before;
      })
      .map(withVisibilityFields);
}

function buildImprovedVisibilityAnimals(animals = []) {
   return animals
      .filter((animal) => {
         const before = normalizeLikelihood(animal.old_likelihood);
         const after = normalizeLikelihood(animal.likelihood);

         return hasMeaningfulVisibilityChange(animal) && after > before;
      })
      .map(withVisibilityFields);
}

function buildRemovedAttractions(attractions = []) {
   return attractions
      .filter((attraction) => normalizeLikelihood(attraction.likelihood) === 0)
      .map(withVisibilityFields);
}

function buildRemovedScheduledItems(items = []) {
   return items.filter((item) => item.is_deleted === true);
}

export function buildItineraryValidationState(itinerary = {}) {
   const removed = {
      animals: buildRemovedAnimals(itinerary.animals),
      attractions: buildRemovedAttractions(itinerary.attractions),
      guardiansTalks: buildRemovedScheduledItems(itinerary.guardiansTalks),
      wildEncounters: buildRemovedScheduledItems(itinerary.wildEncounters),
   };
   const reducedVisibility = {
      animals: buildReducedVisibilityAnimals(itinerary.animals),
   };
   const improvedVisibility = {
      animals: buildImprovedVisibilityAnimals(itinerary.animals),
   };

   return {
      removed,
      reducedVisibility,
      improvedVisibility,
      hasChanges: (
         hasRemovedItems(removed)
         || hasReducedVisibility(reducedVisibility)
         || hasImprovedVisibility(improvedVisibility)
      ),
   };
}
