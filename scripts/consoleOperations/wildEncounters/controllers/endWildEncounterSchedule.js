import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { createEndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import {
   getFieldValue,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { populateWildEncounterDropdown } from '../../options/dropdowns.js';
import { loadWildEncounters } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createEndWildEncounterScheduleController({
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
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.wildEncounter);
      }

      if (!times.length) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.encounterTimes);
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
         const wildEncounters = await loadWildEncounters();
         populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
      }

      await scheduleTimesFilterController?.refresh?.();
   }

   const controller = createEndRecurringScheduleFormController({
      ...controllerOptions,
      endDateEl,
      resetSelection: () => {
         resetFormFields([wildEncounterEl]);
         scheduleTimesFilterController?.clear?.();
      },
      getSelectionValues: () => ({
         wildEncounter: getFieldValue(wildEncounterEl),
         times: getSelectedTimes(),
      }),
      validateSelection,
      prepareForm,
      loadErrorMessage: APP_STRINGS.loadErrors.wildEncounters,
      submitEndSchedule,
      successMessage: result => APP_STRINGS.status.scheduleEnded(result.wildEncounter),
   });

   wildEncounterEl?.addEventListener('change', async () => {
      scheduleTimesFilterController?.clear?.();
      await scheduleTimesFilterController?.refresh?.();
   });

   return controller;
}
