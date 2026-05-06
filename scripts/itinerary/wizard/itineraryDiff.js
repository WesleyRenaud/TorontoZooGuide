import { buildAnimalVisibilityChanges } from './diff/animalVisibility.js';
import { findRemovedItemsByField } from './diff/removedItems.js';
import {
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   isValidatedItineraryEmpty,
} from './diff/summary.js';

function buildRemovedItems(previous, validated, backendRemoved = {}) {
   return {
      animals: backendRemoved.animals
         ?? findRemovedItemsByField(previous.animals, validated.animals, 'species'),
      attractions: backendRemoved.attractions
         ?? findRemovedItemsByField(previous.attractions, validated.attractions, 'name'),
      guardiansTalks: backendRemoved.guardiansTalks
         ?? findRemovedItemsByField(previous.guardiansTalks, validated.guardiansTalks, 'name'),
      wildEncounters: backendRemoved.wildEncounters
         ?? findRemovedItemsByField(previous.wildEncounters, validated.wildEncounters, 'name'),
   };
}

function buildAnimalVisibilityDiff(previous, validated, removed) {
   return buildAnimalVisibilityChanges(
      previous.animals,
      validated.animals,
      removed.animals,
      0.2
   );
}

export function buildItineraryDiff(previous, validated, backendRemoved = {}) {
   const removed = buildRemovedItems(previous, validated, backendRemoved);
   const visibilityChanges = buildAnimalVisibilityDiff(previous, validated, removed);

   return {
      removed,
      reducedVisibility: {
         animals: visibilityChanges.reduced,
      },
      improvedVisibility: {
         animals: visibilityChanges.improved,
      },
   };
}

export {
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   isValidatedItineraryEmpty,
};
