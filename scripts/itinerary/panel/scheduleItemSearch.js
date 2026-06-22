import { normalizeItineraryItems } from '../itineraryShape.js';
import { isScheduleItemTypeUnset } from './scheduleItemTypes.js';
import { getAnimalId } from '../selectors/animalSelector/model.js';
import { getAttractionId } from '../selectors/attractionSelector/model.js';
import { getGuardiansTalkId } from '../selectors/guardiansTalkSelector/model.js';
import { getWildEncounterId } from '../selectors/wildEncounterSelector/model.js';
import {
   isFixedTimeScheduleItemKind,
   ScheduleItemKind,
   scheduleItemKindFromItemType,
} from '../../shared/enums/scheduleItemKind.js';

function tagRows(rows = [], scheduleItemKind) {
   return rows.map((row) => ({
      ...row,
      scheduleItemKind,
   }));
}

function tagAnimalRows(rows = []) {
   return tagRows(rows, ScheduleItemKind.ANIMAL.itemType);
}

function tagAttractionRows(rows = []) {
   return tagRows(rows, ScheduleItemKind.ATTRACTION.itemType);
}

function tagGuardiansTalkRows(rows = []) {
   return tagRows(rows, ScheduleItemKind.GUARDIANS_TALK.itemType);
}

function tagWildEncounterRows(rows = []) {
   return tagRows(rows, ScheduleItemKind.WILD_ENCOUNTER.itemType);
}

export function isUnscheduledItineraryItem(item) {
   return !String(item?.start_time ?? '').trim();
}

export function getScheduleItemRowKind(row) {
   const scheduleItemKind = row?.scheduleItemKind;

   if (scheduleItemKind === ScheduleItemKind.ATTRACTION.itemType) {
      return ScheduleItemKind.ATTRACTION.itemType;
   }

   if (scheduleItemKind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return ScheduleItemKind.GUARDIANS_TALK.itemType;
   }

   if (scheduleItemKind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return ScheduleItemKind.WILD_ENCOUNTER.itemType;
   }

   return ScheduleItemKind.ANIMAL.itemType;
}

export function resolveEffectiveScheduleItemSelection(selection, selectedRow) {
   if (!isScheduleItemTypeUnset(selection)) {
      return selection;
   }

   if (selectedRow) {
      return getScheduleItemRowKind(selectedRow);
   }

   return selection;
}

export function tagScheduleItemRow(itemType, row) {
   if (!row || typeof row !== 'object') {
      return null;
   }

   if (itemType === ScheduleItemKind.ATTRACTION.itemType) {
      return tagAttractionRows([row])[0];
   }

   if (itemType === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return tagGuardiansTalkRows([row])[0];
   }

   if (itemType === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return tagWildEncounterRows([row])[0];
   }

   return tagAnimalRows([row])[0];
}

export function getScheduleItemRowId(row) {
   const kind = getScheduleItemRowKind(row);

   if (kind === ScheduleItemKind.ATTRACTION.itemType) {
      return getAttractionId(row);
   }

   if (kind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return getGuardiansTalkId(row);
   }

   if (kind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return getWildEncounterId(row);
   }

   return getAnimalId(row);
}

export function getItineraryItemKey(itemType, item) {
   const kind = scheduleItemKindFromItemType(itemType);

   if (kind === ScheduleItemKind.ANIMAL) {
      return getAnimalId(item);
   }

   if (kind === ScheduleItemKind.ATTRACTION) {
      return getAttractionId(item);
   }

   if (
      kind === ScheduleItemKind.GUARDIANS_TALK
      || kind === ScheduleItemKind.WILD_ENCOUNTER
   ) {
      return String(item.name).trim();
   }

   return '';
}

export function buildScheduleItemSearchPayload(moduleType, query = '') {
   const normalizedQuery = String(query ?? '').trim();

   if (moduleType === ScheduleItemKind.ANIMAL.itemType) {
      return {
         query: normalizedQuery,
         includeAnimals: true,
      };
   }

   if (moduleType === ScheduleItemKind.ATTRACTION.itemType) {
      return {
         query: normalizedQuery,
         includeAttractions: true,
      };
   }

   if (moduleType === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return {
         query: normalizedQuery,
         includeGuardiansTalks: true,
      };
   }

   if (moduleType === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return {
         query: normalizedQuery,
         includeWildEncounters: true,
      };
   }

   if (isScheduleItemTypeUnset(moduleType)) {
      return {
         query: normalizedQuery,
         includeAnimals: true,
         includeAttractions: true,
         includeGuardiansTalks: true,
         includeWildEncounters: true,
      };
   }

   return { query: normalizedQuery };
}

