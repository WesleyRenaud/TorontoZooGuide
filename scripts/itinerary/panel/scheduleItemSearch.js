import { isScheduleItemTypeUnset } from './scheduleItemTypes.js';
import { getAnimalId } from '../selectors/animalSelector/model.js';
import { getAttractionId } from '../selectors/attractionSelector/model.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';

function tagAnimalRows(rows = []) {
   return rows.map((row) => ({
      ...row,
      scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
   }));
}

function tagAttractionRows(rows = []) {
   return rows.map((row) => ({
      ...row,
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
   }));
}

export function getScheduleItemRowKind(row) {
   if (row?.scheduleItemKind === ScheduleItemKind.ATTRACTION.itemType) {
      return ScheduleItemKind.ATTRACTION.itemType;
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

   const scheduleItemKind = itemType === ScheduleItemKind.ATTRACTION.itemType
      ? ScheduleItemKind.ATTRACTION.itemType
      : ScheduleItemKind.ANIMAL.itemType;

   return {
      ...row,
      scheduleItemKind,
   };
}

export function getScheduleItemRowId(row) {
   if (getScheduleItemRowKind(row) === ScheduleItemKind.ATTRACTION.itemType) {
      return getAttractionId(row);
   }

   return getAnimalId(row);
}

export function getItineraryItemKey(itemType, item) {
   const normalizedType = String(itemType).trim().toLowerCase();

   if (normalizedType === ScheduleItemKind.ANIMAL.itemType) {
      return getAnimalId(item);
   }

   if (normalizedType === ScheduleItemKind.ATTRACTION.itemType) {
      return getAttractionId(item);
   }

   if (
      normalizedType === 'guardians_talks'
      || normalizedType === 'wild_encounters'
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

   if (isScheduleItemTypeUnset(moduleType)) {
      return {
         query: normalizedQuery,
         includeAnimals: true,
         includeAttractions: true,
      };
   }

   return { query: normalizedQuery };
}

export function buildItineraryScheduleItemRowIds(itinerary = {}) {
   const animalIds = new Set(
      itinerary.animals.map((animal) => getAnimalId(animal))
   );
   const attractionIds = new Set(
      itinerary.attractions.map((attraction) => getAttractionId(attraction))
   );

   return { animalIds, attractionIds };
}

export function filterScheduleItemRowsToItinerary(rows = [], itinerary = {}) {
   const { animalIds, attractionIds } = buildItineraryScheduleItemRowIds(itinerary);

   return rows.filter((row) => {
      if (getScheduleItemRowKind(row) === ScheduleItemKind.ATTRACTION.itemType) {
         return attractionIds.has(getScheduleItemRowId(row));
      }

      return animalIds.has(getScheduleItemRowId(row));
   });
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

   if (isScheduleItemTypeUnset(moduleType)) {
      return [
         ...tagAnimalRows(
            Array.isArray(response.animals) ? response.animals : []
         ),
         ...tagAttractionRows(
            Array.isArray(response.attractions) ? response.attractions : []
         ),
      ];
   }

   return [];
}
