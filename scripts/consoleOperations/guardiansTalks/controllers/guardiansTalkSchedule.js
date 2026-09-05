import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { OpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { RecurringScheduleFormController } from '../../forms/recurringScheduleFormController.js';
import { WildEncounterScheduleRowsController } from '../../forms/wildEncounterScheduleRowsController.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { APP_STRINGS } from '../../../strings.js';

export class GuardiansTalkSchedule {
   static createGuardiansTalkScheduleController({
      talkNameEl,
      locationEl,
      startDateEl,
      endDateEl,
      scheduleRowsEl,
      addScheduleRowEl,
      messageEl,
      talkLocationFilterController = null,
      ...controllerOptions
   } = {}) {
      const scheduleRowsController = WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController({
         rowsEl: scheduleRowsEl,
         addRowButtonEl: addScheduleRowEl,
      });


      function resetTalkDropdown() {
         if (talkLocationFilterController?.clear) {
            talkLocationFilterController.clear();
            return;
         }

         if (talkNameEl?.tagName === 'SELECT') {
            Dropdowns.populateGuardiansTalkDropdown(talkNameEl, []);
         }
         else if (talkNameEl) {
            talkNameEl.value = '';
         }
      }

      function validateSelection({ talk, location }) {
         if (!location) {
            return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.location);
         }

         if (!talk) {
            return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.talkName);
         }

         return null;
      }

      async function submitSchedule({
         talk,
         location,
         startDate,
         endDate,
         message,
      }) {
         const scheduleRows = scheduleRowsController.getRows();
         const payload = {
            talk,
            location,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
            scheduleRows,
         };

         const result = await ConsoleOperationsApi.setGuardiansTalkSchedule(payload);

         if (result.success || !OpeningScheduleOverlap.resultHasOpeningScheduleOverlap(result)) {
            return result;
         }

         const resolution = await OpeningScheduleOverlapDialog.showOpeningScheduleOverlapDialog();

         if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
            return ConsoleOperationsApi.replaceGuardiansTalkScheduleOverlaps(payload);
         }

         if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
            return ConsoleOperationsApi.trimGuardiansTalkScheduleOverlaps(payload);
         }

         return { success: false, dismissed: true };
      }

      async function prepareForm() {
         if (talkLocationFilterController?.refreshLocations) {
            await talkLocationFilterController.refreshLocations();
         }
      }

      return RecurringScheduleFormController.createRecurringScheduleFormController({
         ...controllerOptions,
         startDateEl,
         endDateEl,
         messageEl,
         resetSelection: () => {
            ControllerUtils.resetFormFields([locationEl, startDateEl, endDateEl, messageEl]);
            resetTalkDropdown();
         },
         resetScheduleTimes: () => {
            scheduleRowsController.reset();
         },
         validateRecurringSchedule: () => scheduleRowsController.validate(),
         getSelectionValues: () => ({
            talk: ControllerUtils.getFieldValue(talkNameEl),
            location: ControllerUtils.getFieldValue(locationEl),
         }),
         validateSelection,
         prepareForm,
         loadErrorMessage: APP_STRINGS.loadErrors.locations,
         submitSchedule,
         successMessage: result => APP_STRINGS.status.guardiansTalkScheduleSaved(result),
         shouldReportSubmitFailure: result => !result?.dismissed,
      });
   }
}
