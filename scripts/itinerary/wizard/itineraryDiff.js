import { AnimalVisibility } from './diff/animalVisibility.js';
import { ItemKey } from './diff/itemKey.js';
import { RemovedItems } from './diff/removedItems.js';
import { normalizeNonNegativeNumber } from '../panel/format.js';
import { isTransportationAddedAsAttraction } from '../selectors/transportationSelector/model.js';
import { SpeciesExhibitKey } from '../speciesExhibitKey.js';

function validatedAttractionPresenceItems(validated) {
   return [
      ...validated.attractions,
      ...validated.transportations.filter(isTransportationAddedAsAttraction),
   ];
}

function buildRemovedItems(previous, validated, backendRemoved = {}) {
   return {
      animals: RemovedItems.mergeRemovedItems(
         backendRemoved.animals,
         previous.animals,
         validated.animals,
         'species'
      ),
      attractions: RemovedItems.mergeRemovedItems(
         backendRemoved.attractions,
         previous.attractions,
         validatedAttractionPresenceItems(validated),
         'name'
      ),
      guardiansTalks: RemovedItems.mergeRemovedItems(
         backendRemoved.guardiansTalks,
         previous.guardiansTalks,
         validated.guardiansTalks,
         'name'
      ),
      wildEncounters: RemovedItems.mergeRemovedItems(
         backendRemoved.wildEncounters,
         previous.wildEncounters,
         validated.wildEncounters,
         'name'
      ),
   };
}

function buildAnimalVisibilityDiff(previous, validated, removed, minDelta = null) {
   return AnimalVisibility.buildAnimalVisibilityChanges(
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
   // Talks and encounters use is_deleted or drop from validated; only animals and
   // attractions can lose schedule times while staying active.
   return {
      animals: buildUnscheduledItemsByKey(
         previous.animals,
         validated.animals,
         SpeciesExhibitKey.buildSpeciesExhibitKey
      ),
      attractions: buildUnscheduledItemsByKey(
         previous.attractions,
         validatedAttractionPresenceItems(validated),
         (item) => ItemKey.buildItemKey(item, 'name')
      ),
   };
}

function mergeRemovedItemLists(existing = [], incoming = [], buildKey) {
   const merged = [...existing];
   const keys = new Set(
      existing
         .map((item) => buildKey(item))
         .filter(Boolean)
   );

   incoming.forEach((item) => {
      const key = buildKey(item);

      if (!key || keys.has(key)) {
         return;
      }

      merged.push(item);
      keys.add(key);
   });

   return merged;
}

export class ItineraryDiff {
   static mergeRemovedValidationState(
      existingRemoved = {},
      diffRemoved = {}) {
      return {
         animals: mergeRemovedItemLists(
            existingRemoved.animals,
            diffRemoved.animals,
            SpeciesExhibitKey.buildSpeciesExhibitKey),
         attractions: mergeRemovedItemLists(
            existingRemoved.attractions,
            diffRemoved.attractions,
            (item) => ItemKey.buildItemKey(item, 'name')),
         guardiansTalks: mergeRemovedItemLists(
            existingRemoved.guardiansTalks,
            diffRemoved.guardiansTalks,
            (item) => ItemKey.buildItemKey(item, 'name')),
         wildEncounters: mergeRemovedItemLists(
            existingRemoved.wildEncounters,
            diffRemoved.wildEncounters,
            (item) => ItemKey.buildItemKey(item, 'name')),
      };
   }

   static buildItineraryDiff(
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
}
