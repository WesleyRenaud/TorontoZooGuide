import { buildAnimalVisibilityChanges } from './diff/animalVisibility.js';
import { buildItemKey } from './diff/itemKey.js';
import { mergeRemovedItems } from './diff/removedItems.js';
import {
   hasAddedItems,
   hasImprovedVisibility,
   hasReducedVisibility,
   hasRemovedItems,
   hasUnscheduledItems,
   isValidatedItineraryEmpty,
} from './diff/summary.js';
import { normalizeNonNegativeNumber } from '../panel/format.js';
import { buildSpeciesExhibitKey } from '../speciesExhibitKey.js';

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

function hasScheduleTimes(item) {
   return Boolean(item?.start_time && item?.end_time);
}

function buildUnscheduledItemsByKey(previousItems = [], validatedItems = [], buildKey) {
   const validatedByKey = new Map();

   validatedItems.forEach((item) => {
      const key = buildKey(item);

      if (key) {
         validatedByKey.set(key, item);
      }
   });

   return previousItems.filter((item) => {
      if (!hasScheduleTimes(item)) {
         return false;
      }

      const key = buildKey(item);
      const validatedItem = key ? validatedByKey.get(key) : null;

      return Boolean(validatedItem && !hasScheduleTimes(validatedItem));
   });
}

function buildUnscheduledItems(previous, validated) {
   return {
      animals: buildUnscheduledItemsByKey(
         previous.animals,
         validated.animals,
         buildSpeciesExhibitKey
      ),
      attractions: buildUnscheduledItemsByKey(
         previous.attractions,
         validated.attractions,
         (item) => buildItemKey(item, 'name')
      ),
   };
}

export function buildItineraryDiff(
   previous,
   validated,
   backendRemoved = {},
   { animalVisibilityChangeThreshold } = {}
) {
   const removed = buildRemovedItems(previous, validated, backendRemoved);
   const unscheduled = buildUnscheduledItems(previous, validated);
   const minDelta = normalizeNonNegativeNumber(animalVisibilityChangeThreshold);
   const visibilityChanges = buildAnimalVisibilityDiff(previous, validated, removed, (
      minDelta == null ? undefined : minDelta / 100
   ));

   return {
      removed,
      unscheduled,
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
   hasUnscheduledItems,
   isValidatedItineraryEmpty,
};
