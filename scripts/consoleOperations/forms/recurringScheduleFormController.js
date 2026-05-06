import {
   hasCheckedField,
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../helpers/controllerUtils.js';
import { setStatus } from '../shell/status.js';
import { APP_STRINGS } from '../../strings.js';

export function createRecurringScheduleFormController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   startDateEl,
   endDateEl,
   timeEl,
   messageEl,
   dayFieldEls = [],
   activatePanel,
   resetSelection = null,
   getSelectionValues,
   validateSelection = null,
   prepareForm = null,
   loadErrorMessage = APP_STRINGS.loadErrors.options,
   submitSchedule,
   successMessage = () => APP_STRINGS.status.scheduleWasSaved,
   timeRequiredMessage = APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.time),
   noDaysSelectedMessage = APP_STRINGS.validation.oneDay,
} = {}) {
   const recurringFieldEls = [
      startDateEl,
      endDateEl,
      timeEl,
      messageEl,
      ...dayFieldEls,
   ];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function resetForm() {
      resetFormFields(recurringFieldEls);
      resetSelection?.();
   }

   function getFormValues() {
      return {
         ...(typeof getSelectionValues === 'function'
            ? getSelectionValues()
            : {}),
         startDate: getFieldValue(startDateEl),
         endDate: getFieldValue(endDateEl),
         time: getFieldValue(timeEl),
         message: getFieldValue(messageEl),
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
      const selectionError = validateSelection?.(formValues);

      if (selectionError) {
         return selectionError;
      }

      if (!formValues.time) {
         return timeRequiredMessage;
      }

      if (!hasCheckedField(dayFieldEls)) {
         return noDaysSelectedMessage;
      }

      return validateOptionalDateRange(
         formValues.startDate,
         formValues.endDate
      );
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
         const result = await submitSchedule(formValues);

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
