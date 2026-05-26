import { likelihoodToFraction } from '../likelihood/likelihoodValues.js';
import {
   hasAddedItems,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
} from './wizard/itineraryDiff.js';

function hasMeaningfulVisibilityChange(item) {
   const before = likelihoodToFraction(item.old_likelihood);
   const after = likelihoodToFraction(item.likelihood);

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
      .filter((animal) => likelihoodToFraction(animal.likelihood) === 0)
      .map(withVisibilityFields);
}

function buildReducedVisibilityAnimals(animals = []) {
   return animals
      .filter((animal) => {
         const before = likelihoodToFraction(animal.old_likelihood);
         const after = likelihoodToFraction(animal.likelihood);

         return hasMeaningfulVisibilityChange(animal) && after < before;
      })
      .map(withVisibilityFields);
}

function buildImprovedVisibilityAnimals(animals = []) {
   return animals
      .filter((animal) => {
         const before = likelihoodToFraction(animal.old_likelihood);
         const after = likelihoodToFraction(animal.likelihood);

         return hasMeaningfulVisibilityChange(animal) && after > before;
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

export function buildItineraryValidationState(itinerary = {}) {
   const removed = {
      animals: buildRemovedAnimals(itinerary.animals),
      attractions: buildRemovedAttractions(itinerary.attractions),
      guardiansTalks: buildRemovedScheduledItems(itinerary.guardiansTalks),
      wildEncounters: buildRemovedScheduledItems(itinerary.wildEncounters),
   };
   const added = {
      animals: buildAddedAnimals(itinerary.animals),
   };
   const reducedVisibility = {
      animals: buildReducedVisibilityAnimals(itinerary.animals),
   };
   const improvedVisibility = {
      animals: buildImprovedVisibilityAnimals(itinerary.animals),
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
