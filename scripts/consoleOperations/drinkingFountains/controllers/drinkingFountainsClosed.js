import { setDrinkingFountainsClosed } from '../../../api/consoleOperationsApi.js';
import {
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { resolveConsoleMutationError } from '../../resolveApiErrorMessage.js';
import { setStatus } from '../../shell/status.js';
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
         const result = await setDrinkingFountainsClosed({
            startDate: startDate || null,
            endDate: endDate || null,
            message: messageEl?.value.trim() || '',
         });

         if (result.success) {
            setStatus(statusEl, APP_STRINGS.status.drinkingFountainsClosed, 'is-success');
            resetForm();
         }
         else {
            setStatus(statusEl, resolveConsoleMutationError(result), 'is-error');
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
