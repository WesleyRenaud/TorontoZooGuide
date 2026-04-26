import { setRestroomAlert } from '../../../api/consoleOperationsApi.js';
import {
   loadRestrooms,
} from '../../options/loaders.js';
import {
   populateRestroomDropdown,
} from '../../options/dropdowns.js';
import { setStatus } from '../../shell/status.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';

export function createRestroomAlertController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   restroomEl,
   startDateEl,
   endDateEl,
   messageEl,
   activatePanel,
} = {}) {
   const formFieldEls = [restroomEl, startDateEl, endDateEl, messageEl];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function getFormValues() {
      return {
         restroom: getFieldValue(restroomEl),
         startDate: getFieldValue(startDateEl),
         endDate: getFieldValue(endDateEl),
         message: getFieldValue(messageEl),
      };
   }

   function validateForm({
      restroom,
      startDate,
      endDate,
      message,
   }) {
      if (!restroom) {
         return 'Restroom is required.';
      }

      if (!message) {
         return 'Alert message is required.';
      }

      return validateOptionalDateRange(startDate, endDate);
   }

   function resetForm() {
      resetFormFields(formFieldEls);
   }

   async function show() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus,
         loadOptions: loadRestrooms,
         populateOptions: populateRestroomDropdown,
         targetEl: restroomEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: 'Failed to load restrooms.',
      });
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function submitRestroomAlert({
      restroom,
      startDate,
      endDate,
      message,
   }) {
      return setRestroomAlert({
         restroom,
         alertStartDate: startDate || null,
         alertEndDate: endDate || null,
         message,
      });
   }

   function handleSubmitSuccess(result) {
      setStatus(
         statusEl,
         `${result.restroom} was given an alert.`,
         'is-success'
      );

      resetForm();
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
         const result = await submitRestroomAlert(formValues);

         if (result.success) {
            handleSubmitSuccess(result);
         }
         else {
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }
      }
      catch(err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', show);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
