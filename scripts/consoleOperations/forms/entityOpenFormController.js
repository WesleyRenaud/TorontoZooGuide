import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
import { Strings } from '../../strings.js';

export class EntityOpenFormController {
   static createEntityOpenFormController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      entityEl,
      startDateEl = null,
      endDateEl = null,
      activatePanel,
      loadOptions,
      populateOptions,
      submitOpenStatus,
      entityLabel = Strings.entityLabels.item,
      optionsLabel = Strings.entityLabels.items,
      loadErrorMessage = Strings.loadErrors.entityOptions(optionsLabel),
      successMessage = () => Strings.status.open(entityLabel),
   } = {}) {
      const formFieldEls = [entityEl, startDateEl, endDateEl];
      const hasDateRange = Boolean(startDateEl || endDateEl);


      function getFormValues() {
         return {
            entity: ControllerHelper.getFieldValue(entityEl),
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
         };
      }

      function validateForm({ entity, startDate, endDate }) {
         if (!entity) {
            return Strings.validation.entityRequired(entityLabel);
         }

         if (!hasDateRange) {
            return null;
         }

         return ControllerHelper.validateOptionalDateRange(startDate, endDate);
      }

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
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
         await ControllerHelper.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions,
            populateOptions,
            targetEl: entityEl,
            resetForm,
            activatePanel,
            panelEl,
            errorMessage: loadErrorMessage,
         });
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
            const result = await submitOpenStatus(formValues);

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
