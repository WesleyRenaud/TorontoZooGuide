import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerUtils } from '../helpers/controllerUtils.js';
import { Status } from '../shell/status.js';
import { Strings } from '../../strings.js';

export class EntityClosedFormController {
   static createEntityClosedFormController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      entityEl,
      startDateEl = null,
      endDateEl = null,
      messageEl = null,
      activatePanel,
      loadOptions,
      populateOptions,
      submitClosedStatus,
      entityLabel = Strings.entityLabels.item,
      optionsLabel = Strings.entityLabels.items,
      loadErrorMessage = Strings.loadErrors.entityOptions(optionsLabel),
      successMessage = () => Strings.status.closed(entityLabel),
   } = {}) {
      const formFieldEls = [entityEl, startDateEl, endDateEl, messageEl];
      const hasDateRange = Boolean(startDateEl || endDateEl);


      function getFormValues() {
         return {
            entity: ControllerUtils.getFieldValue(entityEl),
            startDate: ControllerUtils.getFieldValue(startDateEl),
            endDate: ControllerUtils.getFieldValue(endDateEl),
            message: ControllerUtils.getFieldValue(messageEl),
         };
      }

      function validateForm({ entity, startDate, endDate }) {
         if (!entity) {
            return Strings.validation.entityRequired(entityLabel);
         }

         if (!hasDateRange) {
            return null;
         }

         return ControllerUtils.validateOptionalDateRange(startDate, endDate);
      }

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
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

      function handleSubmitSuccess(result) {
         Status.setStatus(
            statusEl,
            successMessage(result),
            'is-success'
         );

         resetForm();
      }

      async function onShowClick() {
         await ControllerUtils.loadOptionsAndShowPanel({
            statusEl,
            setStatus: Status.setStatus,
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

         Status.setStatus(statusEl, '');

         const validationError = validateForm(formValues);

         if (validationError) {
            Status.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await submitClosedStatus(formValues);

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else {
               Status.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch (err) {
            Status.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
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
