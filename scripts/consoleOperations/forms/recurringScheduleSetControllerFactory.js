import { OpeningScheduleChecker } from './openingScheduleChecker.js';
import { OpeningScheduleOverlapResolver } from './openingScheduleOverlapResolver.js';
import { RecurringScheduleFormController } from './recurringScheduleFormController.js';
import { RecurringScheduleRowsController } from './recurringScheduleRowsController.js';

export class RecurringScheduleSetControllerFactory {
   static createRecurringScheduleSetController({
      scheduleRowsEl,
      addScheduleRowEl,
      startDateEl,
      endDateEl,
      messageEl,
      getSelectionValues,
      validateSelection,
      resetSelection,
      prepareForm,
      loadErrorMessage,
      successMessage,
      setSchedule,
      replaceOverlaps,
      trimOverlaps,
      ...controllerOptions
   } = {}) {
      const scheduleRowsController = RecurringScheduleRowsController.createRecurringScheduleRowsController({
         rowsEl: scheduleRowsEl,
         addRowButtonEl: addScheduleRowEl,
      });

      async function submitSchedule(formValues = {}) {
         const { startDate, endDate, message, time, times, ...selection } = formValues;
         void time;
         void times;
         const payload = {
            ...selection,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
            scheduleRows: scheduleRowsController.getRows(),
         };

         const result = await setSchedule(payload);

         if (result.success || !OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result)) {
            return result;
         }

         return OpeningScheduleOverlapResolver.resolveOpeningScheduleOverlapConflict({
            payload,
            replaceOverlaps,
            trimOverlaps,
            dismissedResult: { success: false, dismissed: true },
         });
      }

      return RecurringScheduleFormController.createRecurringScheduleFormController({
         ...controllerOptions,
         startDateEl,
         endDateEl,
         messageEl,
         resetSelection,
         resetScheduleTimes: () => {
            scheduleRowsController.reset();
         },
         validateRecurringSchedule: () => scheduleRowsController.validate(),
         getSelectionValues,
         validateSelection,
         prepareForm,
         loadErrorMessage,
         submitSchedule,
         successMessage,
         shouldReportSubmitFailure: result => !result?.dismissed,
      });
   }
}
