import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';
import { VisitDateValidator } from '../../../visitDates/visitDateValidator.js';

export class EventController {
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
            name: ControllerHelper.getFieldValue(nameEl),
            location: ControllerHelper.getFieldValue(locationEl),
            description: ControllerHelper.getFieldValue(descriptionEl),
            link: ControllerHelper.getFieldValue(linkEl),
            startDate: VisitDateValidator.resolveOptionalStartDate(ControllerHelper.getFieldValue(startDateEl)),
            endDate: ControllerHelper.getFieldValue(endDateEl),
         };
      }

      function validateForm(values) {
         if (!values.name) return Strings.validation.entityRequired(Strings.labels.name);
         if (!values.description) return Strings.validation.entityRequired(Strings.labels.description);
         if (!values.link) return Strings.validation.entityRequired(Strings.labels.link);

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
            const result = await ConsoleOperationsClient.createEvent(values);

            if (result.success) {
               ConsoleStatusPresenter.setStatus(
                  statusEl,
                  Strings.status.eventCreated(result),
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
