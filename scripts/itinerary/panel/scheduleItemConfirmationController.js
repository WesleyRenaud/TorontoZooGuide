import { ItineraryClient } from '../../api/itineraryClient.js';
import { AttractionOutsideOperatingHoursFragment } from './attractionOutsideOperatingHoursFragment.js';
import { FixedTimeItemLongWaitFragment } from './fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from './guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from './guardiansTalkWithoutAnimalFragment.js';
import { ItineraryBuildWarningsFragment } from './itineraryBuildWarningsFragment.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItineraryService } from '../itineraryService.js';
import { PersistItineraryWarningSuppressor } from '../persistItineraryWarningSuppressor.js';
import { ScheduleItemConfirmationFlowHelper } from './scheduleItemConfirmationFlowHelper.js';
import { ScheduleItemNotOnItineraryFragment } from './scheduleItemNotOnItineraryFragment.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';
import { WildEncounterUnscheduleFragment } from './wildEncounterUnscheduleFragment.js';

export class ScheduleItemConfirmationController {
   static createScheduleItemSaveFailedResult() {
      return {
         errorType: ItineraryErrorType.SAVE_FAILED,
      };

   }

   static async scheduleItineraryItemWithConfirmation(
      request,
      confirmationOptions = {}
   ) {
      const initialResult = await ItineraryClient.scheduleItineraryItemRequest(request, confirmationOptions);

      if (ItineraryErrorTypes.isItinerarySuccess(initialResult.errorType)) {
         ItineraryService.dispatchScheduleItineraryItemResult(initialResult);
         return initialResult;
      }

      if (ItineraryErrorTypes.requiresScheduleItemNotOnItineraryConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
            showConfirmation: ScheduleItemNotOnItineraryFragment.showScheduleItemNotOnItineraryConfirmation,
            initialResult,
            request,
            confirmationOptions,
            buildConfirmedOptions: () => ({
               confirmingScheduleItemNotOnItinerary: true,
            }),
            beforeConfirm: async ({ doNotShowAgain = false } = {}) => {
               if (doNotShowAgain) {
                  await PersistItineraryWarningSuppressor.persistItineraryWarningSuppression(
                     ItineraryErrorType.ITEM_NOT_ON_ITINERARY
                  );
               }
            },
            resolveConfirmErrorAsSaveFailed: true,
         });
      }

      if (ItineraryErrorTypes.requiresAttractionOutsideOperatingHoursConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
            showConfirmation: AttractionOutsideOperatingHoursFragment.showAttractionOutsideOperatingHoursConfirmation,
            initialResult,
            request,
            confirmationOptions,
            buildConfirmedOptions: () => ({
               confirmingAttractionOutsideOperatingHours: true,
            }),
            resolveConfirmErrorAsSaveFailed: true,
         });
      }

      if (ItineraryBuildWarningsFragment.hasMultipleItineraryBuildWarnings(initialResult.issues)) {
         return ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
            showConfirmation: ItineraryBuildWarningsFragment.showItineraryBuildWarningsConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelper.getConfirmationMountEl(),
               issues: initialResult.issues,
            },
            buildConfirmedOptions: () => ItineraryBuildWarningsFragment.buildConfirmedOptionsFromBuildWarnings(
               initialResult.issues
            ),
         });
      }

      if (ItineraryErrorTypes.requiresGuardiansTalkUnscheduleConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
            showConfirmation: GuardiansTalkUnscheduleFragment.showGuardiansTalkUnscheduleConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelper.getConfirmationMountEl(),
               issues: initialResult.issues,
            },
            buildConfirmedOptions: () => ({
               confirmingGuardiansTalkUnschedule: true,
            }),
         });
      }

      if (ItineraryErrorTypes.requiresGuardiansTalkWithoutAnimalConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
            showConfirmation: GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelper.getConfirmationMountEl(),
               issues: initialResult.issues,
            },
            buildConfirmedOptions: () => ({
               confirmingGuardiansTalkWithoutAnimal: true,
            }),
         });
      }

      if (ItineraryErrorTypes.requiresFixedTimeItemLongWaitConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
            showConfirmation: FixedTimeItemLongWaitFragment.showFixedTimeItemLongWaitConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelper.getConfirmationMountEl(),
               issues: initialResult.issues,
            },
            buildConfirmedOptions: () => ({
               confirmingFixedTimeItemLongWait: true,
            }),
         });
      }

      if (ItineraryErrorTypes.requiresWildEncounterUnscheduleConfirmation(initialResult.errorType)) {
         return ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
            showConfirmation: WildEncounterUnscheduleFragment.showWildEncounterUnscheduleConfirmation,
            initialResult,
            request,
            confirmationOptions,
            confirmationProps: {
               mountEl: ScheduleItemConfirmationFlowHelper.getConfirmationMountEl(),
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
