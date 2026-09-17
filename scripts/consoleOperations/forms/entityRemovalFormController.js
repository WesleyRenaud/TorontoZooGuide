import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
import { Strings } from '../../strings.js';

export class EntityRemovalFormController {
   static createEntityRemovalFormController({
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
      submitRemoval,
      successMessage,
      bindResetValueOnChange = null,
   } = {}) {
      function clearFields() {
         ControllerHelper.resetFormFields(formFieldEls);
      }

      async function resetForm() {
         try {
            await ControllerHelper.reloadOptions({
               loadOptions,
               populateOptions,
               targetEl,
               resetForm: clearFields,
            });
         }
         catch (err) {
            clearFields();
         }
      }

      async function show() {
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions,
            populateOptions,
            targetEl,
            resetForm: clearFields,
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

      async function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            typeof successMessage === 'function'
               ? successMessage(result)
               : successMessage,
            'is-success'
         );

         await resetForm();
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
            const result = await submitRemoval(formValues);

            if (result.success) {
               await handleSubmitSuccess(result);
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
