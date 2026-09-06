import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Status } from '../../shell/status.js';
import { Strings } from '../../../strings.js';

export class AddGuardiansTalkOccurrence {
   static createAddGuardiansTalkOccurrenceController({
      showButtonEl,
      panelEl,
      cancelButtonEl,
      submitButtonEl,
      statusEl,
      talkNameEl,
      locationEl,
      dateEl,
      timeEl,
      activatePanel,
      talkLocationFilterController = null,
   } = {}) {
      const formFieldEls = [locationEl, dateEl, timeEl];

      function resetForm() {
         ControllerUtils.resetFormFields(formFieldEls);
         talkLocationFilterController?.clear?.();
      }

      function getFormValues() {
         const time = ControllerUtils.getFieldValue(timeEl);

         return {
            talk: ControllerUtils.getFieldValue(talkNameEl),
            location: ControllerUtils.getFieldValue(locationEl),
            date: ControllerUtils.getFieldValue(dateEl),
            times: time ? [time] : [],
         };
      }

      function validateForm({ talk, location, date, times }) {
         const required = [
            [location, Strings.labels.location],
            [talk, Strings.labels.talkName],
            [date, Strings.labels.date],
            [times[0], Strings.labels.talkTime],
         ];

         for (const [value, label] of required) {
            if (!value) {
               return Strings.validation.entityRequired(label);
            }
         }

         return null;
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

      showButtonEl?.addEventListener('click', async () => {
         Status.setStatus(statusEl, '');

         try {
            resetForm();
            await talkLocationFilterController?.refreshLocations?.();
            show();
         }
         catch (err) {
            Status.setStatus(statusEl, Strings.loadErrors.locations, 'is-error');
            show();
         }
      });

      cancelButtonEl?.addEventListener('click', hide);

      submitButtonEl?.addEventListener('click', async () => {
         const formValues = getFormValues();

         Status.setStatus(statusEl, '');

         const validationError = validateForm(formValues);

         if (validationError) {
            Status.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsApi.addGuardiansTalkOccurrence(formValues);

            if (!result.success) {
               Status.setStatus(
                  statusEl,
                  ApiErrorMessageResolver.resolveConsoleMutationError(result),
                  'is-error'
               );
               return;
            }

            Status.setStatus(
               statusEl,
               `${result.talk} in ${result.location} on ${result.date} at ${result.times[0]} was added.`,
               'is-success'
            );
            resetForm();
         }
         catch (err) {
            Status.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      });

      return {
         show,
         hide,
      };
   }
}
