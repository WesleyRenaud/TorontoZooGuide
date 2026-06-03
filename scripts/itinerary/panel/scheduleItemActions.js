import { scheduleItineraryItemRequest } from '../../api/itineraryApi.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { showGuardiansTalkUnscheduleConfirmation } from './guardiansTalkUnscheduleConfirmation.js';
import {
   getItineraryErrorTypes,
   isItinerarySuccess,
   requiresGuardiansTalkUnscheduleConfirmation,
   requiresScheduleItemNotOnItineraryConfirmation,
   requiresWildEncounterUnscheduleConfirmation,
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
import { showWildEncounterUnscheduleConfirmation } from './wildEncounterUnscheduleConfirmation.js';

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

export function buildScheduleItemRequest(
   selection,
   selectedRow,
   eventTypes = [],
   scheduleOptions = {}
) {
   const { startTime = '', durationMinutes = null } = scheduleOptions;

   if (durationMinutes != null && !startTime) {
      return null;
   }

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

async function scheduleItineraryItemWithConfirmation(request, confirmationOptions = {}) {
   const initialResult = await scheduleItineraryItemRequest(request, confirmationOptions);

   if (isItinerarySuccess(initialResult.errorType)) {
      return initialResult;
   }

   if (requiresScheduleItemNotOnItineraryConfirmation(initialResult.errorType)) {
      return new Promise((resolve) => {
         showScheduleItemNotOnItineraryConfirmation({
            onConfirm: async ({ doNotShowAgain = false } = {}) => {
               const confirmedResult = await scheduleItineraryItemWithConfirmation(
                  request,
                  {
                     ...confirmationOptions,
                     confirmingScheduleItemNotOnItinerary: true,
                     suppressScheduleItemNotOnItineraryWarning: doNotShowAgain,
                  }
               );

               resolve(confirmedResult);
            },
            onCancel: () => {
               resolve(initialResult);
            },
         });
      });
   }

   if (requiresGuardiansTalkUnscheduleConfirmation(initialResult.errorType)) {
      return new Promise((resolve) => {
         showGuardiansTalkUnscheduleConfirmation({
            mountEl: getItineraryPanelMountEl() ?? document.body,
            issues: initialResult.issues,
            onConfirm: async () => {
               const confirmedResult = await scheduleItineraryItemWithConfirmation(
                  request,
                  {
                     ...confirmationOptions,
                     confirmingGuardiansTalkUnschedule: true,
                  }
               );

               resolve(confirmedResult);
            },
            onCancel: () => {
               resolve(initialResult);
            },
         });
      });
   }

   if (requiresWildEncounterUnscheduleConfirmation(initialResult.errorType)) {
      return new Promise((resolve) => {
         showWildEncounterUnscheduleConfirmation({
            mountEl: getItineraryPanelMountEl() ?? document.body,
            issues: initialResult.issues,
            onConfirm: async () => {
               const confirmedResult = await scheduleItineraryItemWithConfirmation(
                  request,
                  {
                     ...confirmationOptions,
                     confirmingWildEncounterUnschedule: true,
                  }
               );

               resolve(confirmedResult);
            },
            onCancel: () => {
               resolve(initialResult);
            },
         });
      });
   }

   return initialResult;
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
      return {
         errorType: getItineraryErrorTypes()?.SAVE_FAILED,
      };
   }

   return scheduleItineraryItemWithConfirmation(request);
}
