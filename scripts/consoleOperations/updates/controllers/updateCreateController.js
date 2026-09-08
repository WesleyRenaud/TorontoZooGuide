import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class UpdateCreateController {
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
            title: ControllerHelper.getFieldValue(titleEl),
            description: ControllerHelper.getFieldValue(descriptionEl),
            type: ControllerHelper.getFieldValue(typeEl),
            startDate: ControllerHelper.getFieldValue(startDateEl),
            endDate: ControllerHelper.getFieldValue(endDateEl),
         };
      }

      function validateForm(values) {
         if (!values.title) return Strings.validation.entityRequired(Strings.labels.title);
         if (!values.description) return Strings.validation.entityRequired(Strings.labels.description);
         if (!values.type) return Strings.validation.entityRequired(Strings.labels.type);

         return ControllerHelper.validateOptionalDateRange(values.startDate, values.endDate);
      }

      function resetForm() {
         ControllerHelper.resetFormFields(formFieldEls);
      }

      function show() {
         ConsoleStatusPresenter.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      function hide() {
         ControllerHelper.hideConsolePanel({ panelEl, statusEl, setStatus: ConsoleStatusPresenter.setStatus });
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
            const result = await ConsoleOperationsClient.createUpdate(values);

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
