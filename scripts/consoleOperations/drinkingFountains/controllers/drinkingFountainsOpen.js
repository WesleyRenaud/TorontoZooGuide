import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ApiErrorMessageResolver } from '../../apiErrorMessageResolver.js';
import {
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { setStatus } from '../../shell/status.js';
import { APP_STRINGS } from '../../../strings.js';

export function createDrinkingFountainsOpenController({
   showButtonEl,
   panelEl,
   submitButtonEl,
   statusEl,
   startDateEl,
   endDateEl,
   activatePanel,
} = {}) {
   function resetForm() {
      resetFormFields([startDateEl, endDateEl]);
   }

   function show() {
      setStatus(statusEl, '');
      resetForm();
      activatePanel?.(panelEl);
   }

   async function onSubmitClick() {
      setStatus(statusEl, '');

      const startDate = startDateEl?.value.trim() || '';
      const endDate = endDateEl?.value.trim() || '';
      const validationError = validateOptionalDateRange(startDate, endDate);

      if (validationError) {
         setStatus(statusEl, validationError, 'is-error');
         return;
      }

      try {
         const result = await ConsoleOperationsApi.setDrinkingFountainsOpen({
            startDate: startDate || null,
            endDate: endDate || null,
         });

         if (result.success) {
            setStatus(statusEl, APP_STRINGS.status.drinkingFountainsOpen, 'is-success');
            resetForm();
         }
         else {
            setStatus(statusEl, ApiErrorMessageResolver.resolveConsoleMutationError(result), 'is-error');
         }
      }
      catch (err) {
         setStatus(statusEl, APP_STRINGS.common.requestFailed, 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', show);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return { show };
}
