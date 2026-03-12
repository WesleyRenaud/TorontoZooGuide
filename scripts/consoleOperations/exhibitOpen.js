import { loadExhibits, postJson, setStatus, populateExhibitDropdown } from './utils.js';

export function createExhibitOpenController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   exhibitEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      if (exhibitEl) exhibitEl.value = '';
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
         const exhibits = await loadExhibits();
         populateExhibitDropdown(exhibitEl, exhibits);
         resetForm();
         setStatus(statusEl, '');
         activatePanel?.(panelEl);
      }
      catch (err) {
         setStatus(statusEl, 'Failed to load exhibits.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {
      const exhibit = exhibitEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!exhibit) {
         setStatus(statusEl, 'Exhibit is required.', 'is-error');
         return;
      }

      try {
         const result = await postJson('/set-exhibit-open', {
            exhibit
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.exhibit} was set as open.`,
               'is-success'
            );
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

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}