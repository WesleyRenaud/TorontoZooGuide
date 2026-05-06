import { endWildEncounterSchedule } from '../../../api/consoleOperationsApi.js';
import { createEndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';
import { resetFormFields } from '../../helpers/controllerUtils.js';
import { populateWildEncounterDropdown } from '../../options/dropdowns.js';
import { loadWildEncounters } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createEndWildEncounterScheduleController({
   wildEncounterEl,
   endDateEl,
   ...controllerOptions
} = {}) {
   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function validateSelection({ wildEncounter }) {
      if (!wildEncounter) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.wildEncounter);
      }

      return null;
   }

   async function submitEndSchedule({ wildEncounter, endDate }) {
      return endWildEncounterSchedule({
         wildEncounter,
         endDate: endDate || null,
      });
   }

   async function prepareForm() {
      if (wildEncounterEl?.tagName === 'SELECT') {
         const wildEncounters = await loadWildEncounters();
         populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
      }
   }

   return createEndRecurringScheduleFormController({
      ...controllerOptions,
      endDateEl,
      resetSelection: () => {
         resetFormFields([wildEncounterEl]);
      },
      getSelectionValues: () => ({
         wildEncounter: getFieldValue(wildEncounterEl),
      }),
      validateSelection,
      prepareForm,
      loadErrorMessage: APP_STRINGS.loadErrors.wildEncounters,
      submitEndSchedule,
      successMessage: result => APP_STRINGS.status.scheduleEnded(result.wildEncounter),
   });
}
