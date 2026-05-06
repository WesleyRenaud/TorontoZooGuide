import { loadWildEncounters } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';
import { populateWildEncounterDropdown } from '../../options/dropdowns.js';
import { setStatus } from '../../shell/status.js';
import { cancelWildEncounterOccurrence } from '../../../api/consoleOperationsApi.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';

export function createCancelWildEncounterOccurrenceController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   wildEncounterEl,
   dateEl,
   timeEl,
   activatePanel,
   occurrenceFilterController = null,
} = {}) {
   const formFieldEls = [wildEncounterEl, dateEl, timeEl];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function resetOccurrenceDropdowns() {
      if (occurrenceFilterController?.clear) {
         occurrenceFilterController.clear();
      }
      else {
         resetFormFields([dateEl, timeEl]);
      }
   }

   function resetForm() {
      resetFormFields(formFieldEls);
      resetOccurrenceDropdowns();
   }

   function getFormValues() {
      return {
         wildEncounter: getFieldValue(wildEncounterEl),
         date: getFieldValue(dateEl),
         time: getFieldValue(timeEl),
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

   function validateForm({ wildEncounter, date, time }) {
      if (!wildEncounter) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.entityLabels.wildEncounter);
      }

      if (!date) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.date);
      }

      if (!time) {
         return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.time);
      }

      return null;
   }

   async function submitOccurrenceCancellation({ wildEncounter, date, time }) {
      return cancelWildEncounterOccurrence({
         wildEncounter,
         date,
         time,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         `${result.wildEncounter} on ${result.date} at ${result.time} was cancelled.`,
         'is-success'
      );

      resetForm();
   }

   async function onShowClick() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus,
         loadOptions: loadWildEncounters,
         populateOptions: populateWildEncounterDropdown,
         targetEl: wildEncounterEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: APP_STRINGS.loadErrors.wildEncounters,
      });
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
            setStatus(statusEl, result.error || APP_STRINGS.common.genericFailed, 'is-error');
         }
      }
      catch(err) {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
      }
   }

   wildEncounterEl?.addEventListener('change', async () => {
      resetFormFields([dateEl, timeEl]);

      if (occurrenceFilterController?.refresh) {
         await occurrenceFilterController.refresh();
      }
   });

   dateEl?.addEventListener('change', () => {
      resetFormFields([timeEl]);

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
