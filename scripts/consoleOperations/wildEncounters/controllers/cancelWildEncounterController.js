import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class CancelWildEncounterController {
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
         ControllerHelper.resetFormFields(formFieldEls);
         resetOccurrenceFields();
      }

      function getFormValues() {
         return {
            wildEncounter: ControllerHelper.getFieldValue(wildEncounterEl),
            date: ControllerHelper.getFieldValue(dateEl),
            times: getSelectedTimes(),
         };
      }

      function show() {
         ConsoleStatusPresenter.setStatus(statusEl, '');
         activatePanel?.(panelEl);
      }

      function hide() {
         ControllerHelper.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      function validateForm({ wildEncounter, date, times }) {
         if (!wildEncounter) {
            return Strings.validation.entityRequired(Strings.entityLabels.wildEncounter);
         }

         if (!date) {
            return Strings.validation.entityRequired(Strings.labels.date);
         }

         if (!times.length) {
            return Strings.validation.entityRequired(Strings.labels.encounterTimes);
         }

         return null;
      }

      async function prepareForm() {
         if (wildEncounterEl?.tagName === 'SELECT') {
            const wildEncounters = await ConsoleOptionsLoader.loadWildEncounters();
            ConsoleDropdownPopulator.populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
         }
      }

      async function submitOccurrenceCancellation({ wildEncounter, date, times }) {
         return ConsoleOperationsClient.cancelWildEncounterOccurrence({
            wildEncounter,
            date,
            times,
         });
      }

      function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            Strings.status.wildEncounterOccurrenceCancelled(result),
            'is-success'
         );

         resetForm();
      }

      async function onShowClick() {
         ConsoleStatusPresenter.setStatus(statusEl, '');

         try {
            resetForm();
            await prepareForm();
            show();
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.loadErrors.wildEncounters, 'is-error');
            show();
         }
      }

      async function onSubmitClick() {
         const formValues = getFormValues();

         ConsoleStatusPresenter.setStatus(statusEl, '');

         const validationError = validateForm(formValues);

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await submitOccurrenceCancellation(formValues);

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else {
               ConsoleStatusPresenter.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      wildEncounterEl?.addEventListener('change', async () => {
         ControllerHelper.resetFormFields([dateEl]);
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
