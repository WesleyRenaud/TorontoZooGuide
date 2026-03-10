import { loadExhibits, postJson, setStatus, populateExhibitDropdown } from './utils.js';

export function createAnimalOnDisplayController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   speciesEl,
   exhibitEl,
   activatePanel,
} = {}) {

   function resetForm() {
      if (speciesEl) speciesEl.value = '';
      if (exhibitEl) exhibitEl.value = '';
   }

   function hide() {
      panelEl?.classList.remove('active');
      setStatus(statusEl, '');
   }

   async function show() {
      setStatus(statusEl, '');

      try {
         const exhibits = await loadExhibits();
         populateExhibitDropdown(exhibitEl, exhibits);
         resetForm();
         activatePanel?.(panelEl);
      } catch (err) {
         setStatus(statusEl, 'Failed to load exhibits.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {
      const species = speciesEl?.value.trim() ?? '';
      const exhibit = exhibitEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!species) {
         setStatus(statusEl, 'Species name is required.', 'is-error');
         return;
      }

      if (!exhibit) {
         setStatus(statusEl, 'Exhibit is required.', 'is-error');
         return;
      }

      try {
         const result = await postJson('/set-animal-on-display', {
            species,
            exhibit
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.species} in ${result.exhibit} was set as on display.`,
               'is-success'
            );
            resetForm();
         } else {
            setStatus(
               statusEl,
               result.error || 'Failed.',
               'is-error'
            );
         }

      } catch (err) {
         setStatus(statusEl, 'Request failed.', 'is-error');
      }
   }

   exhibitEl?.addEventListener('change', () => {
      if (speciesEl) {
         speciesEl.value = '';
      }
   });

   showButtonEl?.addEventListener('click', show);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}