import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import {
   getFieldValue,
   hideConsolePanel,
   resetFormFields,
} from '../helpers/controllerUtils.js';
import { Status } from '../shell/status.js';
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

   function validateForm(formValues) {
      return validateSelection?.(formValues) ?? null;
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
      Status.setStatus(statusEl, '');

      try {
         resetForm();
         await prepareForm?.();
         show();
      }
      catch (err) {
         Status.setStatus(statusEl, loadErrorMessage, 'is-error');
         show();
      }
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
         const result = await submitEndSchedule(formValues);

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
