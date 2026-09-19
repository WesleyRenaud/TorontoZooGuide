import { AnimalExhibitAutofillController } from '../animals/controllers/animalExhibitAutofillController.js';
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
      speciesEl = null,
      loadOptionsForSpecies = null,
      onUniqueFill = null,
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
            const result = await submitAlert(formValues);

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

      if (speciesEl && loadOptionsForSpecies) {
         AnimalExhibitAutofillController.createAnimalExhibitAutofillController({
            speciesEl,
            exhibitEl: targetEl,
            loadExhibits: loadOptions,
            loadExhibitsForSpecies: loadOptionsForSpecies,
            populateExhibits: populateOptions,
            onUniqueFill,
         });
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
