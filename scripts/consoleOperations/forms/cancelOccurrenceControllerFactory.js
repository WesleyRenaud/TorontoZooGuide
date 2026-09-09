import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { ScheduleTimesCheckboxField } from './scheduleTimesCheckboxField.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
import { Strings } from '../../strings.js';

export class CancelOccurrenceControllerFactory {
   static createCancelOccurrenceController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      dateEl,
      timesEl,
      activatePanel,
      occurrenceFilterController = null,
      resetSelection = null,
      getSelectionValues,
      validateSelection = null,
      prepareForm = null,
      loadErrorMessage = Strings.loadErrors.options,
      submitOccurrenceCancellation,
      successMessage,
   } = {}) {
      const formFieldEls = [dateEl];


      function getSelectedTimes() {
         return ScheduleTimesCheckboxField.getSelectedScheduleTimes(timesEl);
      }

      function resetOccurrenceFields() {
         occurrenceFilterController?.clear?.();
      }

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
         resetSelection?.();
         resetOccurrenceFields();
      }

      function getFormValues() {
         return {
            ...(typeof getSelectionValues === 'function'
               ? getSelectionValues()
               : {}),
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

      function validateForm(formValues) {
         return validateSelection?.(formValues) ?? null;
      }

      function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            successMessage(result),
            'is-success'
         );

         resetForm();
      }

      async function onShowClick() {
         ConsoleStatusPresenter.setStatus(statusEl, '');

         try {
            resetForm();
            await prepareForm?.();
            show();
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, loadErrorMessage, 'is-error');
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

      dateEl?.addEventListener('change', () => {
         occurrenceFilterController?.refreshTimes?.();
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
