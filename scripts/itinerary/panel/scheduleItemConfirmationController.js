import { ItineraryClient } from '../../api/itineraryClient.js';
import { ItineraryBuildWarningsFragment } from './itineraryBuildWarningsFragment.js';
import { ItineraryConfirmationRegistry } from '../itineraryConfirmationRegistry.js';
import { ItineraryErrorTypes } from '../itineraryErrorTypes.js';
import { ItineraryService } from '../itineraryService.js';
import { ScheduleItemConfirmationFlowHelper } from './scheduleItemConfirmationFlowHelper.js';
import { ItineraryErrorType } from '../../shared/enums/itineraryErrorType.js';

export class ScheduleItemConfirmationController {
   static createScheduleItemSaveFailedResult() {
      return {
         errorType: ItineraryErrorType.SAVE_FAILED,
      };

   }

   static requestScheduleItemConfirmationFromEntry(
      entry,
      initialResult,
      request,
      confirmationOptions
   ) {
      return ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
         showConfirmation: entry.showConfirmation,
         initialResult,
         request,
         confirmationOptions,
         confirmationProps: entry.confirmationPropsWithIssues
            ? {
               mountEl: ScheduleItemConfirmationFlowHelper.getConfirmationMountEl(),
               issues: initialResult.issues,
            }
            : {},
         buildConfirmedOptions: ItineraryConfirmationRegistry.buildConfirmedOptions(entry),
         beforeConfirm: ItineraryConfirmationRegistry.buildBeforeConfirm(entry),
         resolveConfirmErrorAsSaveFailed: Boolean(entry.resolveConfirmErrorAsSaveFailed),
      });
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

      for (
         const entry of ItineraryConfirmationRegistry.getScheduleItemConfirmationEntriesBeforeWarnings()
      ) {
         if (ItineraryErrorTypes[entry.requiresMethod](initialResult.errorType)) {
            return ScheduleItemConfirmationController.requestScheduleItemConfirmationFromEntry(
               entry,
               initialResult,
               request,
               confirmationOptions
            );
         }
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

      for (
         const entry of ItineraryConfirmationRegistry.getScheduleItemConfirmationEntriesAfterWarnings()
      ) {
         if (ItineraryErrorTypes[entry.requiresMethod](initialResult.errorType)) {
            return ScheduleItemConfirmationController.requestScheduleItemConfirmationFromEntry(
               entry,
               initialResult,
               request,
               confirmationOptions
            );
         }
      }

      return initialResult;
   }
}
