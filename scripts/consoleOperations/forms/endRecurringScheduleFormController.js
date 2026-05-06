import {
   hideConsolePanel,
   resetFormFields,
} from '../helpers/controllerUtils.js';
import { setStatus } from '../shell/status.js';
import { APP_STRINGS } from '../../strings.js';

export function createEndRecurringScheduleFormController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   endDateEl,
   activatePanel,
   resetSelection = null,
   getSelectionValues,
   validateSelection = null,
   prepareForm = null,
   loadErrorMessage = APP_STRINGS.loadErrors.options,
   submitEndSchedule,
   successMessage = () => APP_STRINGS.status.scheduleWasEnded,
} = {}) {
   const formFieldEls = [endDateEl];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function resetForm() {
      resetFormFields(formFieldEls);
      resetSelection?.();
   }

   function getFormValues() {
      return {
         ...(typeof getSelectionValues === 'function'
            ? getSelectionValues()
            : {}),
         endDate: getFieldValue(endDateEl),
      };
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

   function validateForm(formValues) {
      return validateSelection?.(formValues) ?? null;
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
      setStatus(statusEl, '');

      try {
         resetForm();
         await prepareForm?.();
         show();
      }
      catch (err) {
         setStatus(statusEl, loadErrorMessage, 'is-error');
         show();
      }
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
         const result = await submitEndSchedule(formValues);

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
