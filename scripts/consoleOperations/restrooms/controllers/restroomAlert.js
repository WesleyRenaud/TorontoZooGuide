import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class RestroomAlert {
   static createRestroomAlertController({
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


      function getFormValues() {
         return {
            restroom: ControllerUtils.getFieldValue(restroomEl),
            startDate: ControllerUtils.getFieldValue(startDateEl),
            endDate: ControllerUtils.getFieldValue(endDateEl),
            message: ControllerUtils.getFieldValue(messageEl),
         };
      }

      function validateForm({
         restroom,
         startDate,
         endDate,
         message,
      }) {
         if (!restroom) {
            return Strings.validation.entityRequired(Strings.entityLabels.restroom);
         }

         if (!message) {
            return Strings.validation.entityRequired(Strings.labels.alertMessage);
         }

         return ControllerUtils.validateOptionalDateRange(startDate, endDate);
      }

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
      }

      async function show() {
         await ControllerUtils.loadOptionsAndShowPanel({
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
            loadOptions: ConsoleOptionsLoader.loadRestrooms,
            populateOptions: ConsoleDropdownPopulator.populateRestroomDropdown,
            targetEl: restroomEl,
            resetForm,
            activatePanel,
            panelEl,
            errorMessage: Strings.loadErrors.restrooms,
         });
      }

      function hide() {
         ControllerUtils.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      async function submitRestroomAlert({
         restroom,
         startDate,
         endDate,
         message,
      }) {
         return ConsoleOperationsApi.setRestroomAlert({
            restroom,
            alertStartDate: startDate || null,
            alertEndDate: endDate || null,
            message,
         });
      }

      function handleSubmitSuccess(result) {
         ConsoleStatusPresenter.setStatus(
            statusEl,
            `${result.restroom} was given an alert.`,
            'is-success'
         );

         resetForm();
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
            const result = await submitRestroomAlert(formValues);

            if (result.success) {
               handleSubmitSuccess(result);
            }
            else {
               ConsoleStatusPresenter.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch(err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
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
}
