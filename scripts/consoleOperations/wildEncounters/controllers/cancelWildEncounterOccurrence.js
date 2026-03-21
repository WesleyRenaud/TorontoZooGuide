import {
   loadWildEncounters,
   postJson,
   setStatus,
   populateWildEncounterDropdown
} from '../../utils.js';

export function createCancelWildEncounterOccurrenceController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   wildEncounterEl,
   dateEl,
   timeEl,
   activatePanel,
   hidePanels,
   occurrenceFilterController = null,
} = {}) {

   function resetOccurrenceDropdowns() {
      if (occurrenceFilterController?.clear) {
         occurrenceFilterController.clear();
      }
      else {
         if (dateEl) dateEl.value = '';
         if (timeEl) timeEl.value = '';
      }
   }

   function resetForm() {
      if (wildEncounterEl) wildEncounterEl.value = '';
      if (dateEl) dateEl.value = '';
      if (timeEl) timeEl.value = '';

      resetOccurrenceDropdowns();
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
      const date = dateEl?.value.trim() ?? '';
      const time = timeEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!wildEncounter) {
         setStatus(statusEl, 'Wild Encounter is required.', 'is-error');
         return;
      }

      if (!date) {
         setStatus(statusEl, 'Date is required.', 'is-error');
         return;
      }

      if (!time) {
         setStatus(statusEl, 'Time is required.', 'is-error');
         return;
      }

      try {
         const result = await postJson('/cancel-wild-encounter-occurrence', {
            wildEncounter,
            date,
            time
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.wildEncounter} on ${result.date} at ${result.time} was cancelled.`,
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

   wildEncounterEl?.addEventListener('change', async () => {
      if (dateEl) dateEl.value = '';
      if (timeEl) timeEl.value = '';

      if (occurrenceFilterController?.refresh) {
         await occurrenceFilterController.refresh();
      }
   });

   dateEl?.addEventListener('change', () => {
      if (timeEl) timeEl.value = '';

      if (occurrenceFilterController?.refreshTimes) {
         occurrenceFilterController.refreshTimes();
      }
   });

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}