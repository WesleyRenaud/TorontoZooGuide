import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import {
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { Status } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export function createDrinkingFountainsClosedController({
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
      resetFormFields([startDateEl, endDateEl, messageEl]);
   }

   function show() {
      Status.setStatus(statusEl, '');
      resetForm();
      activatePanel?.(panelEl);
   }

   async function onSubmitClick() {
      Status.setStatus(statusEl, '');

      const startDate = startDateEl?.value.trim() || '';
      const endDate = endDateEl?.value.trim() || '';
      const validationError = validateOptionalDateRange(startDate, endDate);

      if (validationError) {
         Status.setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await ConsoleOperationsApi.setDrinkingFountainsClosed({
            startDate: startDate || null,
            endDate: endDate || null,
            message: messageEl?.value.trim() || '',
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
