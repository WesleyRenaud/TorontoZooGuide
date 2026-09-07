import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class CreateUpdate {
   static createCreateUpdateController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      titleEl,
      descriptionEl,
      typeEl,
      startDateEl,
      endDateEl,
      activatePanel,
   } = {}) {
      const formFieldEls = [titleEl, descriptionEl, typeEl, startDateEl, endDateEl];


      function getFormValues() {
         return {
            title: ControllerUtils.getFieldValue(titleEl),
            description: ControllerUtils.getFieldValue(descriptionEl),
            type: ControllerUtils.getFieldValue(typeEl),
            startDate: ControllerUtils.getFieldValue(startDateEl),
            endDate: ControllerUtils.getFieldValue(endDateEl),
         };
      }

      function validateForm(values) {
         if (!values.title) return Strings.validation.entityRequired(Strings.labels.title);
         if (!values.description) return Strings.validation.entityRequired(Strings.labels.description);
         if (!values.type) return Strings.validation.entityRequired(Strings.labels.type);

         return ControllerUtils.validateOptionalDateRange(values.startDate, values.endDate);
      }

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
      }

      function show() {
         ConsoleStatusPresenter.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      function hide() {
         ControllerUtils.hideConsolePanel({ panelEl, statusEl, setStatus: ConsoleStatusPresenter.setStatus });
      }

      async function onSubmitClick() {
         const values = getFormValues();
         const validationError = validateForm(values);

         ConsoleStatusPresenter.setStatus(statusEl, '');

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsApi.createUpdate(values);

            if (result.success) {
               ConsoleStatusPresenter.setStatus(
                  statusEl,
                  Strings.status.updateCreated(result),
                  'is-success'
               );
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
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return { show, hide };
   }
}
