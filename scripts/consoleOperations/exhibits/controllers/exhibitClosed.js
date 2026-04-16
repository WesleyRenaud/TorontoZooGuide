import { loadExhibits, setStatus, populateExhibitDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../shared/controllerUtils.js';

export function createExhibitClosedController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   exhibitEl,
   startDateEl,
   endDateEl,
   messageEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      resetFormFields([exhibitEl, startDateEl, endDateEl, messageEl]);
   }

   function show() {
      setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      hideConsolePanel({
         panelEl,
         statusEl,
         setStatus,
      });
   }

   async function onShowClick() {
      await loadOptionsAndShowPanel({
         statusEl,
         setStatus,
         loadOptions: loadExhibits,
         populateOptions: populateExhibitDropdown,
         targetEl: exhibitEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: 'Failed to load exhibits.',
      });
   }

   async function onSubmitClick() {
      const exhibit = exhibitEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!exhibit) {
         setStatus(statusEl, 'Exhibit is required.', 'is-error');
         return;
      }

      const dateError = validateOptionalDateRange(startDate, endDate);

      if (dateError) {
         setStatus(statusEl, dateError, 'is-error');
         return;
      }

      try {
         const result = await postJson('/set-exhibit-closed', {
            exhibit,
            startDate: startDate || null,
            endDate: endDate || null,
            message
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.exhibit} was set as closed.`,
               'is-success'
            );
            resetForm();
         }
         else {
            setStatus(statusEl, result.error || 'Failed.', 'is-error');
         }
      }
      catch(err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}
