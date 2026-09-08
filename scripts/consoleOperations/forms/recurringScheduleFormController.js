import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
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
         ControllerHelper.resetFormFields(recurringFieldEls);
         resetScheduleTimes?.();
         resetSelection?.();
      }

      function getFormValues() {
         const formValues = {
            ...(typeof getSelectionValues === 'function'
               ? getSelectionValues()
               : {}),
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
            message: ControllerHelper.getFieldValue(messageEl),
         };

         if (getScheduleTimes) {
            formValues.times = getScheduleTimes();
         }
         else {
            formValues.time = ControllerHelper.getFieldValue(timeEl);
         }

         return formValues;
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

         if (!validateRecurringSchedule && !ControllerHelper.hasCheckedField(dayFieldEls)) {
            return noDaysSelectedMessage;
         }

         return ControllerHelper.validateOptionalDateRange(
            formValues.startDate,
            formValues.endDate
         );
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
         ConsoleStatusPresenter.setStatus(statusEl, '');

         try {
            resetForm();
            await prepareForm?.();
            show();
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, loadErrorMessage, 'is-error');
            show();
         }
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
            const result = await submitSchedule(formValues);

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else if (shouldReportSubmitFailure?.(result) ?? true) {
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
