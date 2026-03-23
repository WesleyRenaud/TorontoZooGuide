import { loadAttractions, setStatus, populateAttractionDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

export function createRemoveAttractionOpeningScheduleController({
   showButtonEl,
   panelEl,
   submitButtonEl,
   statusEl,
   attractionEl,
   activatePanel,
   hidePanels
} = {}) {

   function resetForm() {
      if (attractionEl) attractionEl.value = '';
   }

   function hide() {
      panelEl?.classList.remove('active');
      setStatus(statusEl, '');
   }

   async function onShowClick() {

      setStatus(statusEl, '');

      try {
         const attractions = await loadAttractions();
         populateAttractionDropdown(attractionEl, attractions);
         resetForm();
         activatePanel?.(panelEl);
      }
      catch(err) {
         setStatus(statusEl, 'Failed to load attractions.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {

      const attraction = attractionEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!attraction) {
         setStatus(statusEl, 'Attraction is required.', 'is-error');
         return;
      }

      try {

         const result = await postJson('/remove-attraction-opening-schedule', {
            attraction
         });

         if (result.success) {

            setStatus(
               statusEl,
               `${result.attraction} opening schedule was removed.`,
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
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      hide
   };

}