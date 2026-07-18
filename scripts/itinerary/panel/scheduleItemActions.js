import { ensureItineraryVisitDate } from '../ensureItineraryVisitDate.js';
import {
   createScheduleItemSaveFailedResult,
   scheduleItineraryItemWithConfirmation,
} from './scheduleItemConfirmationFlow.js';
import {
   getScheduleItemRowId,
   getScheduleItemRowKind,
   resolveEffectiveScheduleItemSelection,
} from './scheduleItemSearch.js';
import {
   isScheduleItemEventType,
   isScheduleItemSearchEnabled,
} from './scheduleItemTypes.js';
import {
   getAnimalExhibit,
   getAnimalSpecies,
   getAnimalStoredEnclosureName,
} from '../selectors/animalSelector/model.js';
import { getAttractionName } from '../selectors/attractionSelector/model.js';

export function buildAnimalDraftEntry(row) {
   const species = getAnimalSpecies(row);
   const exhibit = getAnimalExhibit(row);
   const enclosureName = getAnimalStoredEnclosureName(row);

   if (!species || !exhibit) {
      return null;
   }

   const entry = { species, exhibit };

   if (enclosureName) {
      entry.enclosure_name = enclosureName;
   }

   return entry;
}

export function buildAttractionDraftEntry(row) {
   const name = getAttractionName(row);

   return name || null;
}

export function buildScheduleItemRequest(
   selection,
   selectedRow,
   eventTypes = [],
   scheduleOptions = {}
) {
   const { startTime = '', durationMinutes = null } = scheduleOptions;

   const timePayload = {
      ...(startTime ? { startTime } : {}),
      ...(durationMinutes != null ? { durationMinutes } : {}),
   };

   if (isScheduleItemEventType(selection, eventTypes)) {
      return {
         itemType: selection,
         key: '',
         ...timePayload,
      };
   }

   if (!isScheduleItemSearchEnabled(selection, eventTypes) || !selectedRow) {
      return null;
   }

   return {
      itemType: getScheduleItemRowKind(selectedRow),
      key: getScheduleItemRowId(selectedRow),
      ...timePayload,
   };
}

export async function scheduleSelectedItineraryItem(
   itinerary,
   selection,
   selectedRow,
   eventTypes = [],
   scheduleOptions = {}
) {
   const effectiveSelection = resolveEffectiveScheduleItemSelection(
      selection,
      selectedRow
   );
   const request = buildScheduleItemRequest(
      effectiveSelection,
      selectedRow,
      eventTypes,
      scheduleOptions
   );

   if (!request) {
      return createScheduleItemSaveFailedResult();
   }

   try {
      await ensureItineraryVisitDate(itinerary);
   }
   catch {
      return createScheduleItemSaveFailedResult();
   }

   return scheduleItineraryItemWithConfirmation(request);
}
