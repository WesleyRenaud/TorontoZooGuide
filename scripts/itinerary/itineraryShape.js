import { AnimalIdentity } from './animalIdentity.js';
import { ValueNormalizer } from '../api/valueNormalizer.js';
import { Format } from './panel/format.js';
import { TransportationSelectorModel } from './selectors/transportationSelector/transportationSelectorModel.js';

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

function normalizeGuardiansTalkListForSave(items) {
   return ItineraryShape.normalizeItineraryItems(items)
      .map(Format.normalizeGuardiansTalkForSave)
      .filter((talk) => talk.name);
}

function normalizeTransportationNameForSave(item) {
   if (typeof item === 'string') {
      return ValueNormalizer.asTrimmedString(item);
   }

   if (!item || typeof item !== 'object') {
      return '';
   }

   return ValueNormalizer.asTrimmedString(item.name);
}

function getAttractionDraftName(item) {
   if (typeof item === 'string') {
      return ValueNormalizer.asTrimmedString(item);
   }

   return ValueNormalizer.asTrimmedString(item?.name);
}

function buildAttractionNameSet(attractions = []) {
   return new Set(
      ItineraryShape.normalizeItineraryItems(attractions)
         .map(getAttractionDraftName)
         .filter(Boolean)
   );
}

function isAttractionAddedAsAttraction(item) {
   return Boolean(item && typeof item === 'object' && item.addedAsAttraction === true);
}

function normalizeTransportationsForSave(draft = {}) {
   const fromAttractions = ItineraryShape.normalizeItineraryItems(draft.attractions)
      .filter(isAttractionAddedAsAttraction)
      .map((item) => ({
         name: normalizeTransportationNameForSave(item),
         added_as_attraction: true,
      }))
      .filter((item) => item.name);

   const fromTransportations = ItineraryShape.normalizeItineraryItems(draft.transportations)
      .map((item) => {
         const name = normalizeTransportationNameForSave(item);

         if (!name) {
            return null;
         }

         return {
            name,
            added_as_attraction: (
               TransportationSelectorModel.isTransportationAddedAsAttraction(item)
               || isAttractionAddedAsAttraction(item)
            ),
         };
      })
      .filter(Boolean);

   const bySaveKey = new Map();

   [...fromTransportations, ...fromAttractions].forEach((item) => {
      bySaveKey.set(
         `${item.name}::${item.added_as_attraction}`,
         item
      );
   });

   return [...bySaveKey.values()];
}

function normalizeAttractionsForSave(attractions = []) {
   return Format.normalizeItineraryNamesForSave(
      ItineraryShape.normalizeItineraryItems(attractions).filter((item) => (
         !isAttractionAddedAsAttraction(item)
      ))
   );
}

function sortStringsForComparison(values = []) {
   return [...values].map((item) => String(item)).sort((a, b) => a.localeCompare(b));
}

function sortWildEncountersForSaveComparison(items = []) {
   return sortStringsForComparison(items);
}

function sortAnimalsForSaveComparison(animals = []) {
   return [...animals].sort((a, b) => (
      AnimalIdentity.buildAnimalIdentityComparisonKey(a).localeCompare(
         AnimalIdentity.buildAnimalIdentityComparisonKey(b)
      )
   ));
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

function areItineraryDraftSaveItemSelectionsEqual(leftSave, rightSave) {
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

export class ItineraryShape {
   static ITINERARY_ITEM_KEYS = Object.freeze([
      'animals',
      'attractions',
      'guardiansTalks',
      'wildEncounters',
      'transportations',
   ]);

   static normalizeItineraryItems(items) {
      return Array.isArray(items)
         ? items
         : [];
   }

   static createEmptyItineraryDraft() {
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

   static normalizeItineraryDraft(draft = {}) {
      const source = asItineraryDraftSource(draft);

      return {
         date: normalizeItineraryDate(source.date),
         arrivalTime: normalizeItineraryTime(source.arrivalTime),
         departureTime: normalizeItineraryTime(source.departureTime),
         animals: ItineraryShape.normalizeItineraryItems(source.animals),
         attractions: ItineraryShape.normalizeItineraryItems(source.attractions),
         guardiansTalks: ItineraryShape.normalizeItineraryItems(source.guardiansTalks),
         wildEncounters: ItineraryShape.normalizeItineraryItems(source.wildEncounters),
         transportations: ItineraryShape.normalizeItineraryItems(source.transportations),
         transportationStations: ItineraryShape.normalizeItineraryItems(
            source.transportationStations
         ),
         events: ItineraryShape.normalizeItineraryItems(source.events),
      };
   }

   static cloneItineraryDraft(draft = {}) {
      const normalizedDraft = ItineraryShape.normalizeItineraryDraft(draft);

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

   static hydrateWizardDraftFromSavedItinerary(draft = {}) {
      const normalized = ItineraryShape.normalizeItineraryDraft(draft);
      const attractionNames = buildAttractionNameSet(normalized.attractions);
      const fromTransportations = normalized.transportations.flatMap((item) => {
         if (!TransportationSelectorModel.isTransportationAddedAsAttraction(item)) {
            return [];
         }

         const name = TransportationSelectorModel.getTransportationName(item);

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
            (item) => !TransportationSelectorModel.isTransportationAddedAsAttraction(item)
         ),
      };
   }

   static toSetItineraryPayload(draft = {}) {
      const base = ItineraryShape.normalizeItineraryDraft(draft);

      return {
         date: base.date,
         arrivalTime: base.arrivalTime,
         departureTime: base.departureTime,
         animals: base.animals.map(AnimalIdentity.normalizeAnimalForSave).filter(Boolean),
         attractions: normalizeAttractionsForSave(base.attractions),
         transportations: normalizeTransportationsForSave(base),
         guardiansTalks: normalizeGuardiansTalkListForSave(base.guardiansTalks),
         wildEncounters: Format.normalizeWildEncounterListForSave(base.wildEncounters),
      };
   }

   static areItineraryDraftsSemanticallyEqual(left, right) {
      const leftSave = ItineraryShape.toSetItineraryPayload(left);
      const rightSave = ItineraryShape.toSetItineraryPayload(right);

      if (leftSave.date !== rightSave.date) {
         return false;
      }

      return areItineraryDraftSaveItemSelectionsEqual(leftSave, rightSave);
   }

   static areItineraryDraftsEqual(left, right) {
      return areDraftValuesEqual(
         ItineraryShape.normalizeItineraryDraft(left),
         ItineraryShape.normalizeItineraryDraft(right)
      );
   }

   static isItineraryEmptyDraft(draft = {}) {
      const normalizedDraft = ItineraryShape.normalizeItineraryDraft(draft);

      return !normalizedDraft.date
      && !normalizedDraft.arrivalTime
      && !normalizedDraft.departureTime
      && normalizedDraft.events.length === 0
      && normalizedDraft.transportations.length === 0
      && ItineraryShape.ITINERARY_ITEM_KEYS.every((key) => (
         normalizedDraft[key].length === 0
      ));
   }

   static hasSavedItineraryContent(draft = {}) {
      return !ItineraryShape.isItineraryEmptyDraft(
         ItineraryShape.normalizeItineraryDraft(draft)
      );
   }

   static isItineraryCompletelyUnset(draft = {}) {
      if (!draft || typeof draft !== 'object') {
         return true;
      }

      return ItineraryShape.isItineraryEmptyDraft(
         ItineraryShape.normalizeItineraryDraft(draft)
      );
   }
}
