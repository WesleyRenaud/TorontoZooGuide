import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
import { Strings } from '../../strings.js';

export class EntityAlertFormController {
   static createEntityAlertFormController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      formFieldEls = [],
      activatePanel,
      loadOptions,
      populateOptions,
      targetEl,
      loadErrorMessage,
      getFormValues,
      validateForm,
      submitAlert,
      successMessage,
      bindResetValueOnChange = null,
   } = {}) {
      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
      }

      async function show() {
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions,
            populateOptions,
            targetEl,
            resetForm,
            activatePanel,
            panelEl,
            errorMessage: loadErrorMessage,
         });
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
            typeof successMessage === 'function'
               ? successMessage(result)
               : successMessage,
            'is-success'
         );

         resetForm();
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
            const result = await submitAlert(formValues);

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

      if (bindResetValueOnChange) {
         ControllerHelper.bindResetValueOnChange(
            bindResetValueOnChange.sourceEl,
            bindResetValueOnChange.targetEl
         );
      }

      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return {
         show,
         hide,
      };
   }
}
