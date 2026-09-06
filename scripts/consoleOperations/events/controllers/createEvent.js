import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Status } from '../../shell/status.js';
import { Strings } from '../../../strings.js';
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
            name: ControllerUtils.getFieldValue(nameEl),
            location: ControllerUtils.getFieldValue(locationEl),
            description: ControllerUtils.getFieldValue(descriptionEl),
            link: ControllerUtils.getFieldValue(linkEl),
            startDate: VisitDateRules.resolveOptionalStartDate(ControllerUtils.getFieldValue(startDateEl)),
            endDate: ControllerUtils.getFieldValue(endDateEl),
         };
      }

      function validateForm(values) {
         if (!values.name) return Strings.validation.entityRequired(Strings.labels.name);
         if (!values.description) return Strings.validation.entityRequired(Strings.labels.description);
         if (!values.link) return Strings.validation.entityRequired(Strings.labels.link);

         return ControllerUtils.validateOptionalDateRange(values.startDate, values.endDate);
      }

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
      }

      function show() {
         Status.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      function hide() {
         ControllerUtils.hideConsolePanel({ panelEl, statusEl, setStatus: Status.setStatus });
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
                  Strings.status.eventCreated(result),
                  'is-success'
               );
               resetForm();
            }
            else {
               Status.setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
            }
         }
         catch (err) {
            Status.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      }

      showButtonEl?.addEventListener('click', show);
      cancelButtonEl?.addEventListener('click', hide);
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return { show, hide };
   }
}
