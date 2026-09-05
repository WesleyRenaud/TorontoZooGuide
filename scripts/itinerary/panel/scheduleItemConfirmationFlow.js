import { ItineraryApi } from '../../api/itineraryApi.js';
import { AttractionOutsideOperatingHoursConfirmation } from './attractionOutsideOperatingHoursConfirmation.js';
import { Popup } from './components/popup.js';
import { FixedTimeItemLongWaitConfirmation } from './fixedTimeItemLongWaitConfirmation.js';
import { GuardiansTalkUnscheduleConfirmation } from './guardiansTalkUnscheduleConfirmation.js';
import { GuardiansTalkWithoutAnimalConfirmation } from './guardiansTalkWithoutAnimalConfirmation.js';
import { ItineraryBuildWarningsConfirmation } from './itineraryBuildWarningsConfirmation.js';
import { ItineraryConfirmationResult } from '../itineraryConfirmationResult.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { dispatchScheduleItineraryItemResult } from '../itineraryService.js';
import { PersistItineraryWarningSuppression } from '../persistItineraryWarningSuppression.js';
import { ScheduleItemNotOnItineraryConfirmation } from './scheduleItemNotOnItineraryConfirmation.js';
import { WildEncounterUnscheduleConfirmation } from './wildEncounterUnscheduleConfirmation.js';

function getConfirmationMountEl() {
   return Popup.getItineraryPanelMountEl() ?? document.body;
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

         const confirmedResult = await ScheduleItemConfirmationFlow.scheduleItineraryItemWithConfirmation(
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
               resolve(ScheduleItemConfirmationFlow.createScheduleItemSaveFailedResult());
            }
         },
         onCancel: () => {
            resolve(ItineraryConfirmationResult.createItineraryConfirmationCancelledResult(initialResult));
         },
      });
   });
}

export class ScheduleItemConfirmationFlow {
   static createScheduleItemSaveFailedResult() {
      return {
         errorType: ItineraryErrorTypes.getItineraryErrorTypes()?.SAVE_FAILED,
      };

   }

   static async scheduleItineraryItemWithConfirmation(
      request,
      confirmationOptions = {}
   ) {
      const initialResult = await ItineraryApi.scheduleItineraryItemRequest(request, confirmationOptions);

      if (ItineraryErrorTypes.isItinerarySuccess(initialResult.errorType)) {
         dispatchScheduleItineraryItemResult(initialResult);
         return initialResult;
      }

      if (ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation(initialResult.errorType)) {
         return requestScheduleItemConfirmation({
            showConfirmation: ScheduleItemNotOnItineraryConfirmation.showScheduleItemNotOnItineraryConfirmation,
            initialResult,
            request,
            confirmationOptions,
            buildConfirmedOptions: () => ({
               confirmingScheduleItemNotOnItinerary: true,
            }),
            beforeConfirm: async ({ doNotShowAgain = false } = {}) => {
               if (doNotShowAgain) {
                  await PersistItineraryWarningSuppression.persistItineraryWarningSuppression(
                     ItineraryErrorTypes.getItineraryErrorTypes()?.ITEM_NOT_ON_ITINERARY
                  );
               }
            },
            resolveConfirmErrorAsSaveFailed: true,
         });
      }

      if (ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation(initialResult.errorType)) {
         return requestScheduleItemConfirmation({
            showConfirmation: AttractionOutsideOperatingHoursConfirmation.showAttractionOutsideOperatingHoursConfirmation,
            initialResult,
            request,
            confirmationOptions,
            buildConfirmedOptions: () => ({
               confirmingAttractionOutsideOperatingHours: true,
            }),
            resolveConfirmErrorAsSaveFailed: true,
         });
      }

      if (ItineraryBuildWarningsConfirmation.hasMultipleItineraryBuildWarnings(initialResult.issues)) {
         return requestScheduleItemConfirmation({
            showConfirmation: ItineraryBuildWarningsConfirmation.showItineraryBuildWarningsConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: getConfirmationMountEl(),
               issues: initialResult.issues,
            },
            buildConfirmedOptions: () => ItineraryBuildWarningsConfirmation.buildConfirmedOptionsFromBuildWarnings(
               initialResult.issues
            ),
         });
      }

      if (ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation(initialResult.errorType)) {
         return requestScheduleItemConfirmation({
            showConfirmation: GuardiansTalkUnscheduleConfirmation.showGuardiansTalkUnscheduleConfirmation,
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

      if (ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation(initialResult.errorType)) {
         return requestScheduleItemConfirmation({
            showConfirmation: GuardiansTalkWithoutAnimalConfirmation.showGuardiansTalkWithoutAnimalConfirmation,
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

      if (ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation(initialResult.errorType)) {
         return requestScheduleItemConfirmation({
            showConfirmation: FixedTimeItemLongWaitConfirmation.showFixedTimeItemLongWaitConfirmation,
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

      if (ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation(initialResult.errorType)) {
         return requestScheduleItemConfirmation({
            showConfirmation: WildEncounterUnscheduleConfirmation.showWildEncounterUnscheduleConfirmation,
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
}