export function buildItineraryScheduleItemRowIds(
      itinerary = {},
      { unscheduledOnly = false, scheduledOnly = false } = {}) {
   const pickItems = (items) => {
      const list = normalizeItineraryItems(items);

      if (scheduledOnly) {
         return list.filter((item) => !isUnscheduledItineraryItem(item));
      }

      return unscheduledOnly
         ? list.filter(isUnscheduledItineraryItem)
         : list;
   };

   return {
      animalIds: new Set(
         pickItems(itinerary.animals).map((animal) => getAnimalId(animal))
      ),
      attractionIds: new Set(
         pickItems(itinerary.attractions).map((attraction) => getAttractionId(attraction))
      ),
      guardiansTalkIds: new Set(
         pickItems(itinerary.guardiansTalks).map((talk) => getGuardiansTalkId(talk))
      ),
      wildEncounterIds: new Set(
         pickItems(itinerary.wildEncounters).map((encounter) => getWildEncounterId(encounter))
      ),
   };
}

export function filterScheduleItemRowsToItinerary(
      rows = [],
      itinerary = {},
      { unscheduledOnly = false } = {}) {
   const {
      animalIds,
      attractionIds,
      guardiansTalkIds,
      wildEncounterIds,
   } = buildItineraryScheduleItemRowIds(itinerary, { unscheduledOnly });

   return rows.filter((row) => {
      const kind = getScheduleItemRowKind(row);

      if (kind === ScheduleItemKind.ATTRACTION.itemType) {
         return attractionIds.has(getScheduleItemRowId(row));
      }

      if (kind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
         return guardiansTalkIds.has(getScheduleItemRowId(row));
      }

      if (kind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
         return wildEncounterIds.has(getScheduleItemRowId(row));
      }

      return animalIds.has(getScheduleItemRowId(row));
   });
}

export function filterScheduleItemRowsExcludingScheduledOccurrences(
      rows = [],
      itinerary = {}) {
   const {
      guardiansTalkIds,
      wildEncounterIds,
   } = buildItineraryScheduleItemRowIds(itinerary, { scheduledOnly: true });

   return rows.filter((row) => {
      const kind = getScheduleItemRowKind(row);

      if (kind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
         return !guardiansTalkIds.has(getScheduleItemRowId(row));
      }

      if (kind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
         return !wildEncounterIds.has(getScheduleItemRowId(row));
      }

      return true;
   });
}

export function filterScheduleItemRowsForScheduleModule(
      rows = [],
      itinerary = {},
      { onlyItineraryItemsEnabled = false } = {}) {
   const rowsWithoutScheduledOccurrences = filterScheduleItemRowsExcludingScheduledOccurrences(
      rows,
      itinerary
   );

   if (!onlyItineraryItemsEnabled) {
      return rowsWithoutScheduledOccurrences;
   }

   return filterScheduleItemRowsToItinerary(
      rowsWithoutScheduledOccurrences,
      itinerary,
      { unscheduledOnly: true }
   ).filter((row) => !isFixedTimeScheduleItemKind(getScheduleItemRowKind(row)));
}

export function extractScheduleItemSearchRows(moduleType, response = {}) {
   if (moduleType === ScheduleItemKind.ANIMAL.itemType) {
      return tagAnimalRows(
         Array.isArray(response.animals) ? response.animals : []
      );
   }

   if (moduleType === ScheduleItemKind.ATTRACTION.itemType) {
      return tagAttractionRows(
         Array.isArray(response.attractions) ? response.attractions : []
      );
   }

   if (moduleType === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return tagGuardiansTalkRows(
         Array.isArray(response.guardians_talks) ? response.guardians_talks : []
      );
   }

   if (moduleType === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return tagWildEncounterRows(
         Array.isArray(response.wild_encounters) ? response.wild_encounters : []
      );
   }

   if (isScheduleItemTypeUnset(moduleType)) {
      return [
         ...tagAnimalRows(
            Array.isArray(response.animals) ? response.animals : []
         ),
         ...tagAttractionRows(
            Array.isArray(response.attractions) ? response.attractions : []
         ),
         ...tagGuardiansTalkRows(
            Array.isArray(response.guardians_talks) ? response.guardians_talks : []
         ),
         ...tagWildEncounterRows(
            Array.isArray(response.wild_encounters) ? response.wild_encounters : []
         ),
      ];
   }

   return [];
}
