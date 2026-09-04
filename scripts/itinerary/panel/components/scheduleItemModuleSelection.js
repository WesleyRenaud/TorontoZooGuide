import { ItineraryEventTypes } from '../../itineraryEventTypes.js';
import {
   filterScheduleItemRowsForScheduleModule,
   getScheduleItemRowId,
   getScheduleItemRowKind,
   resolveEffectiveScheduleItemSelection,
} from '../scheduleItemSearch.js';
import {
   isScheduleItemSearchEnabled,
   isScheduleItemTypeUnset,
} from '../scheduleItemTypes.js';
import { getAnimalTitleLine } from '../../selectors/animalSelector/model.js';
import { getAttractionTitle } from '../../selectors/attractionSelector/model.js';
import { getGuardiansTalkName } from '../../selectors/guardiansTalkSelector/model.js';
import { getTransportationName } from '../../selectors/transportationSelector/model.js';
import { getWildEncounterName } from '../../selectors/wildEncounterSelector/model.js';
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

   return ItineraryEventTypes.isScheduleItemEventType(effectiveSelection, eventTypes);
}

export function filterVisibleScheduleModuleRows({
   rows = [],
   itinerary = {},
   onlyItineraryItemsEnabled = false,
} = {}) {
   return filterScheduleItemRowsForScheduleModule(rows, itinerary, {
      onlyItineraryItemsEnabled,
   });
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
   const kind = getScheduleItemRowKind(row);

   if (kind === ScheduleItemKind.ATTRACTION.itemType) {
      return getAttractionTitle(row) || '';
   }

   if (kind === ScheduleItemKind.TRANSPORTATION.itemType) {
      return getTransportationName(row) || '';
   }

   if (kind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return getGuardiansTalkName(row) || '';
   }

   if (kind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return getWildEncounterName(row) || '';
   }

   return getAnimalTitleLine(row);
}

export function resolveScheduleModuleSearchRowRenderer({
   row,
   renderAnimalRowLeft,
   renderAttractionRowLeft,
   renderTransportationRowLeft,
   renderGuardiansTalkRowLeft,
   renderWildEncounterRowLeft,
}) {
   const kind = getScheduleItemRowKind(row);

   if (kind === ScheduleItemKind.ATTRACTION.itemType) {
      return renderAttractionRowLeft(row);
   }

   if (kind === ScheduleItemKind.TRANSPORTATION.itemType) {
      return renderTransportationRowLeft(row);
   }

   if (kind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return renderGuardiansTalkRowLeft(row);
   }

   if (kind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return renderWildEncounterRowLeft(row);
   }

   return renderAnimalRowLeft(row);
}
