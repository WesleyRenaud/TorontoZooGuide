import { normalizeItineraryItems } from '../itineraryShape.js';
import { ScheduleItemTypes } from './scheduleItemTypes.js';
import { AnimalSelectorModel } from '../selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../selectors/attractionSelector/attractionSelectorModel.js';
import { GuardiansTalkSelectorModel } from '../selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { WildEncounterScheduleItemKey } from '../selectors/wildEncounterSelector/scheduleItemKey.js';
import { WildEncounterSelectorModel } from '../selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';

function itineraryWildEncounterId(encounter) {
   return WildEncounterScheduleItemKey.fromRow(encounter)?.toWire() ?? null;
}

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

function tagTransportationRows(rows = []) {
   return tagRows(rows, ScheduleItemKind.TRANSPORTATION.itemType);
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

   if (scheduleItemKind === ScheduleItemKind.TRANSPORTATION.itemType) {
      return ScheduleItemKind.TRANSPORTATION.itemType;
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
   if (!ScheduleItemTypes.isScheduleItemTypeUnset(selection)) {
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

   if (itemType === ScheduleItemKind.TRANSPORTATION.itemType) {
      if (TransportationSelectorModel.isTransportationAddedAsAttraction(row)) {
         return tagAttractionRows([row])[0];
      }

      return tagTransportationRows([row])[0];
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
      return AttractionSelectorModel.getAttractionId(row);
   }

   if (kind === ScheduleItemKind.TRANSPORTATION.itemType) {
      return TransportationSelectorModel.getTransportationScheduleItemKey(row);
   }

   if (kind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return GuardiansTalkSelectorModel.getGuardiansTalkId(row);
   }

   if (kind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return WildEncounterSelectorModel.getWildEncounterId(row);
   }

   return AnimalSelectorModel.getAnimalId(row);
}

export function getItineraryItemKey(itemType, item) {
   const kind = ScheduleItemKind.scheduleItemKindFromItemType(itemType);

   if (kind === ScheduleItemKind.ANIMAL) {
      return AnimalSelectorModel.getAnimalId(item);
   }

   if (kind === ScheduleItemKind.ATTRACTION) {
      return AttractionSelectorModel.getAttractionId(item);
   }

   if (kind === ScheduleItemKind.TRANSPORTATION) {
      return TransportationSelectorModel.getTransportationScheduleItemKey(item);
   }

   if (kind === ScheduleItemKind.GUARDIANS_TALK) {
      return GuardiansTalkSelectorModel.getGuardiansTalkId(item);
   }

   if (kind === ScheduleItemKind.WILD_ENCOUNTER) {
      return WildEncounterSelectorModel.getWildEncounterKey(item);
   }

   return '';
}

export function buildScheduleItemSearchPayload(moduleType, query = '') {
   const normalizedQuery = String(query ?? '').trim();

   if (moduleType === ScheduleItemKind.ANIMAL.itemType) {
      return {
         query: normalizedQuery,
         includeAnimals: true,
         forItinerary: true,
      };
   }

   if (moduleType === ScheduleItemKind.ATTRACTION.itemType) {
      return {
         query: normalizedQuery,
         includeAttractions: true,
      };
   }

   if (moduleType === ScheduleItemKind.TRANSPORTATION.itemType) {
      return {
         query: normalizedQuery,
         includeTransportations: true,
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

   if (ScheduleItemTypes.isScheduleItemTypeUnset(moduleType)) {
      return {
         query: normalizedQuery,
         includeAnimals: true,
         includeAttractions: true,
         includeGuardiansTalks: true,
         includeWildEncounters: true,
         forItinerary: true,
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

   const transportationItems = pickItems(itinerary.transportations);
   const attractionIds = new Set(
      pickItems(itinerary.attractions).map((attraction) => AttractionSelectorModel.getAttractionId(attraction))
   );

   transportationItems
      .filter(TransportationSelectorModel.isTransportationAddedAsAttraction)
      .forEach((transportation) => {
         attractionIds.add(TransportationSelectorModel.getTransportationId(transportation));
      });

   return {
      animalIds: new Set(
         pickItems(itinerary.animals).map((animal) => AnimalSelectorModel.getAnimalId(animal))
      ),
      attractionIds,
      transportationIds: new Set(
         transportationItems
            .filter((transportation) => !TransportationSelectorModel.isTransportationAddedAsAttraction(transportation))
            .map((transportation) => TransportationSelectorModel.getTransportationScheduleItemKey(transportation))
      ),
      guardiansTalkIds: new Set(
         pickItems(itinerary.guardiansTalks).map((talk) => GuardiansTalkSelectorModel.getGuardiansTalkId(talk))
      ),
      wildEncounterIds: new Set(
         pickItems(itinerary.wildEncounters)
            .map(itineraryWildEncounterId)
            .filter(Boolean)
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
      transportationIds,
      guardiansTalkIds,
      wildEncounterIds,
   } = buildItineraryScheduleItemRowIds(itinerary, { unscheduledOnly });

   return rows.filter((row) => {
      const kind = getScheduleItemRowKind(row);

      if (kind === ScheduleItemKind.ATTRACTION.itemType) {
         return attractionIds.has(getScheduleItemRowId(row));
      }

      if (kind === ScheduleItemKind.TRANSPORTATION.itemType) {
         return transportationIds.has(getScheduleItemRowId(row));
      }

      if (kind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
         return guardiansTalkIds.has(getScheduleItemRowId(row));
      }

      if (kind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
         return wildEncounterIds.has(WildEncounterSelectorModel.getWildEncounterId(row));
      }

      return animalIds.has(getScheduleItemRowId(row));
   });
}

export function filterScheduleItemRowsExcludingScheduledOccurrences(
      rows = [],
      itinerary = {}) {
   const {
      animalIds,
      attractionIds,
      transportationIds,
      guardiansTalkIds,
      wildEncounterIds,
   } = buildItineraryScheduleItemRowIds(itinerary, { scheduledOnly: true });

   return rows.filter((row) => {
      const kind = getScheduleItemRowKind(row);

      if (kind === ScheduleItemKind.ATTRACTION.itemType) {
         return !attractionIds.has(getScheduleItemRowId(row));
      }

      if (kind === ScheduleItemKind.TRANSPORTATION.itemType) {
         return !transportationIds.has(getScheduleItemRowId(row));
      }

      if (kind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
         return !guardiansTalkIds.has(getScheduleItemRowId(row));
      }

      if (kind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
         return !wildEncounterIds.has(WildEncounterSelectorModel.getWildEncounterId(row));
      }

      if (kind === ScheduleItemKind.ANIMAL.itemType) {
         return !animalIds.has(getScheduleItemRowId(row));
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
   ).filter((row) => !ScheduleItemKind.isFixedTimeScheduleItemKind(getScheduleItemRowKind(row)));
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

   if (moduleType === ScheduleItemKind.TRANSPORTATION.itemType) {
      return tagTransportationRows(
         Array.isArray(response.transportations) ? response.transportations : []
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

   if (ScheduleItemTypes.isScheduleItemTypeUnset(moduleType)) {
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
