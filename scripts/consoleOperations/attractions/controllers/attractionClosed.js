import { loadAttractions } from '../../options/loaders.js';
import { populateAttractionDropdown } from '../../options/dropdowns.js';
import { setStatus } from '../../shell/status.js';
import { setAttractionClosed } from '../../../api/consoleOperationsApi.js';
import {
   hideConsolePanel,
   loadOptionsAndShowPanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../helpers/controllerUtils.js';

export function createAttractionClosedController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   attractionEl,
   startDateEl,
   endDateEl,
   messageEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      resetFormFields([attractionEl, startDateEl, endDateEl, messageEl]);
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
         loadOptions: loadAttractions,
         populateOptions: populateAttractionDropdown,
         targetEl: attractionEl,
         resetForm,
         activatePanel,
         panelEl,
         errorMessage: 'Failed to load attractions.',
      });
   }

   async function onSubmitClick() {
      const attraction = attractionEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!attraction) {
         setStatus(statusEl, 'Attraction is required.', 'is-error');
         return;
      }

      const dateError = validateOptionalDateRange(startDate, endDate);

      if (dateError) {
         setStatus(statusEl, dateError, 'is-error');
         return;
      }

      try {
         const result = await setAttractionClosed({
            attraction,
            startDate: startDate || null,
            endDate: endDate || null,
            message
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.attraction} was set as closed.`,
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
