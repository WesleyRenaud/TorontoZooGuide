import { ItineraryEventTypes } from '../itineraryEventTypes.js';
import { ItineraryVisitDateResolver } from '../itineraryVisitDateResolver.js';
import { ScheduleItemConfirmationController } from './scheduleItemConfirmationController.js';
import { ScheduleItemSearcher } from './scheduleItemSearcher.js';
import { ScheduleItemTypes } from './scheduleItemTypes.js';
import { AnimalSelectorModel } from '../selectors/animalSelector/animalSelectorModel.js';
import { AttractionSelectorModel } from '../selectors/attractionSelector/attractionSelectorModel.js';

export class ScheduleItemController {
   static buildAnimalDraftEntry(row) {
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

   static buildAttractionDraftEntry(row) {
      const name = AttractionSelectorModel.getAttractionName(row);

      return name || null;
   }

   static buildScheduleItemRequest(
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
         itemType: ScheduleItemSearcher.getScheduleItemRowKind(selectedRow),
         key: ScheduleItemSearcher.getScheduleItemRowId(selectedRow),
         ...timePayload,
      };
   }

   static async scheduleSelectedItineraryItem(
   itinerary,
   selection,
   selectedRow,
   eventTypes = [],
   scheduleOptions = {}
) {
      const effectiveSelection = ScheduleItemSearcher.resolveEffectiveScheduleItemSelection(
         selection,
         selectedRow
      );
      const request = ScheduleItemController.buildScheduleItemRequest(
         effectiveSelection,
         selectedRow,
         eventTypes,
         scheduleOptions
      );

      if (!request) {
         return ScheduleItemConfirmationController.createScheduleItemSaveFailedResult();
      }

      try {
         await ItineraryVisitDateResolver.ensureItineraryVisitDate(itinerary);
      }
      catch {
         return ScheduleItemConfirmationController.createScheduleItemSaveFailedResult();
      }

      return ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation(request);
   }
}
