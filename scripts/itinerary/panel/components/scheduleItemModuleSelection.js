import {
   filterScheduleItemRowsToItinerary,
   getScheduleItemRowId,
   getScheduleItemRowKind,
   resolveEffectiveScheduleItemSelection,
} from '../scheduleItemSearch.js';
import {
   isScheduleItemEventType,
   isScheduleItemSearchEnabled,
   isScheduleItemTypeUnset,
} from '../scheduleItemTypes.js';
import { getAnimalSpecies } from '../../selectors/animalSelector/model.js';
import { getAttractionTitle } from '../../selectors/attractionSelector/model.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';

export function canScheduleModuleSelection({
   selection = '',
   selectedRow = null,
   eventTypes = [],
} = {}) {
   const effectiveSelection = resolveEffectiveScheduleItemSelection(selection, selectedRow);

   if (isScheduleItemTypeUnset(effectiveSelection)) {
      return false;
   }

   if (isScheduleItemSearchEnabled(effectiveSelection, eventTypes)) {
      return Boolean(selectedRow);
   }

   return isScheduleItemEventType(effectiveSelection, eventTypes);
}

export function filterVisibleScheduleModuleRows({
   rows = [],
   itinerary = {},
   onlyItineraryItemsEnabled = false,
} = {}) {
   if (!onlyItineraryItemsEnabled) {
      return rows;
   }

   return filterScheduleItemRowsToItinerary(rows, itinerary);
}

export function shouldClearSelectedScheduleRow({
   selectedRowId = '',
   visibleRows = [],
} = {}) {
   if (!selectedRowId) {
      return false;
   }

   return !visibleRows.some((row) => getScheduleItemRowId(row) === selectedRowId);
}

export function resolveScheduleModuleSearchLabel(row) {
   if (getScheduleItemRowKind(row) === ScheduleItemKind.ATTRACTION.itemType) {
      return getAttractionTitle(row) || '';
   }

   return getAnimalSpecies(row) || '';
}

export function resolveScheduleModuleSearchRowRenderer({
   selection = '',
   row,
   renderAnimalRowLeft,
   renderAttractionRowLeft,
}) {
   if (
      selection === ScheduleItemKind.ATTRACTION.itemType
      || getScheduleItemRowKind(row) === ScheduleItemKind.ATTRACTION.itemType
   ) {
      return renderAttractionRowLeft(row);
   }

   return renderAnimalRowLeft(row);
}
