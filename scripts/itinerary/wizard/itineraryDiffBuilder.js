import { AnimalPresenter } from './diff/animalPresenter.js';
import { ItemKey } from './diff/itemKey.js';
import { RemovedItems } from './diff/removedItems.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { SpeciesExhibitKey } from '../speciesExhibitKey.js';

export class ItineraryDiffBuilder {
   static validatedAttractionPresenceItems(validated) {
      return [
         ...validated.attractions,
         ...validated.transportations.filter(TransportationSelectorModel.isTransportationAddedAsAttraction),
      ];
   }

   static buildRemovedItems(previous, validated, backendRemoved = {}) {
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
            ItineraryDiffBuilder.validatedAttractionPresenceItems(validated),
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

   static buildAnimalVisibilityDiff(previous, validated, removed, minDelta = null) {
      return AnimalPresenter.buildAnimalVisibilityChanges(
         previous.animals,
         validated.animals,
         removed.animals,
         minDelta
      );
   }

   static hasScheduleTimes(item) {
      return Boolean(item?.start_time && item?.end_time);
   }

   static buildUnscheduledItemsByKey(previousItems = [], validatedItems = [], buildKey) {
      const validatedByKey = new Map();

      validatedItems.forEach((item) => {
         const key = buildKey(item);

         if (key) {
            validatedByKey.set(key, item);
         }
      });

      return previousItems.filter((item) => {
         if (!ItineraryDiffBuilder.hasScheduleTimes(item)) {
            return false;
         }

         const key = buildKey(item);
         const validatedItem = key ? validatedByKey.get(key) : null;

         return Boolean(validatedItem && !ItineraryDiffBuilder.hasScheduleTimes(validatedItem));
      });
   }

   static buildUnscheduledItems(previous, validated) {
      // Talks and encounters use is_deleted or drop from validated; only animals and
      // attractions can lose schedule times while staying active.
      return {
         animals: ItineraryDiffBuilder.buildUnscheduledItemsByKey(
            previous.animals,
            validated.animals,
            SpeciesExhibitKey.buildSpeciesExhibitKey
         ),
         attractions: ItineraryDiffBuilder.buildUnscheduledItemsByKey(
            previous.attractions,
            ItineraryDiffBuilder.validatedAttractionPresenceItems(validated),
            (item) => ItemKey.buildItemKey(item, 'name')
         ),
      };
   }

   static mergeRemovedItemLists(existing = [], incoming = [], buildKey) {
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
}
