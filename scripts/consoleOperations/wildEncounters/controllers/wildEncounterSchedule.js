import { loadWildEncounters, setStatus, populateWildEncounterDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';
import {
   hasCheckedField,
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../shared/controllerUtils.js';

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
      resetFormFields([
         wildEncounterEl,
         startDateEl,
         endDateEl,
         timeEl,
         messageEl,
         mondayEl,
         tuesdayEl,
         wednesdayEl,
         thursdayEl,
         fridayEl,
         saturdayEl,
         sundayEl,
      ]);
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

   function hasAtLeastOneDaySelected() {
      return hasCheckedField([
         mondayEl,
         tuesdayEl,
         wednesdayEl,
         thursdayEl,
         fridayEl,
         saturdayEl,
         sundayEl,
      ]);
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

      const dateError = validateOptionalDateRange(startDate, endDate);

      if (dateError) {
         setStatus(statusEl, dateError, 'is-error');
         return;
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
