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
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };
}

export function normalizeItineraryDraft(draft = {}) {
   const source = asItineraryDraftSource(draft);

   return {
      date: normalizeItineraryDate(source.date),
      animals: normalizeItineraryItems(source.animals),
      attractions: normalizeItineraryItems(source.attractions),
      guardiansTalks: normalizeItineraryItems(source.guardiansTalks),
      wildEncounters: normalizeItineraryItems(source.wildEncounters),
   };
}

export function cloneItineraryDraft(draft = {}) {
   const normalizedDraft = normalizeItineraryDraft(draft);

   return {
      date: normalizedDraft.date,
      animals: cloneItineraryItems(normalizedDraft.animals),
      attractions: cloneItineraryItems(normalizedDraft.attractions),
      guardiansTalks: cloneItineraryItems(normalizedDraft.guardiansTalks),
      wildEncounters: cloneItineraryItems(normalizedDraft.wildEncounters),
   };
}

export function areItineraryDraftsEqual(left, right) {
   return areDraftValuesEqual(
      normalizeItineraryDraft(left),
      normalizeItineraryDraft(right)
   );
}

export function isItineraryEmptyDraft(draft = {}) {
   const normalizedDraft = normalizeItineraryDraft(draft);

   return ITINERARY_ITEM_KEYS.every((key) => (
      normalizedDraft[key].length === 0
   ));
}
