import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class EndWildEncounterSchedule {
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
         return ConsoleOperationsApi.endWildEncounterSchedule({
            wildEncounter,
            times,
            endDate: endDate || null,
         });
      }

      async function prepareForm() {
         if (wildEncounterEl?.tagName === 'SELECT') {
            const wildEncounters = await Loaders.loadWildEncounters();
            Dropdowns.populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
         }

         await scheduleTimesFilterController?.refresh?.();
      }

      const controller = EndRecurringScheduleFormController.createEndRecurringScheduleFormController({
         ...controllerOptions,
         endDateEl,
         resetSelection: () => {
            ControllerUtils.resetFormFields([wildEncounterEl]);
            scheduleTimesFilterController?.clear?.();
         },
         getSelectionValues: () => ({
            wildEncounter: ControllerUtils.getFieldValue(wildEncounterEl),
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
