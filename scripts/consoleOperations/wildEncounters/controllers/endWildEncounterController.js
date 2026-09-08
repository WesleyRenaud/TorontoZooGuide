import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class EndWildEncounterController {
   static createEndWildEncounterScheduleController({
      wildEncounterEl,
      timesEl,
      endDateEl,
      scheduleTimesFilterController = null,
      ...controllerOptions
   } = {}) {

      function getSelectedTimes() {
         return ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl);
      }

      function validateSelection({ wildEncounter, times }) {
         if (!wildEncounter) {
            return Strings.validation.entityRequired(Strings.entityLabels.wildEncounter);
         }

         if (!times.length) {
            return Strings.validation.entityRequired(Strings.labels.encounterTimes);
         }

         return null;
      }

      async function submitEndSchedule({ wildEncounter, times, endDate }) {
         return ConsoleOperationsClient.endWildEncounterSchedule({
            wildEncounter,
            times,
            endDate: endDate || null,
         });
      }

      async function prepareForm() {
         if (wildEncounterEl?.tagName === 'SELECT') {
            const wildEncounters = await ConsoleOptionsLoader.loadWildEncounters();
            ConsoleDropdownPopulator.populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
         }

         await scheduleTimesFilterController?.refresh?.();
      }

      const controller = EndRecurringScheduleFormController.createEndRecurringScheduleFormController({
         ...controllerOptions,
         endDateEl,
         resetSelection: () => {
            ControllerHelper.resetFormFields([wildEncounterEl]);
            scheduleTimesFilterController?.clear?.();
         },
         getSelectionValues: () => ({
            wildEncounter: ControllerHelper.getFieldValue(wildEncounterEl),
            times: getSelectedTimes(),
         }),
         validateSelection,
         prepareForm,
         loadErrorMessage: Strings.loadErrors.wildEncounters,
         submitEndSchedule,
         successMessage: result => Strings.status.scheduleEnded(result.wildEncounter),
      });

      wildEncounterEl?.addEventListener('change', async () => {
         scheduleTimesFilterController?.clear?.();
         await scheduleTimesFilterController?.refresh?.();
      });

      return controller;
   }
}
