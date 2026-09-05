import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { JoinedTimesFormatter } from '../../../shared/joinedTimesFormatter.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export class CancelWildEncounterOccurrence {
   static createCancelWildEncounterOccurrenceController({
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
         return ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl);
      }

      function resetOccurrenceFields() {
         if (occurrenceFilterController?.clear) {
            occurrenceFilterController.clear();
         }
      }

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
         resetOccurrenceFields();
      }

      function getFormValues() {
         return {
            wildEncounter: ControllerUtils.getFieldValue(wildEncounterEl),
            date: ControllerUtils.getFieldValue(dateEl),
            times: getSelectedTimes(),
         };
      }

      function show() {
         Status.setStatus(statusEl, '');
         activatePanel?.(panelEl);
      }

      function hide() {
         ControllerUtils.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: Status.setStatus,
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
            const wildEncounters = await Loaders.loadWildEncounters();
            Dropdowns.populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
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
         Status.setStatus(
            statusEl,
            `${result.wildEncounter} on ${result.date} at ${JoinedTimesFormatter.format(result.times)} was cancelled.`,
            'is-success'
         );

         resetForm();
      }

      async function onShowClick() {
         Status.setStatus(statusEl, '');

         try {
            resetForm();
            await prepareForm();
            show();
         }
         catch (err) {
            Status.setStatus(statusEl, APP_STRINGS.loadErrors.wildEncounters, 'is-error');
            show();
         }
      }

      async function onSubmitClick() {
         const formValues = getFormValues();

         Status.setStatus(statusEl, '');

         const validationError = validateForm(formValues);

         if (validationError) {
            Status.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await submitOccurrenceCancellation(formValues);

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else {
               Status.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch (err) {
            Status.setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
         }
      }

      wildEncounterEl?.addEventListener('change', async () => {
         ControllerUtils.resetFormFields([dateEl]);
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
}
