import { scheduleItineraryItemRequest } from '../../api/itineraryApi.js';
import {
   getItineraryErrorTypes,
   isItinerarySuccess,
   requiresScheduleItemNotOnItineraryConfirmation,
} from '../itineraryErrorTypes.js';
import { showScheduleItemNotOnItineraryConfirmation } from './scheduleItemNotOnItineraryConfirmation.js';
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
} from '../selectors/animalSelector/model.js';
import { getAttractionName } from '../selectors/attractionSelector/model.js';

export function buildAnimalDraftEntry(row) {
   const species = getAnimalSpecies(row);
   const exhibit = getAnimalExhibit(row);

   if (!species || !exhibit) {
      return null;
   }

   return { species, exhibit };
}

export function buildAttractionDraftEntry(row) {
   const name = getAttractionName(row);

   return name || null;
}

export function buildScheduleItemRequest(selection, selectedRow, eventTypes = []) {
   if (isScheduleItemEventType(selection, eventTypes)) {
      return {
         itemType: selection,
         key: '',
      };
   }

   if (!isScheduleItemSearchEnabled(selection, eventTypes) || !selectedRow) {
      return null;
   }

   return {
      itemType: getScheduleItemRowKind(selectedRow),
      key: getScheduleItemRowId(selectedRow),
   };
}

async function scheduleItineraryItemWithConfirmation(request) {
   const initialResult = await scheduleItineraryItemRequest(request);

   if (
      isItinerarySuccess(initialResult.errorType)
      || !requiresScheduleItemNotOnItineraryConfirmation(initialResult.errorType)
   ) {
      return initialResult;
   }

   return new Promise((resolve) => {
      showScheduleItemNotOnItineraryConfirmation({
         onConfirm: async ({ doNotShowAgain = false } = {}) => {
            const confirmedResult = await scheduleItineraryItemRequest(request, {
               confirmingScheduleItemNotOnItinerary: true,
               suppressScheduleItemNotOnItineraryWarning: doNotShowAgain,
            });

            resolve(confirmedResult);
         },
         onCancel: () => {
            resolve(initialResult);
         },
      });
   });
}

export async function scheduleSelectedItineraryItem(
   itinerary,
   selection,
   selectedRow,
   eventTypes = []
) {
   const effectiveSelection = resolveEffectiveScheduleItemSelection(
      selection,
      selectedRow
   );
   const request = buildScheduleItemRequest(
      effectiveSelection,
      selectedRow,
      eventTypes
   );

   if (!request) {
      return {
         errorType: getItineraryErrorTypes()?.SAVE_FAILED,
      };
   }

   return scheduleItineraryItemWithConfirmation(request);
}
