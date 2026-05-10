import { buildAnimalVisibilityChanges } from './diff/animalVisibility.js';
import { mergeRemovedItems } from './diff/removedItems.js';
import {
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   isValidatedItineraryEmpty,
} from './diff/summary.js';

function buildRemovedItems(previous, validated, backendRemoved = {}) {
   return {
      animals: mergeRemovedItems(
         backendRemoved.animals,
         previous.animals,
         validated.animals,
         'species'
      ),
      attractions: mergeRemovedItems(
         backendRemoved.attractions,
         previous.attractions,
         validated.attractions,
         'name'
      ),
      guardiansTalks: mergeRemovedItems(
         backendRemoved.guardiansTalks,
         previous.guardiansTalks,
         validated.guardiansTalks,
         'name'
      ),
      wildEncounters: mergeRemovedItems(
         backendRemoved.wildEncounters,
         previous.wildEncounters,
         validated.wildEncounters,
         'name'
      ),
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
