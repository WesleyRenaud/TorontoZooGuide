import { loadAttractions, postJson, setStatus, populateAttractionDropdown } from '../utils.js';

export function createAttractionOpenController( {
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   attractionEl,
   activatePanel,
   hidePanels,
} = {} ) {

   function resetForm() {
      if(attractionEl) attractionEl.value = '';
   }

   function show() {
      setStatus(statusEl, '');
      activatePanel?.(panelEl);
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
         setStatus(statusEl, '');
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

      if(!attraction) {
         setStatus(statusEl, 'Attraction is required.', 'is-error');
         return;
      }

      try {
         const result = await postJson('/set-attraction-open', {
            attraction
         });

         if(result.success) {
            setStatus(
               statusEl,
               `${result.attraction} was set as open.`,
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