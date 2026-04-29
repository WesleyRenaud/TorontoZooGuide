import { setDrinkingFountainsOpen } from '../../../api/consoleOperationsApi.js';
import {
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';
import { setStatus } from '../../shell/status.js';

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
         const result = await setDrinkingFountainsOpen({
            startDate: startDate || null,
            endDate: endDate || null,
         });

         if (result.success) {
            setStatus(statusEl, 'Drinking fountains were set as open.', 'is-success');
            resetForm();
         }
         else {
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }
      }
      catch (err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', show);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return { show };
}
