import {
   normalizeGuardiansTalkForSave,
   normalizeItineraryNamesForSave,
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

function normalizeItineraryItems(items) {
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

function normalizeAnimalForSave(item) {
   if (!item || typeof item !== 'object') {
      return null;
   }

   const species = String(item.species ?? '').trim();
   const exhibit = String(item.exhibit ?? '').trim();

   if (!species || !exhibit) {
      return null;
   }

   return { species, exhibit };
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
      wildEncounters: normalizeItineraryNamesForSave(base.wildEncounters),
   };
}

function sortStringsForComparison(values = []) {
   return [...values].map((item) => String(item)).sort((a, b) => a.localeCompare(b));
}

function sortScheduledItemsForSaveComparison(items = []) {
   return [...items].sort((left, right) => (
      left.name.localeCompare(right.name)
   ));
}

function sortAnimalsForSaveComparison(animals = []) {
   return [...animals].sort((a, b) => {
      const keyA = `${String(a.species).toLowerCase()}||${String(a.exhibit).toLowerCase()}`;
      const keyB = `${String(b.species).toLowerCase()}||${String(b.exhibit).toLowerCase()}`;

      return keyA.localeCompare(keyB);
   });
}

export function areItineraryDraftsSemanticallyEqual(left, right) {
   const leftSave = toSetItineraryPayload(left);
   const rightSave = toSetItineraryPayload(right);

   if (leftSave.date !== rightSave.date) {
      return false;
   }

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
      sortStringsForComparison(leftSave.wildEncounters),
      sortStringsForComparison(rightSave.wildEncounters),
   );
}

export function areItineraryDraftsEqual(left, right) {
   return areDraftValuesEqual(
      normalizeItineraryDraft(left),
      normalizeItineraryDraft(right)
   );
}

export function isItineraryEmptyDraft(draft = {}) {
   const normalizedDraft = normalizeItineraryDraft(draft);

   return !normalizedDraft.arrivalTime
   && !normalizedDraft.departureTime
   && normalizedDraft.events.length === 0
   && ITINERARY_ITEM_KEYS.every((key) => (
      normalizedDraft[key].length === 0
   ));
}
