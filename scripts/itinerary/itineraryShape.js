import {
   buildAnimalIdentityComparisonKey,
   normalizeAnimalForSave,
} from './animalIdentity.js';
import {
   normalizeGuardiansTalkForSave,
   normalizeItineraryNamesForSave,
   normalizeWildEncounterListForSave,
} from './panel/format.js';

export const ITINERARY_ITEM_KEYS = Object.freeze([
   'animals',
   'attractions',
   'guardiansTalks',
   'wildEncounters',
]);

function asItineraryDraftSource(value) {
   return value && typeof value === 'object'
      ? value
      : {};
}

function normalizeItineraryDate(value) {
   return typeof value === 'string'
      ? value
      : '';
}

function normalizeItineraryTime(value) {
   return typeof value === 'string'
      ? value
      : '';
}

export function normalizeItineraryItems(items) {
   return Array.isArray(items)
      ? items
      : [];
}

function cloneItineraryItems(items) {
   return items.slice();
}

function areObjectsEqual(left, right) {
   const leftKeys = Object.keys(left);
   const rightKeys = Object.keys(right);

   if (leftKeys.length !== rightKeys.length) {
      return false;
   }

   return leftKeys.every((key) => (
      Object.hasOwn(right, key)
      && areDraftValuesEqual(left[key], right[key])
   ));
}

function areDraftValuesEqual(left, right) {
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
         areDraftValuesEqual(value, right[index])
      ));
   }

   if (!left || !right) {
      return false;
   }

   if (typeof left !== 'object' || typeof right !== 'object') {
      return false;
   }

   return areObjectsEqual(left, right);
}

export function createEmptyItineraryDraft() {
   return {
      date: '',
      arrivalTime: '',
      departureTime: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      events: [],
   };
}

export function normalizeItineraryDraft(draft = {}) {
   const source = asItineraryDraftSource(draft);

   return {
      date: normalizeItineraryDate(source.date),
      arrivalTime: normalizeItineraryTime(source.arrivalTime),
      departureTime: normalizeItineraryTime(source.departureTime),
      animals: normalizeItineraryItems(source.animals),
      attractions: normalizeItineraryItems(source.attractions),
      guardiansTalks: normalizeItineraryItems(source.guardiansTalks),
      wildEncounters: normalizeItineraryItems(source.wildEncounters),
      events: normalizeItineraryItems(source.events),
   };
}

export function cloneItineraryDraft(draft = {}) {
   const normalizedDraft = normalizeItineraryDraft(draft);

   return {
      date: normalizedDraft.date,
      arrivalTime: normalizedDraft.arrivalTime,
      departureTime: normalizedDraft.departureTime,
      animals: cloneItineraryItems(normalizedDraft.animals),
      attractions: cloneItineraryItems(normalizedDraft.attractions),
      guardiansTalks: cloneItineraryItems(normalizedDraft.guardiansTalks),
      wildEncounters: cloneItineraryItems(normalizedDraft.wildEncounters),
      events: cloneItineraryItems(normalizedDraft.events),
   };
}

function normalizeGuardiansTalkListForSave(items) {
   return normalizeItineraryItems(items)
      .map(normalizeGuardiansTalkForSave)
      .filter((talk) => talk.name);
}

export function toSetItineraryPayload(draft = {}) {
   const base = normalizeItineraryDraft(draft);

   return {
      date: base.date,
      arrivalTime: base.arrivalTime,
      departureTime: base.departureTime,
      animals: base.animals.map(normalizeAnimalForSave).filter(Boolean),
      attractions: normalizeItineraryNamesForSave(base.attractions),
      guardiansTalks: normalizeGuardiansTalkListForSave(base.guardiansTalks),
      wildEncounters: normalizeWildEncounterListForSave(base.wildEncounters),
   };
}

function sortStringsForComparison(values = []) {
   return [...values].map((item) => String(item)).sort((a, b) => a.localeCompare(b));
}

function sortWildEncountersForSaveComparison(items = []) {
   return sortStringsForComparison(items);
}

function sortAnimalsForSaveComparison(animals = []) {
   return [...animals].sort((a, b) => (
      buildAnimalIdentityComparisonKey(a).localeCompare(
         buildAnimalIdentityComparisonKey(b)
      )
   ));
}

function areItineraryDraftSaveItemSelectionsEqual(
      leftSave,
      rightSave) {
   if (leftSave.arrivalTime !== rightSave.arrivalTime) {
      return false;
   }

   if (leftSave.departureTime !== rightSave.departureTime) {
      return false;
   }

   if (
      !areDraftValuesEqual(
         sortAnimalsForSaveComparison(leftSave.animals),
         sortAnimalsForSaveComparison(rightSave.animals),
      )
   ) {
      return false;
   }

   return areDraftValuesEqual(
      sortStringsForComparison(leftSave.attractions),
      sortStringsForComparison(rightSave.attractions),
   )
   && areDraftValuesEqual(
      sortScheduledItemsForSaveComparison(leftSave.guardiansTalks),
      sortScheduledItemsForSaveComparison(rightSave.guardiansTalks),
   )
   && areDraftValuesEqual(
      sortWildEncountersForSaveComparison(leftSave.wildEncounters),
      sortWildEncountersForSaveComparison(rightSave.wildEncounters),
   );
}

export function areItineraryDraftItemSelectionsEqual(left, right) {
   return areItineraryDraftSaveItemSelectionsEqual(
      toSetItineraryPayload(left),
      toSetItineraryPayload(right),
   );
}

export function areItineraryDraftsSemanticallyEqual(left, right) {
   const leftSave = toSetItineraryPayload(left);
   const rightSave = toSetItineraryPayload(right);

   if (leftSave.date !== rightSave.date) {
      return false;
   }

   return areItineraryDraftSaveItemSelectionsEqual(leftSave, rightSave);
}

function sortScheduledItemsForSaveComparison(items = []) {
   return [...items].sort((left, right) => (
      left.name.localeCompare(right.name)
   ));
}

export function areItineraryDraftsEqual(left, right) {
   return areDraftValuesEqual(
      normalizeItineraryDraft(left),
      normalizeItineraryDraft(right)
   );
}

export function isItineraryEmptyDraft(draft = {}) {
   const normalizedDraft = normalizeItineraryDraft(draft);

   return !normalizedDraft.date
   && !normalizedDraft.arrivalTime
   && !normalizedDraft.departureTime
   && normalizedDraft.events.length === 0
   && ITINERARY_ITEM_KEYS.every((key) => (
      normalizedDraft[key].length === 0
   ));
}

export function hasSavedItineraryContent(draft = {}) {
   return !isItineraryEmptyDraft(normalizeItineraryDraft(draft));
}

export function isItineraryCompletelyUnset(draft = {}) {
   if (!draft || typeof draft !== 'object') {
      return true;
   }

   return isItineraryEmptyDraft(normalizeItineraryDraft(draft));
}
