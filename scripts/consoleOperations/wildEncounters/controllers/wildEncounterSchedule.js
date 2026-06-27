import { setWildEncounterSchedule } from '../../../api/consoleOperationsApi.js';
import { initMultiTimePicker } from '../../../datePickers/multiTimePicker.js';
import { createMultiTimeFieldController } from '../../forms/multiTimeFieldController.js';
import { createRecurringScheduleFormController } from '../../forms/recurringScheduleFormController.js';
import { resetFormFields } from '../../helpers/controllerUtils.js';
import { populateWildEncounterDropdown } from '../../options/dropdowns.js';
import { loadWildEncounters } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createWildEncounterScheduleController({
   wildEncounterEl,
   startDateEl,
   endDateEl,
   timesListEl,
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

   const multiTimeField = createMultiTimeFieldController({
      listEl: timesListEl,
      inputEl: timeEl,
   });

   initMultiTimePicker(timeEl, {
      onCommitTime: (time) => {
         multiTimeField.addTime(time);
      },
      onRemoveLastTime: () => multiTimeField.removeLastTime(),
   });

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

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
      times,
      message,
   }) {
      return setWildEncounterSchedule({
         wildEncounter,
         startDate: startDate || null,
         endDate: endDate || null,
         times,
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
      resetScheduleTimes: () => {
         multiTimeField.reset();
      },
      getScheduleTimes: () => {
         multiTimeField.commitPendingInput();
         return multiTimeField.getTimes();
      },
      getSelectionValues: () => ({
         wildEncounter: getFieldValue(wildEncounterEl),
      }),
      validateSelection,
      prepareForm,
      loadErrorMessage: APP_STRINGS.loadErrors.wildEncounters,
      submitSchedule,
      successMessage: result => APP_STRINGS.status.scheduleSaved(result.wildEncounter),
      timeRequiredMessage: APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.encounterTimes),
   });
}
