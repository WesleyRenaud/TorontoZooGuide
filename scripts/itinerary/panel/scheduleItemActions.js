import { EnsureItineraryVisitDate } from '../ensureItineraryVisitDate.js';
import { ItineraryEventTypes } from '../itineraryEventTypes.js';
import { ScheduleItemConfirmationFlow } from './scheduleItemConfirmationFlow.js';
import { ScheduleItemSearch } from './scheduleItemSearch.js';
import { ScheduleItemTypes } from './scheduleItemTypes.js';
import { AnimalSelectorModel } from '../selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../selectors/attractionSelector/attractionSelectorModel.js';

export function buildAnimalDraftEntry(row) {
   const species = AnimalSelectorModel.getAnimalSpecies(row);
   const exhibit = AnimalSelectorModel.getAnimalExhibit(row);
   const enclosureName = AnimalSelectorModel.getAnimalStoredEnclosureName(row);

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
   const name = AttractionSelectorModel.getAttractionName(row);

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

   if (ItineraryEventTypes.isScheduleItemEventType(selection, eventTypes)) {
      return {
         itemType: selection,
         key: '',
         ...timePayload,
      };
   }

   if (!ScheduleItemTypes.isScheduleItemSearchEnabled(selection, eventTypes) || !selectedRow) {
      return null;
   }

   return {
      itemType: ScheduleItemSearch.getScheduleItemRowKind(selectedRow),
      key: ScheduleItemSearch.getScheduleItemRowId(selectedRow),
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
   const effectiveSelection = ScheduleItemSearch.resolveEffectiveScheduleItemSelection(
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
      return ScheduleItemConfirmationFlow.createScheduleItemSaveFailedResult();
   }

   try {
      await EnsureItineraryVisitDate.ensureItineraryVisitDate(itinerary);
   }
   catch {
      return ScheduleItemConfirmationFlow.createScheduleItemSaveFailedResult();
   }

   return ScheduleItemConfirmationFlow.scheduleItineraryItemWithConfirmation(request);
}
