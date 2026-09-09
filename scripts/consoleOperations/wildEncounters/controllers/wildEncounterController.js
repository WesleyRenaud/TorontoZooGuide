import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { OpeningScheduleChecker } from '../../forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapResolver } from '../../forms/openingScheduleOverlapResolver.js';
import { RecurringScheduleFormController } from '../../forms/recurringScheduleFormController.js';
import { WildEncounterScheduleRowsController } from '../../forms/wildEncounterScheduleRowsController.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class WildEncounterController {
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
            return Strings.validation.entityRequired(Strings.entityLabels.wildEncounter);
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

         const result = await ConsoleOperationsClient.setWildEncounterSchedule(payload);

         if (result.success || !OpeningScheduleChecker.resultHasOpeningScheduleOverlap(result)) {
            return result;
         }

         return OpeningScheduleOverlapResolver.resolveOpeningScheduleOverlapConflict({
            payload,
            replaceOverlaps: ConsoleOperationsClient.replaceWildEncounterScheduleOverlaps,
            trimOverlaps: ConsoleOperationsClient.trimWildEncounterScheduleOverlaps,
            dismissedResult: { success: false, dismissed: true },
         });
      }

      async function prepareForm() {
         if (wildEncounterEl?.tagName === 'SELECT') {
            const wildEncounters = await ConsoleOptionsLoader.loadWildEncounters();
            ConsoleDropdownPopulator.populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
         }
      }

      return RecurringScheduleFormController.createRecurringScheduleFormController({
         ...controllerOptions,
         startDateEl,
         endDateEl,
         messageEl,
         resetSelection: () => {
            ControllerHelper.resetFormFields([wildEncounterEl, startDateEl, endDateEl, messageEl]);
         },
         resetScheduleTimes: () => {
            scheduleRowsController.reset();
         },
         validateRecurringSchedule: () => scheduleRowsController.validate(),
         getSelectionValues: () => ({
            wildEncounter: ControllerHelper.getFieldValue(wildEncounterEl),
         }),
         validateSelection,
         prepareForm,
         loadErrorMessage: Strings.loadErrors.wildEncounters,
         submitSchedule,
         successMessage: result => Strings.status.scheduleSaved(result.wildEncounter),
         shouldReportSubmitFailure: result => !result?.dismissed,
      });
   }
}
