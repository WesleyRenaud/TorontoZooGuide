import { setStatus } from '../shell/status.js';
import { APP_STRINGS } from '../../strings.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../helpers/controllerUtils.js';

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

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

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
      setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         successMessage(result),
         'is-success'
      );

      resetForm();
   }

   async function onShowClick() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus,
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

      setStatus(statusEl, '');

      const validationError = validateForm(formValues);

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await submitOpenStatus(formValues);

         if (result.success) {
            handleSubmitSuccess(result);
         }
         else {
            setStatus(statusEl, result.error || APP_STRINGS.common.genericFailed, 'is-error');
         }
      }
      catch (err) {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
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
