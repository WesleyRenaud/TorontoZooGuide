import { loadWildEncounters, setStatus, populateWildEncounterDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

export function createEndWildEncounterScheduleController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   wildEncounterEl,
   endDateEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      if (wildEncounterEl) wildEncounterEl.value = '';
      if (endDateEl) endDateEl.value = '';
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
         if (wildEncounterEl?.tagName === 'SELECT') {
            const wildEncounters = await loadWildEncounters();
            populateWildEncounterDropdown(wildEncounterEl, wildEncounters);
         }

         resetForm();
         activatePanel?.(panelEl);
      }
      catch(err) {
         setStatus(statusEl, 'Failed to load Wild Encounters.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {
      const wildEncounter = wildEncounterEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!wildEncounter) {
         setStatus(statusEl, 'Wild Encounter is required.', 'is-error');
         return;
      }

      try {
         const result = await postJson('/end-wild-encounter-schedule', {
            wildEncounter,
            endDate: endDate || null
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.wildEncounter} schedule was ended.`,
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