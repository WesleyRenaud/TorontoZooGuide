import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export class DrinkingFountainsClosed {
   static createDrinkingFountainsClosedController({
      showButtonEl,
      panelEl,
      submitButtonEl,
      statusEl,
      startDateEl,
      endDateEl,
      messageEl,
      activatePanel,
   } = {}) {
      function resetForm() {
         ControllerUtils.resetFormFields([startDateEl, endDateEl, messageEl]);
      }

      function show() {
         Status.setStatus(statusEl, '');
         resetForm();
         activatePanel?.(panelEl);
      }

      async function onSubmitClick() {
         Status.setStatus(statusEl, '');

         const startDate = ValueNormalizer.asTrimmedString(startDateEl?.value);
         const endDate = ValueNormalizer.asTrimmedString(endDateEl?.value);
         const validationError = ControllerUtils.validateOptionalDateRange(startDate, endDate);

         if (validationError) {
            Status.setStatus(statusEl, validationError, 'is-error');
            return;
         }

         try {
            const result = await ConsoleOperationsApi.setDrinkingFountainsClosed({
               startDate: startDate || null,
               endDate: endDate || null,
               message: ValueNormalizer.asTrimmedString(messageEl?.value),
            });

            if (result.success) {
               Status.setStatus(statusEl, APP_STRINGS.status.drinkingFountainsClosed, 'is-success');
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
      submitButtonEl?.addEventListener('click', onSubmitClick);

      return { show };
   }
}
