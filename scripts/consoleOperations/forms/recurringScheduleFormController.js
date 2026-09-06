import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerUtils } from '../helpers/controllerUtils.js';
import { Status } from '../shell/status.js';
import { Strings } from '../../strings.js';

export class RecurringScheduleFormController {
   static createRecurringScheduleFormController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      startDateEl,
      endDateEl,
      timeEl,
      getScheduleTimes = null,
      resetScheduleTimes = null,
      messageEl,
      dayFieldEls = [],
      activatePanel,
      resetSelection = null,
      getSelectionValues,
      validateSelection = null,
      prepareForm = null,
      loadErrorMessage = Strings.loadErrors.options,
      submitSchedule,
      successMessage = () => Strings.status.scheduleWasSaved,
      shouldReportSubmitFailure = null,
      timeRequiredMessage = Strings.validation.entityRequired(Strings.labels.time),
      noDaysSelectedMessage = Strings.validation.oneDay,
      validateRecurringSchedule = null,
   } = {}) {
      const recurringFieldEls = [
         startDateEl,
         endDateEl,
         timeEl,
         messageEl,
         ...dayFieldEls,
      ];


      function resetForm() {
         ControllerUtils.resetFormFields(recurringFieldEls);
         resetScheduleTimes?.();
         resetSelection?.();
      }

      function getFormValues() {
         const formValues = {
            ...(typeof getSelectionValues === 'function'
               ? getSelectionValues()
               : {}),
            startDate: ControllerUtils.getFieldValue(startDateEl),
            endDate: ControllerUtils.getFieldValue(endDateEl),
            message: ControllerUtils.getFieldValue(messageEl),
         };

         if (getScheduleTimes) {
            formValues.times = getScheduleTimes();
         }
         else {
            formValues.time = ControllerUtils.getFieldValue(timeEl);
         }

         return formValues;
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

      function validateForm(formValues) {
         const selectionError = validateSelection?.(formValues);

         if (selectionError) {
            return selectionError;
         }

         if (validateRecurringSchedule) {
            const recurringScheduleError = validateRecurringSchedule(formValues);

            if (recurringScheduleError) {
               return recurringScheduleError;
            }
         }
         else if (getScheduleTimes) {
            if (!formValues.times?.length) {
               return timeRequiredMessage;
            }
         }
         else if (!formValues.time) {
            return timeRequiredMessage;
         }

         if (!validateRecurringSchedule && !ControllerUtils.hasCheckedField(dayFieldEls)) {
            return noDaysSelectedMessage;
         }

         return ControllerUtils.validateOptionalDateRange(
            formValues.startDate,
            formValues.endDate
         );
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
            const result = await submitSchedule(formValues);

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else if (shouldReportSubmitFailure?.(result) ?? true) {
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
