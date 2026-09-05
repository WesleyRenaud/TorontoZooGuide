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
import { VisitDateRules } from '../../../visitDates/visitDateRules.js';

export class CreateEvent {
   static createCreateEventController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      nameEl,
      locationEl,
      descriptionEl,
      linkEl,
      startDateEl,
      endDateEl,
      activatePanel,
   } = {}) {
      const formFieldEls = [nameEl, locationEl, descriptionEl, linkEl, startDateEl, endDateEl];

      function getFormValues() {
         return {
            name: getFieldValue(nameEl),
            location: getFieldValue(locationEl),
            description: getFieldValue(descriptionEl),
            link: getFieldValue(linkEl),
            startDate: VisitDateRules.resolveOptionalStartDate(getFieldValue(startDateEl)),
            endDate: getFieldValue(endDateEl),
         };
      }

      function validateForm(values) {
         if (!values.name) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.name);
         if (!values.description) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.description);
         if (!values.link) return APP_STRINGS.validation.entityRequired(APP_STRINGS.labels.link);

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
            const result = await ConsoleOperationsApi.createEvent(values);

            if (result.success) {
               Status.setStatus(
                  statusEl,
                  APP_STRINGS.status.eventCreated(result),
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
