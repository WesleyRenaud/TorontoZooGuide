import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
import { Strings } from '../../strings.js';

export class AddOccurrenceControllerFactory {
   static createAddOccurrenceController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      formFieldEls = [],
      activatePanel,
      resetSelection = null,
      getFormValues,
      validateForm = null,
      prepareForm = null,
      loadErrorMessage = Strings.loadErrors.options,
      submitOccurrence,
      successMessage,
   } = {}) {

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
         resetSelection?.();
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
         const formValues = typeof getFormValues === 'function'
            ? getFormValues()
            : {};

         ConsoleStatusPresenter.setStatus(statusEl, '');

         const validationError = validateForm?.(formValues) ?? null;

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await submitOccurrence(formValues);

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

      showButtonEl?.addEventListener('click', onShowClick);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return {
         show,
         hide,
      };
   }
}
