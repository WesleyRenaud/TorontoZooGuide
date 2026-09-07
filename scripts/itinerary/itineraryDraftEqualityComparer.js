import { AnimalIdentity } from './animalIdentity.js';

export class ItineraryDraftEqualityComparer {
   static areObjectsEqual(left, right) {
      const leftKeys = Object.keys(left);
      const rightKeys = Object.keys(right);

      if (leftKeys.length !== rightKeys.length) {
         return false;
      }

      return leftKeys.every((key) => (
         Object.hasOwn(right, key)
         && ItineraryDraftEqualityComparer.areDraftValuesEqual(left[key], right[key])
      ));
   }

   static areDraftValuesEqual(left, right) {
      if (left === right) {
         return true;
      }

      if (Array.isArray(left) || Array.isArray(right)) {
         if (!Array.isArray(left) || !Array.isArray(right)) {
            return false;
         }

         if (left.length !== right.length) {
            return false;
         }

         return left.every((value, index) => (
            ItineraryDraftEqualityComparer.areDraftValuesEqual(value, right[index])
         ));
      }

      if (!left || !right) {
         return false;
      }

      if (typeof left !== 'object' || typeof right !== 'object') {
         return false;
      }

      return ItineraryDraftEqualityComparer.areObjectsEqual(left, right);
   }

   static sortStringsForComparison(values = []) {
      return [...values].map((item) => String(item)).sort((a, b) => a.localeCompare(b));
   }

   static sortWildEncountersForSaveComparison(items = []) {
      return ItineraryDraftEqualityComparer.sortStringsForComparison(items);
   }

   static sortAnimalsForSaveComparison(animals = []) {
      return [...animals].sort((a, b) => (
         AnimalIdentity.buildAnimalIdentityComparisonKey(a).localeCompare(
            AnimalIdentity.buildAnimalIdentityComparisonKey(b)
         )
      ));
   }

   static sortScheduledItemsForSaveComparison(items = []) {
      return [...items].sort((left, right) => (
         left.name.localeCompare(right.name)
      ));
   }

   static sortTransportationsForSaveComparison(items = []) {
      return [...items].sort((left, right) => (
         left.name.localeCompare(right.name)
      ));
   }

   static areItineraryDraftSaveItemSelectionsEqual(leftSave, rightSave) {
      if (leftSave.arrivalTime !== rightSave.arrivalTime) {
         return false;
      }

      if (leftSave.departureTime !== rightSave.departureTime) {
         return false;
      }

      if (
         !ItineraryDraftEqualityComparer.areDraftValuesEqual(
            ItineraryDraftEqualityComparer.sortAnimalsForSaveComparison(leftSave.animals),
            ItineraryDraftEqualityComparer.sortAnimalsForSaveComparison(rightSave.animals),
         )
      ) {
         return false;
      }

      return ItineraryDraftEqualityComparer.areDraftValuesEqual(
         ItineraryDraftEqualityComparer.sortStringsForComparison(leftSave.attractions),
         ItineraryDraftEqualityComparer.sortStringsForComparison(rightSave.attractions),
      )
      && ItineraryDraftEqualityComparer.areDraftValuesEqual(
         ItineraryDraftEqualityComparer.sortTransportationsForSaveComparison(leftSave.transportations),
         ItineraryDraftEqualityComparer.sortTransportationsForSaveComparison(rightSave.transportations),
      )
      && ItineraryDraftEqualityComparer.areDraftValuesEqual(
         ItineraryDraftEqualityComparer.sortScheduledItemsForSaveComparison(leftSave.guardiansTalks),
         ItineraryDraftEqualityComparer.sortScheduledItemsForSaveComparison(rightSave.guardiansTalks),
      )
      && ItineraryDraftEqualityComparer.areDraftValuesEqual(
         ItineraryDraftEqualityComparer.sortWildEncountersForSaveComparison(leftSave.wildEncounters),
         ItineraryDraftEqualityComparer.sortWildEncountersForSaveComparison(rightSave.wildEncounters),
      );
   }
}
