import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import {
   getFieldValue,
   hideConsolePanel,
   resetFormFields,
} from '../../helpers/controllerUtils.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

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
         resetFormFields(formFieldEls);
         talkLocationFilterController?.clear?.();
      }

      function getFormValues() {
         const time = getFieldValue(timeEl);

         return {
            talk: getFieldValue(talkNameEl),
            location: getFieldValue(locationEl),
            date: getFieldValue(dateEl),
            times: time ? [time] : [],
         };
      }

      function validateForm({ talk, location, date, times }) {
         const required = [
            [location, APP_STRINGS.labels.location],
            [talk, APP_STRINGS.labels.talkName],
            [date, APP_STRINGS.labels.date],
            [times[0], APP_STRINGS.labels.talkTime],
         ];

         for (const [value, label] of required) {
            if (!value) {
               return APP_STRINGS.validation.entityRequired(label);
            }
         }

         return null;
      }

      function show() {
         Status.setStatus(statusEl, '');
         activatePanel?.(panelEl);
      }

      function hide() {
         hideConsolePanel({
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
            Status.setStatus(statusEl, APP_STRINGS.loadErrors.locations, 'is-error');
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
            Status.setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
         }
      });

      return {
         show,
         hide,
      };
   }
}
