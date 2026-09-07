import { ItemKey } from './diff/itemKey.js';
import { ItineraryDiffBuilder } from './itineraryDiffBuilder.js';
import { ItineraryItemFormatter } from '../panel/itineraryItemFormatter.js';
import { SpeciesExhibitKey } from '../speciesExhibitKey.js';

export class ItineraryDiff {
   static mergeRemovedValidationState(
      existingRemoved = {},
      diffRemoved = {}) {
      return {
         animals: ItineraryDiffBuilder.mergeRemovedItemLists(
            existingRemoved.animals,
            diffRemoved.animals,
            SpeciesExhibitKey.buildSpeciesExhibitKey),
         attractions: ItineraryDiffBuilder.mergeRemovedItemLists(
            existingRemoved.attractions,
            diffRemoved.attractions,
            (item) => ItemKey.buildItemKey(item, 'name')),
         guardiansTalks: ItineraryDiffBuilder.mergeRemovedItemLists(
            existingRemoved.guardiansTalks,
            diffRemoved.guardiansTalks,
            (item) => ItemKey.buildItemKey(item, 'name')),
         wildEncounters: ItineraryDiffBuilder.mergeRemovedItemLists(
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
      const removed = ItineraryDiffBuilder.buildRemovedItems(previous, validated, backendRemoved);
      const unscheduled = ItineraryDiffBuilder.buildUnscheduledItems(previous, validated);
      const minDelta = ItineraryItemFormatter.normalizeNonNegativeNumber(animalVisibilityChangeThreshold);
      const visibilityChanges = ItineraryDiffBuilder.buildAnimalVisibilityDiff(previous, validated, removed, (
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
