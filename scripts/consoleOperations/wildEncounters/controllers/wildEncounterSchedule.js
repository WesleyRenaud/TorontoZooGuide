import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { RecurringScheduleFormController } from '../../forms/recurringScheduleFormController.js';
import { WildEncounterScheduleRowsController } from '../../forms/wildEncounterScheduleRowsController.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export class WildEncounterSchedule {
   static createWildEncounterScheduleController({
      wildEncounterEl,
      startDateEl,
      endDateEl,
      scheduleRowsEl,
      addScheduleRowEl,
      messageEl,
      ...controllerOptions
   } = {}) {
      const scheduleRowsController = WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController({
         rowsEl: scheduleRowsEl,
         addRowButtonEl: addScheduleRowEl,
      });


      function validateSelection({
         wildEncounter,
      }) {
         if (!wildEncounter) {
            return APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.wildEncounter);
         }

         return null;
      }

      async function submitSchedule({
         wildEncounter,
         startDate,
         endDate,
         message,
      }) {
         const scheduleRows = scheduleRowsController.getRows();
         const payload = {
            wildEncounter,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
            scheduleRows,
         };

         const result = await ConsoleOperationsApi.setWildEncounterSchedule(payload);

         if (result.success || !OpeningScheduleOverlap.resultHasOpeningScheduleOverlap(result)) {
            return result;
         }

         const resolution = await showOpeningScheduleOverlapDialog();

         if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
            return ConsoleOperationsApi.replaceWildEncounterScheduleOverlaps(payload);
         }

         if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
            return ConsoleOperationsApi.trimWildEncounterScheduleOverlaps(payload);
         }

         return { success: false, dismissed: true };
      }

      async function prepareForm() {
         if (wildEncounterEl?.tagName === 'SELECT') {
            const wildEncounters = await Loaders.loadWildEncounters();
            Dropdowns.populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
         }
      }

      return RecurringScheduleFormController.createRecurringScheduleFormController({
         ...controllerOptions,
         startDateEl,
         endDateEl,
         messageEl,
         resetSelection: () => {
            ControllerUtils.resetFormFields([wildEncounterEl, startDateEl, endDateEl, messageEl]);
         },
         resetScheduleTimes: () => {
            scheduleRowsController.reset();
         },
         validateRecurringSchedule: () => scheduleRowsController.validate(),
         getSelectionValues: () => ({
            wildEncounter: ControllerUtils.getFieldValue(wildEncounterEl),
         }),
         validateSelection,
         prepareForm,
         loadErrorMessage: APP_STRINGS.loadErrors.wildEncounters,
         submitSchedule,
         successMessage: result => APP_STRINGS.status.scheduleSaved(result.wildEncounter),
         shouldReportSubmitFailure: result => !result?.dismissed,
      });
   }
}
