import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { getSelectedScheduleTimes } from '../../forms/scheduleTimesCheckboxField.js';
import {
   getFieldValue,
   hideConsolePanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { populateWildEncounterDropdown } from '../../options/dropdowns.js';
import { loadWildEncounters } from '../../options/loaders.js';
import { JoinedTimesFormatter } from '../../../shared/joinedTimesFormatter.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export function createCancelWildEncounterOccurrenceController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   wildEncounterEl,
   dateEl,
   timesEl,
   activatePanel,
   occurrenceFilterController = null,
} = {}) {
   const formFieldEls = [wildEncounterEl, dateEl];


   function getSelectedTimes() {
      return getSelectedScheduleTimes(timesEl);
   }

   function resetOccurrenceFields() {
      if (occurrenceFilterController?.clear) {
         occurrenceFilterController.clear();
      }
   }

   function resetForm() {
      resetFormFields(formFieldEls);
      resetOccurrenceFields();
   }

   function getFormValues() {
      return {
         wildEncounter: getFieldValue(wildEncounterEl),
         date: getFieldValue(dateEl),
         times: getSelectedTimes(),
      };
   }

   function show() {
      setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   function validateForm({ wildEncounter, date, times }) {
      if (!wildEncounter) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.wildEncounter);
      }

      if (!date) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.date);
      }

      if (!times.length) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.encounterTimes);
      }

      return null;
   }

   async function prepareForm() {
      if (wildEncounterEl?.tagName === 'SELECT') {
         const wildEncounters = await loadWildEncounters();
         populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
      }
   }

   async function submitOccurrenceCancellation({ wildEncounter, date, times }) {
      return ConsoleOperationsApi.cancelWildEncounterOccurrence({
         wildEncounter,
         date,
         times,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         `${result.wildEncounter} on ${result.date} at ${JoinedTimesFormatter.format(result.times)} was cancelled.`,
         'is-success'
      );

      resetForm();
   }

   async function onShowClick() {
      setStatus(statusEl, '');

      try {
         resetForm();
         await prepareForm();
         show();
      }
      catch (err) {
         setStatus(statusEl, APP_STRINGS.loadErrors.wildEncounters, 'is-error');
         show();
      }
   }

   async function onSubmitClick() {
      const formValues = getFormValues();

      setStatus(statusEl, '');

      const validationError = validateForm(formValues);

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await submitOccurrenceCancellation(formValues);

         if (result.success) {
            handleSubmitSuccess(result);
         }
         else {
            setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
         }
      }
      catch (err) {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
      }
   }

   wildEncounterEl?.addEventListener('change', async () => {
      resetFormFields([dateEl]);
      resetOccurrenceFields();

      if (occurrenceFilterController?.refresh) {
         await occurrenceFilterController.refresh();
      }
   });

   dateEl?.addEventListener('change', () => {
      if (occurrenceFilterController?.refreshTimes) {
         occurrenceFilterController.refreshTimes();
      }
   });

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
