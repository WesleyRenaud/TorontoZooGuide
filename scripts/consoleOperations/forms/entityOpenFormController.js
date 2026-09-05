import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import {
   getFieldValue,
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../helpers/controllerUtils.js';
import { Status } from '../shell/status.js';
import { APP_STRINGS } from '../../strings.js';

export function createEntityOpenFormController({
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
   entityLabel = APP_STRINGS.entityLabels.item,
   optionsLabel = APP_STRINGS.entityLabels.items,
   loadErrorMessage = APP_STRINGS.loadErrors.entityOptions(optionsLabel),
   successMessage = () => APP_STRINGS.status.open(entityLabel),
} = {}) {
   const formFieldEls = [entityEl, startDateEl, endDateEl];
   const hasDateRange = Boolean(startDateEl || endDateEl);


   function getFormValues() {
      return {
         entity: getFieldValue(entityEl),
         startDate: getFieldValue(startDateEl),
         endDate: getFieldValue(endDateEl),
      };
   }

   function validateForm({ entity, startDate, endDate }) {
      if (!entity) {
         return APP_STRINGS.validation.entityRequired(entityLabel);
      }

      if (!hasDateRange) {
         return null;
      }

      return validateOptionalDateRange(startDate, endDate);
   }

   function resetForm() {
      resetFormFields(formFieldEls);
   }

   function show() {
      Status.setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      hideConsolePanel({
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
      await loadOptionsAndShowPanel({
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
         const result = await submitOpenStatus(formValues);

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

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
