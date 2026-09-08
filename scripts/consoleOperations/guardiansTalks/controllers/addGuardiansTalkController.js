import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleStatusPresenter } from '../../shell/consoleStatusPresenter.js';
import { Strings } from '../../../strings.js';

export class AddGuardiansTalkController {
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
         ControllerHelper.resetFormFields(formFieldEls);
         talkLocationFilterController?.clear?.();
      }

      function getFormValues() {
         const time = ControllerHelper.getFieldValue(timeEl);

         return {
            talk: ControllerHelper.getFieldValue(talkNameEl),
            location: ControllerHelper.getFieldValue(locationEl),
            date: ControllerHelper.getFieldValue(dateEl),
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
         ControllerHelper.hideConsolePanel({
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
            const result = await ConsoleOperationsClient.addGuardiansTalkOccurrence(formValues);

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
