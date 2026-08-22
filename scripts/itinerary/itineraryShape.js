import {
   buildAnimalIdentityComparisonKey,
   normalizeAnimalForSave,
} from './animalIdentity.js';
import {
   normalizeGuardiansTalkForSave,
   normalizeItineraryNamesForSave,
   normalizeWildEncounterListForSave,
} from './panel/format.js';
import {
   getTransportationName,
   isTransportationAddedAsAttraction,
} from './selectors/transportationSelector/model.js';

export const ITINERARY_ITEM_KEYS = Object.freeze([
   'animals',
   'attractions',
   'guardiansTalks',
   'wildEncounters',
   'transportations',
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
      transportations: [],
      transportationStations: [],
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
      transportations: normalizeItineraryItems(source.transportations),
      transportationStations: normalizeItineraryItems(source.transportationStations),
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
      transportations: cloneItineraryItems(normalizedDraft.transportations),
      transportationStations: cloneItineraryItems(
         normalizedDraft.transportationStations
      ),
      events: cloneItineraryItems(normalizedDraft.events),
   };
}

function normalizeGuardiansTalkListForSave(items) {
   return normalizeItineraryItems(items)
      .map(normalizeGuardiansTalkForSave)
      .filter((talk) => talk.name);
}

function normalizeTransportationNameForSave(item) {
   if (typeof item === 'string') {
      return item.trim();
   }

   if (!item || typeof item !== 'object') {
      return '';
   }

   return typeof item.name === 'string'
      ? item.name.trim()
      : '';
}

function getAttractionDraftName(item) {
   if (typeof item === 'string') {
      return item.trim();
   }

   return typeof item?.name === 'string'
      ? item.name.trim()
      : '';
}

function buildAttractionNameSet(attractions = []) {
   return new Set(
      normalizeItineraryItems(attractions)
         .map(getAttractionDraftName)
         .filter(Boolean)
   );
}

export function hydrateWizardDraftFromSavedItinerary(draft = {}) {
   const normalized = normalizeItineraryDraft(draft);
   const attractionNames = buildAttractionNameSet(normalized.attractions);
   const fromTransportations = normalized.transportations.flatMap((item) => {
      if (!isTransportationAddedAsAttraction(item)) {
         return [];
      }

      const name = getTransportationName(item);

      if (!name || attractionNames.has(name)) {
         return [];
      }

      attractionNames.add(name);

      return [{ name, addedAsAttraction: true }];
   });

   return {
      ...normalized,
      attractions: [...normalized.attractions, ...fromTransportations],
      transportations: normalized.transportations.filter(
         (item) => !isTransportationAddedAsAttraction(item)
      ),
   };
}

function isAttractionAddedAsAttraction(item) {
   return Boolean(item && typeof item === 'object' && item.addedAsAttraction === true);
}

function normalizeTransportationsForSave(draft = {}) {
   const fromAttractions = normalizeItineraryItems(draft.attractions)
      .filter(isAttractionAddedAsAttraction)
      .map((item) => ({
         name: normalizeTransportationNameForSave(item),
         added_as_attraction: true,
      }))
      .filter((item) => item.name);

   const fromTransportations = normalizeItineraryItems(draft.transportations)
      .map((item) => {
         const name = normalizeTransportationNameForSave(item);

         if (!name) {
            return null;
         }

         return {
            name,
            added_as_attraction: (
               isTransportationAddedAsAttraction(item)
               || isAttractionAddedAsAttraction(item)
            ),
         };
      })
      .filter(Boolean);

   const byName = new Map();

   [...fromTransportations, ...fromAttractions].forEach((item) => {
      byName.set(item.name, item);
   });

   return [...byName.values()];
}

function normalizeAttractionsForSave(attractions = []) {
   return normalizeItineraryNamesForSave(
      normalizeItineraryItems(attractions).filter((item) => (
         !isAttractionAddedAsAttraction(item)
      ))
   );
}

export function toSetItineraryPayload(draft = {}) {
   const base = normalizeItineraryDraft(draft);

   return {
      date: base.date,
      arrivalTime: base.arrivalTime,
      departureTime: base.departureTime,
      animals: base.animals.map(normalizeAnimalForSave).filter(Boolean),
      attractions: normalizeAttractionsForSave(base.attractions),
      transportations: normalizeTransportationsForSave(base),
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
      sortTransportationsForSaveComparison(leftSave.transportations),
      sortTransportationsForSaveComparison(rightSave.transportations),
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

function sortTransportationsForSaveComparison(items = []) {
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
   && normalizedDraft.transportations.length === 0
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
