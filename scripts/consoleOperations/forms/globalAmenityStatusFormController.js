import { ApiErrorMessageResolver } from '../apiErrorMessageResolver.js';
import { ControllerHelper } from '../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../shell/consoleStatusPresenter.js';
import { Strings } from '../../strings.js';

export class GlobalAmenityStatusFormController {
   static createGlobalAmenityStatusFormController({
      showButtonEl,
      panelEl,
      submitButtonEl,
      statusEl,
      startDateEl,
      endDateEl,
      messageEl = null,
      includeDateRange = true,
      activatePanel,
      submitStatus,
      successMessage,
      requireMessage = false,
   } = {}) {
      const formFieldEls = includeDateRange
         ? [startDateEl, endDateEl, messageEl]
         : [messageEl];

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
      }

      function getFormValues() {
         if (!includeDateRange) {
            return {
               message: ControllerHelper.getFieldValue(messageEl),
            };
         }

         return {
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
            message: ControllerHelper.getFieldValue(messageEl),
         };
      }

      function validateForm({ startDate, endDate, message }) {
         if (requireMessage && !message) {
            return Strings.validation.entityRequired(Strings.labels.message);
         }

         if (!includeDateRange) {
            return null;
         }

         return ControllerHelper.validateOptionalDateRange(startDate, endDate);
      }

      function resolveSuccessMessage(result) {
         return typeof successMessage === 'function'
            ? successMessage(result)
            : successMessage;
      }

      function show() {
         ConsoleStatusPresenter.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      async function onSubmitClick() {
         ConsoleStatusPresenter.setStatus(statusEl, '');

         const formValues = getFormValues();
         const validationError = validateForm(formValues);

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await submitStatus(formValues);

            if (result.success) {
               ConsoleStatusPresenter.setStatus(statusEl, resolveSuccessMessage(result), 'is-success');
               resetForm();
            }
            else {
               ConsoleStatusPresenter.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      showButtonEl?.addEventListener('click', show);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return { show };
   }
}
