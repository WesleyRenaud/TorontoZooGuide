import {
   isScheduleItemTypeUnset,
   SCHEDULE_ITEM_MODULE_TYPES,
} from './scheduleItemTypes.js';
import { getAnimalId } from '../selectors/animalSelector/model.js';
import { getAttractionId } from '../selectors/attractionSelector/model.js';

function tagAnimalRows(rows = []) {
   return rows.map((row) => ({
      ...row,
      scheduleItemKind: SCHEDULE_ITEM_MODULE_TYPES.animals,
   }));
}

function tagAttractionRows(rows = []) {
   return rows.map((row) => ({
      ...row,
      scheduleItemKind: SCHEDULE_ITEM_MODULE_TYPES.attractions,
   }));
}

export function getScheduleItemRowKind(row) {
   if (row?.scheduleItemKind === SCHEDULE_ITEM_MODULE_TYPES.attractions) {
      return SCHEDULE_ITEM_MODULE_TYPES.attractions;
   }

   return SCHEDULE_ITEM_MODULE_TYPES.animals;
}

export function getScheduleItemRowId(row) {
   if (getScheduleItemRowKind(row) === SCHEDULE_ITEM_MODULE_TYPES.attractions) {
      return getAttractionId(row);
   }

   return getAnimalId(row);
}

export function buildScheduleItemSearchPayload(moduleType, query = '') {
   const normalizedQuery = String(query ?? '').trim();

   if (moduleType === SCHEDULE_ITEM_MODULE_TYPES.animals) {
      return {
         query: normalizedQuery,
         includeAnimals: true,
      };
   }

   if (moduleType === SCHEDULE_ITEM_MODULE_TYPES.attractions) {
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

export function extractScheduleItemSearchRows(moduleType, response = {}) {
   if (moduleType === SCHEDULE_ITEM_MODULE_TYPES.animals) {
      return tagAnimalRows(
         Array.isArray(response.animals) ? response.animals : []
      );
   }

   if (moduleType === SCHEDULE_ITEM_MODULE_TYPES.attractions) {
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
