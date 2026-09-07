import { ItineraryApi } from '../../api/itineraryApi.js';
import { AttractionOutsideOperatingHoursConfirmation } from './attractionOutsideOperatingHoursConfirmation.js';
import { FixedTimeItemLongWaitConfirmation } from './fixedTimeItemLongWaitConfirmation.js';
import { GuardiansTalkUnscheduleConfirmation } from './guardiansTalkUnscheduleConfirmation.js';
import { GuardiansTalkWithoutAnimalConfirmation } from './guardiansTalkWithoutAnimalConfirmation.js';
import { ItineraryBuildWarningsConfirmation } from './itineraryBuildWarningsConfirmation.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItineraryService } from '../itineraryService.js';
import { PersistItineraryWarningSuppression } from '../persistItineraryWarningSuppression.js';
import { ScheduleItemConfirmationFlowHelpers } from './scheduleItemConfirmationFlowHelpers.js';
import { ScheduleItemNotOnItineraryConfirmation } from './scheduleItemNotOnItineraryConfirmation.js';
import { WildEncounterUnscheduleConfirmation } from './wildEncounterUnscheduleConfirmation.js';

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
         ItineraryService.dispatchScheduleItineraryItemResult(initialResult);
         return initialResult;
      }

      if (ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelpers.requestScheduleItemConfirmation({
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
         return ScheduleItemConfirmationFlowHelpers.requestScheduleItemConfirmation({
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
         return ScheduleItemConfirmationFlowHelpers.requestScheduleItemConfirmation({
            showConfirmation: ItineraryBuildWarningsConfirmation.showItineraryBuildWarningsConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelpers.getConfirmationMountEl(),
               issues: initialResult.issues,
            },
            buildConfirmedOptions: () => ItineraryBuildWarningsConfirmation.buildConfirmedOptionsFromBuildWarnings(
               initialResult.issues
            ),
         });
      }

      if (ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelpers.requestScheduleItemConfirmation({
            showConfirmation: GuardiansTalkUnscheduleConfirmation.showGuardiansTalkUnscheduleConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelpers.getConfirmationMountEl(),
               issues: initialResult.issues,
            },
            buildConfirmedOptions: () => ({
               confirmingGuardiansTalkUnschedule: true,
            }),
         });
      }

      if (ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelpers.requestScheduleItemConfirmation({
            showConfirmation: GuardiansTalkWithoutAnimalConfirmation.showGuardiansTalkWithoutAnimalConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelpers.getConfirmationMountEl(),
               issues: initialResult.issues,
            },
            buildConfirmedOptions: () => ({
               confirmingGuardiansTalkWithoutAnimal: true,
            }),
         });
      }

      if (ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelpers.requestScheduleItemConfirmation({
            showConfirmation: FixedTimeItemLongWaitConfirmation.showFixedTimeItemLongWaitConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelpers.getConfirmationMountEl(),
               issues: initialResult.issues,
            },
            buildConfirmedOptions: () => ({
               confirmingFixedTimeItemLongWait: true,
            }),
         });
      }

      if (ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelpers.requestScheduleItemConfirmation({
            showConfirmation: WildEncounterUnscheduleConfirmation.showWildEncounterUnscheduleConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelpers.getConfirmationMountEl(),
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
