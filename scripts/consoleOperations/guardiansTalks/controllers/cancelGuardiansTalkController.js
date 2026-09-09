import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ScheduleTimesCheckboxField } from '../../forms/scheduleTimesCheckboxField.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class CancelGuardiansTalkController {
   static createCancelGuardiansTalkOccurrenceController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      talkNameEl,
      locationEl,
      dateEl,
      timesEl,
      activatePanel,
      talkLocationFilterController = null,
      occurrenceFilterController = null,
   } = {}) {
      const formFieldEls = [locationEl, dateEl];


      function getSelectedTimes() {
         return ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl);
      }

      function resetOccurrenceFields() {
         if (occurrenceFilterController?.clear) {
            occurrenceFilterController.clear();
         }
      }

      function resetTalkDropdown() {
         if (talkLocationFilterController?.clear) {
            talkLocationFilterController.clear();
         }
         else if (talkNameEl?.tagName === 'SELECT') {
            ConsoleDropdownPopulator.populateGuardiansTalkDropdown(talkNameEl, []);
         }
         else if (talkNameEl) {
            talkNameEl.value = '';
         }

         resetOccurrenceFields();
      }

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
         resetTalkDropdown();
      }

      function getFormValues() {
         return {
            talk: ControllerHelper.getFieldValue(talkNameEl),
            location: ControllerHelper.getFieldValue(locationEl),
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

      function validateForm({ talk, location, date, times }) {
         if (!location) {
            return Strings.validation.entityRequired(Strings.labels.location);
         }

         if (!talk) {
            return Strings.validation.entityRequired(Strings.labels.talkName);
         }

         if (!date) {
            return Strings.validation.entityRequired(Strings.labels.date);
         }

         if (!times.length) {
            return Strings.validation.entityRequired(Strings.labels.talkTimes);
         }

         return null;
      }

      async function refreshLocations() {
         if (talkLocationFilterController?.refreshLocations) {
            await talkLocationFilterController.refreshLocations();
         }
      }

      async function submitOccurrenceCancellation({ talk, location, date, times }) {
         return ConsoleOperationsClient.cancelGuardiansTalkOccurrence({
            talk,
            location,
            date,
            times,
         });
      }

      function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            Strings.status.guardiansTalkOccurrenceCancelled(result),
            'is-success'
         );

         resetForm();
      }

      async function onShowClick() {
         ConsoleStatusPresenter.setStatus(statusEl, '');

         try {
            resetForm();
            await refreshLocations();
            show();
         }
         catch(err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.loadErrors.locations, 'is-error');
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
         catch(err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      locationEl?.addEventListener('change', () => {
         resetOccurrenceFields();
      });

      talkNameEl?.addEventListener('change', async () => {
         if (occurrenceFilterController?.refresh) {
            await occurrenceFilterController.refresh();
         }
         else {
            resetOccurrenceFields();
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
