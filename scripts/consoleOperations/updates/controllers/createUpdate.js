import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import {
   getFieldValue,
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

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
            title: getFieldValue(titleEl),
            description: getFieldValue(descriptionEl),
            type: getFieldValue(typeEl),
            startDate: getFieldValue(startDateEl),
            endDate: getFieldValue(endDateEl),
         };
      }

      function validateForm(values) {
         if (!values.title) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.title);
         if (!values.description) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.description);
         if (!values.type) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.type);

         return validateOptionalDateRange(values.startDate, values.endDate);
      }

      function resetForm() {
         resetFormFields(formFieldEls);
      }

      function show() {
         Status.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      function hide() {
         hideConsolePanel({ panelEl, statusEl, setStatus: Status.setStatus });
      }

      async function onSubmitClick() {
         const values = getFormValues();
         const validationError = validateForm(values);

         Status.setStatus(statusEl, '');

         if (validationError) {
            Status.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsApi.createUpdate(values);

            if (result.success) {
               Status.setStatus(
                  statusEl,
                  APP_STRINGS.status.updateCreated(result),
                  'is-success'
               );
               resetForm();
            }
            else {
               Status.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch (err) {
            Status.setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
         }
      }

      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return { show, hide };
   }
}
