import { loadWildEncounters } from '../../options/loaders.js';
import { populateWildEncounterDropdown } from '../../options/dropdowns.js';
import { endWildEncounterSchedule } from '../../../api/consoleOperationsApi.js';
import { resetFormFields } from '../../helpers/controllerUtils.js';
import { createEndRecurringScheduleFormController } from '../../forms/endRecurringScheduleFormController.js';

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
         return 'Wild Encounter is required.';
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
      loadErrorMessage: 'Failed to load Wild Encounters.',
      submitEndSchedule,
      successMessage: result => `${result.wildEncounter} schedule was ended.`,
   });
}
