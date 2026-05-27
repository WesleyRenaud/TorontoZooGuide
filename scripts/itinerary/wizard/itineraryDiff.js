import { buildAnimalVisibilityChanges } from './diff/animalVisibility.js';
import { mergeRemovedItems } from './diff/removedItems.js';
import {
   hasAddedItems,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   isValidatedItineraryEmpty,
} from './diff/summary.js';
import { normalizeNonNegativeNumber } from '../panel/format.js';

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

function buildAnimalVisibilityDiff(previous, validated, removed, minDelta = null) {
   return buildAnimalVisibilityChanges(
      previous.animals,
      validated.animals,
      removed.animals,
      minDelta
   );
}

export function buildItineraryDiff(
   previous,
   validated,
   backendRemoved = {},
   { animalVisibilityChangeThreshold } = {}
) {
   const removed = buildRemovedItems(previous, validated, backendRemoved);
   const minDelta = normalizeNonNegativeNumber(animalVisibilityChangeThreshold);
   const visibilityChanges = buildAnimalVisibilityDiff(previous, validated, removed, (
      minDelta == null ? undefined : minDelta / 100
   ));

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
   hasAddedItems,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   isValidatedItineraryEmpty,
};
