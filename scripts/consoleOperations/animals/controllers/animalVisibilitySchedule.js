import { loadExhibits, setStatus, populateExhibitDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

export function createAnimalVisibilityScheduleController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   speciesEl,
   exhibitEl,
   startDateEl,
   endDateEl,
   dailyStartTimeEl,
   dailyEndTimeEl,
   messageEl,
   activatePanel,
   hidePanels,
} = {}) {

   function resetForm() {
      if (speciesEl) speciesEl.value = '';
      if (exhibitEl) exhibitEl.value = '';
      if (startDateEl) startDateEl.value = '';
      if (endDateEl) endDateEl.value = '';
      if (dailyStartTimeEl) dailyStartTimeEl.value = '';
      if (dailyEndTimeEl) dailyEndTimeEl.value = '';
      if (messageEl) messageEl.value = '';
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
         activatePanel?.(panelEl);
      } catch (err) {
         setStatus(statusEl, 'Failed to load exhibits.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {

      const species = speciesEl?.value.trim() ?? '';
      const exhibit = exhibitEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const dailyStartTime = dailyStartTimeEl?.value.trim() ?? '';
      const dailyEndTime = dailyEndTimeEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!species) {
         setStatus(statusEl, 'Species name is required.', 'is-error');
         return;
      }

      if (!exhibit) {
         setStatus(statusEl, 'Exhibit is required.', 'is-error');
         return;
      }

      if (!dailyStartTime || !dailyEndTime) {
         setStatus(statusEl, 'Daily viewing start and end times are required.', 'is-error');
         return;
      }

      try {

         const result = await postJson('/set-animal-visibility-schedule', {
            species,
            exhibit,
            startDate: startDate || null,
            endDate: endDate || null,
            dailyStartTime,
            dailyEndTime,
            message
         });

         if (result.success) {

            setStatus(
               statusEl,
               `${result.species} in ${result.exhibit} viewing schedule updated.`,
               'is-success'
            );

            resetForm();

         } else {

            setStatus(statusEl, result.error || 'Failed.', 'is-error');

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

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };
}