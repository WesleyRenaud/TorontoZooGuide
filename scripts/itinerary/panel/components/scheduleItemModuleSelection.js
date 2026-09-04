import { ItineraryEventTypes } from '../../itineraryEventTypes.js';
import {
   filterScheduleItemRowsForScheduleModule,
   getScheduleItemRowId,
   getScheduleItemRowKind,
   resolveEffectiveScheduleItemSelection,
} from '../scheduleItemSearch.js';
import { ScheduleItemTypes } from '../scheduleItemTypes.js';
import { AnimalSelectorModel } from '../../selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../../selectors/attractionSelector/attractionSelectorModel.js';
import { GuardiansTalkSelectorModel } from '../../selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { TransportationSelectorModel } from '../../selectors/transportationSelector/transportationSelectorModel.js';
import { WildEncounterSelectorModel } from '../../selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { ScheduleItemKind } from '../../../shared/enums/scheduleItemKind.js';

export function canScheduleModuleSelection({
   selection = '',
   selectedRow = null,
   eventTypes = [],
} = {}) {
   const effectiveSelection = resolveEffectiveScheduleItemSelection(selection, selectedRow);

   if (ScheduleItemTypes.isScheduleItemTypeUnset(effectiveSelection)) {
      return false;
   }

   if (ScheduleItemTypes.isScheduleItemSearchEnabled(effectiveSelection, eventTypes)) {
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
      return AttractionSelectorModel.getAttractionTitle(row) || '';
   }

   if (kind === ScheduleItemKind.TRANSPORTATION.itemType) {
      return TransportationSelectorModel.getTransportationName(row) || '';
   }

   if (kind === ScheduleItemKind.GUARDIANS_TALK.itemType) {
      return GuardiansTalkSelectorModel.getGuardiansTalkName(row) || '';
   }

   if (kind === ScheduleItemKind.WILD_ENCOUNTER.itemType) {
      return WildEncounterSelectorModel.getWildEncounterName(row) || '';
   }

   return AnimalSelectorModel.getAnimalTitleLine(row);
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
