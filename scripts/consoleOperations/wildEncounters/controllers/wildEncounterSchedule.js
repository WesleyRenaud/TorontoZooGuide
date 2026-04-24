import { loadWildEncounters } from '../../options/loaders.js';
import { populateWildEncounterDropdown } from '../../options/dropdowns.js';
import { setWildEncounterSchedule } from '../../../api/consoleOperationsApi.js';
import {
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { createRecurringScheduleFormController } from '../../forms/recurringScheduleFormController.js';

export function createWildEncounterScheduleController({
   wildEncounterEl,
   startDateEl,
   endDateEl,
   timeEl,
   mondayEl,
   tuesdayEl,
   wednesdayEl,
   thursdayEl,
   fridayEl,
   saturdayEl,
   sundayEl,
   messageEl,
   ...controllerOptions
} = {}) {
   const dayFieldEls = [
      mondayEl,
      tuesdayEl,
      wednesdayEl,
      thursdayEl,
      fridayEl,
      saturdayEl,
      sundayEl,
   ];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function validateSelection({
      wildEncounter,
   }) {
      if (!wildEncounter) {
         return 'Wild Encounter is required.';
      }

      return null;
   }

   async function submitSchedule({
      wildEncounter,
      startDate,
      endDate,
      time,
      message,
   }) {
      return setWildEncounterSchedule({
         wildEncounter,
         startDate: startDate || null,
         endDate: endDate || null,
         time,
         monday: Boolean(mondayEl?.checked),
         tuesday: Boolean(tuesdayEl?.checked),
         wednesday: Boolean(wednesdayEl?.checked),
         thursday: Boolean(thursdayEl?.checked),
         friday: Boolean(fridayEl?.checked),
         saturday: Boolean(saturdayEl?.checked),
         sunday: Boolean(sundayEl?.checked),
         message,
      });
   }

   async function prepareForm() {
      if (wildEncounterEl?.tagName === 'SELECT') {
         const wildEncounters = await loadWildEncounters();
         populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
      }
   }

   return createRecurringScheduleFormController({
      ...controllerOptions,
      startDateEl,
      endDateEl,
      timeEl,
      messageEl,
      dayFieldEls,
      resetSelection: () => {
         resetFormFields([wildEncounterEl]);
      },
      getSelectionValues: () => ({
         wildEncounter: getFieldValue(wildEncounterEl),
      }),
      validateSelection,
      prepareForm,
      loadErrorMessage: 'Failed to load Wild Encounters.',
      submitSchedule,
      successMessage: result => `${result.wildEncounter} schedule was saved.`,
      timeRequiredMessage: 'Encounter time is required.',
   });
}
