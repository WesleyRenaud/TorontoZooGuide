import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
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
         ConsoleStatusPresenter.setStatus(statusEl, '');
         activatePanel?.(panelEl);
      }

      function hide() {
         ControllerUtils.hideConsolePanel({
            panelEl,
            statusEl,
            setStatus: ConsoleStatusPresenter.setStatus,
         });
      }

      showButtonEl?.addEventListener('click', async () => {
         ConsoleStatusPresenter.setStatus(statusEl, '');

         try {
            resetForm();
            await talkLocationFilterController?.refreshLocations?.();
            show();
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.loadErrors.locations, 'is-error');
            show();
         }
      });

      cancelButtonEl?.addEventListener('click', hide);

      submitButtonEl?.addEventListener('click', async () => {
         const formValues = getFormValues();

         ConsoleStatusPresenter.setStatus(statusEl, '');

         const validationError = validateForm(formValues);

         if (validationError) {
            ConsoleStatusPresenter.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsApi.addGuardiansTalkOccurrence(formValues);

            if (!result.success) {
               ConsoleStatusPresenter.setStatus(
                  statusEl,
                  ApiErrorMessageResolver.resolveConsoleMutationError(result),
                  'is-error'
               );
               return;
            }

            ConsoleStatusPresenter.setStatus(
               statusEl,
               `${result.talk} in ${result.location} on ${result.date} at ${result.times[0]} was added.`,
               'is-success'
            );
            resetForm();
         }
         catch (err) {
            ConsoleStatusPresenter.setStatus(statusEl, Strings.common.requestFailed, 'is-error');
         }
      });

      return {
         show,
         hide,
      };
   }
}
