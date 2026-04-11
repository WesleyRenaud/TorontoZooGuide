import { loadWildEncounters, setStatus, populateWildEncounterDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

export function createWildEncounterScheduleController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   wildEncounterEl,
   startDateEl,
   endDateEl,
   timeEl,
   mondayEl,
   tuesdayEl,
   wednesdayEl,
   thursdayEl,
   fridayEl,
   saturdayEl,
   sundayEl,
   messageEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      if (wildEncounterEl) wildEncounterEl.value = '';
      if (startDateEl) startDateEl.value = '';
      if (endDateEl) endDateEl.value = '';
      if (timeEl) timeEl.value = '';
      if (messageEl) messageEl.value = '';

      if (mondayEl) mondayEl.checked = false;
      if (tuesdayEl) tuesdayEl.checked = false;
      if (wednesdayEl) wednesdayEl.checked = false;
      if (thursdayEl) thursdayEl.checked = false;
      if (fridayEl) fridayEl.checked = false;
      if (saturdayEl) saturdayEl.checked = false;
      if (sundayEl) sundayEl.checked = false;
   }

   function show() {
      setStatus(statusEl, '');
      activatePanel?.(panelEl);
   }

   function hide() {
      panelEl?.classList.remove('active');
      setStatus(statusEl, '');
   }

   function hasAtLeastOneDaySelected() {
      return Boolean(
         mondayEl?.checked
         || tuesdayEl?.checked
         || wednesdayEl?.checked
         || thursdayEl?.checked
         || fridayEl?.checked
         || saturdayEl?.checked
         || sundayEl?.checked
      );
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
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const time = timeEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!wildEncounter) {
         setStatus(statusEl, 'Wild Encounter is required.', 'is-error');
         return;
      }

      if (!time) {
         setStatus(statusEl, 'Encounter time is required.', 'is-error');
         return;
      }

      if (!hasAtLeastOneDaySelected()) {
         setStatus(statusEl, 'At least one day must be selected.', 'is-error');
         return;
      }

      const effectiveStart = startDate || new Date().toISOString().split('T')[0];

      if (endDate) {
         const startMs = new Date(effectiveStart).getTime();
         const endMs = new Date(endDate).getTime();

         if (Number.isNaN(startMs) || Number.isNaN(endMs)) {
            setStatus(statusEl, 'Invalid start or end date.', 'is-error');
            return;
         }

         if (endMs < startMs) {
            setStatus(statusEl, 'End date cannot be before the start date.', 'is-error');
            return;
         }
      }

      try {
         const result = await postJson('/set-wild-encounter-schedule', {
            wildEncounter,
            startDate: startDate || null,
            endDate: endDate || null,
            time,
            monday: Boolean(mondayEl?.checked),
            tuesday: Boolean(tuesdayEl?.checked),
            wednesday: Boolean(wednesdayEl?.checked),
            thursday: Boolean(thursdayEl?.checked),
            friday: Boolean(fridayEl?.checked),
            saturday: Boolean(saturdayEl?.checked),
            sunday: Boolean(sundayEl?.checked),
            message
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.wildEncounter} schedule was saved.`,
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
