import { scheduleItineraryItemRequest } from '../../api/itineraryApi.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { showFixedTimeItemLongWaitConfirmation } from './fixedTimeItemLongWaitConfirmation.js';
import { showGuardiansTalkUnscheduleConfirmation } from './guardiansTalkUnscheduleConfirmation.js';
import { showGuardiansTalkWithoutAnimalConfirmation } from './guardiansTalkWithoutAnimalConfirmation.js';
import {
   buildConfirmedOptionsFromBuildWarnings,
   hasMultipleItineraryBuildWarnings,
   showItineraryBuildWarningsConfirmation,
} from './itineraryBuildWarningsConfirmation.js';
import { createItineraryConfirmationCancelledResult } from '../itineraryConfirmationResult.js';
import {
   getItineraryErrorTypes,
   isItinerarySuccess,
   requiresFixedTimeItemLongWaitConfirmation,
   requiresGuardiansTalkUnscheduleConfirmation,
   requiresGuardiansTalkWithoutAnimalConfirmation,
   requiresScheduleItemNotOnItineraryConfirmation,
   requiresWildEncounterUnscheduleConfirmation,
} from '../itineraryErrorTypes.js';
import { dispatchScheduleItineraryItemResult } from '../itineraryService.js';
import { persistItineraryWarningSuppression } from '../persistItineraryWarningSuppression.js';
import { showScheduleItemNotOnItineraryConfirmation } from './scheduleItemNotOnItineraryConfirmation.js';
import { showWildEncounterUnscheduleConfirmation } from './wildEncounterUnscheduleConfirmation.js';

export function createScheduleItemSaveFailedResult() {
   return {
      errorType: getItineraryErrorTypes()?.SAVE_FAILED,
   };
}

function getConfirmationMountEl() {
   return getItineraryPanelMountEl() ?? document.body;
}

function requestScheduleItemConfirmation({
   showConfirmation,
   initialResult,
   request,
   confirmationOptions,
   confirmationProps = {},
   buildConfirmedOptions,
   beforeConfirm = async () => {},
   resolveConfirmErrorAsSaveFailed = false,
}) {
   return new Promise((resolve) => {
      const confirm = async (confirmArgs = {}) => {
         await beforeConfirm(confirmArgs);

         const confirmedResult = await scheduleItineraryItemWithConfirmation(
            request,
            {
               ...confirmationOptions,
               ...buildConfirmedOptions(confirmArgs),
            }
         );

         resolve(confirmedResult);
      };

      showConfirmation({
         ...confirmationProps,
         onConfirm: async (confirmArgs) => {
            if (!resolveConfirmErrorAsSaveFailed) {
               await confirm(confirmArgs);
               return;
            }

            try {
               await confirm(confirmArgs);
            }
            catch (error) {
               resolve(createScheduleItemSaveFailedResult());
            }
         },
         onCancel: () => {
            resolve(createItineraryConfirmationCancelledResult(initialResult));
         },
      });
   });
}

export async function scheduleItineraryItemWithConfirmation(
   request,
   confirmationOptions = {}
) {
   const initialResult = await scheduleItineraryItemRequest(request, confirmationOptions);

   if (isItinerarySuccess(initialResult.errorType)) {
      dispatchScheduleItineraryItemResult(initialResult);
      return initialResult;
   }

   if (requiresScheduleItemNotOnItineraryConfirmation(initialResult.errorType)) {
      return requestScheduleItemConfirmation({
         showConfirmation: showScheduleItemNotOnItineraryConfirmation,
         initialResult,
         request,
         confirmationOptions,
         buildConfirmedOptions: () => ({
            confirmingScheduleItemNotOnItinerary: true,
         }),
         beforeConfirm: async ({ doNotShowAgain = false } = {}) => {
            if (doNotShowAgain) {
               await persistItineraryWarningSuppression(
                  getItineraryErrorTypes()?.ITEM_NOT_ON_ITINERARY
               );
            }
         },
         resolveConfirmErrorAsSaveFailed: true,
      });
   }

   if (hasMultipleItineraryBuildWarnings(initialResult.issues)) {
      return requestScheduleItemConfirmation({
         showConfirmation: showItineraryBuildWarningsConfirmation,
         initialResult,
         request,
         confirmationOptions,
         confirmationProps: {
            mountEl: getConfirmationMountEl(),
            issues: initialResult.issues,
         },
         buildConfirmedOptions: () => buildConfirmedOptionsFromBuildWarnings(
            initialResult.issues
         ),
      });
   }

   if (requiresGuardiansTalkUnscheduleConfirmation(initialResult.errorType)) {
      return requestScheduleItemConfirmation({
         showConfirmation: showGuardiansTalkUnscheduleConfirmation,
         initialResult,
         request,
         confirmationOptions,
         confirmationProps: {
            mountEl: getConfirmationMountEl(),
            issues: initialResult.issues,
         },
         buildConfirmedOptions: () => ({
            confirmingGuardiansTalkUnschedule: true,
         }),
      });
   }

   if (requiresGuardiansTalkWithoutAnimalConfirmation(initialResult.errorType)) {
      return requestScheduleItemConfirmation({
         showConfirmation: showGuardiansTalkWithoutAnimalConfirmation,
         initialResult,
         request,
         confirmationOptions,
         confirmationProps: {
            mountEl: getConfirmationMountEl(),
            issues: initialResult.issues,
         },
         buildConfirmedOptions: () => ({
            confirmingGuardiansTalkWithoutAnimal: true,
         }),
      });
   }

   if (requiresFixedTimeItemLongWaitConfirmation(initialResult.errorType)) {
      return requestScheduleItemConfirmation({
         showConfirmation: showFixedTimeItemLongWaitConfirmation,
         initialResult,
         request,
         confirmationOptions,
         confirmationProps: {
            mountEl: getConfirmationMountEl(),
            issues: initialResult.issues,
         },
         buildConfirmedOptions: () => ({
            confirmingFixedTimeItemLongWait: true,
         }),
      });
   }

   if (requiresWildEncounterUnscheduleConfirmation(initialResult.errorType)) {
      return requestScheduleItemConfirmation({
         showConfirmation: showWildEncounterUnscheduleConfirmation,
         initialResult,
         request,
         confirmationOptions,
         confirmationProps: {
            mountEl: getConfirmationMountEl(),
            issues: initialResult.issues,
         },
         buildConfirmedOptions: () => ({
            confirmingWildEncounterUnschedule: true,
         }),
      });
   }

   return initialResult;
}
