import { setStatus, populateGuardiansTalkDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';
import {
   hasCheckedField,
   hideConsolePanel,
   resetFormFields,
   validateOptionalDateRange,
} from '../../shared/controllerUtils.js';

export function createGuardiansTalkScheduleController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   talkNameEl,
   locationEl,
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
   talkLocationFilterController = null,
} = {}) {

   function resetTalkDropdown() {
      if (talkLocationFilterController?.clear) {
         talkLocationFilterController.clear();
         return;
      }

      if (talkNameEl?.tagName === 'SELECT') {
         populateGuardiansTalkDropdown(talkNameEl, []);
      }
      else if (talkNameEl) {
         talkNameEl.value = '';
      }
   }

   function resetForm() {
      resetFormFields([
         locationEl,
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

      resetTalkDropdown();
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
         resetForm();

         if (talkLocationFilterController?.refreshLocations) {
            await talkLocationFilterController.refreshLocations();
         }

         activatePanel?.(panelEl);
      }
      catch(err) {
         setStatus(statusEl, 'Failed to load locations.', 'is-error');
         activatePanel?.(panelEl);
      }
   }

   async function onSubmitClick() {
      const talk = talkNameEl?.value.trim() ?? '';
      const location = locationEl?.value.trim() ?? '';
      const startDate = startDateEl?.value.trim() ?? '';
      const endDate = endDateEl?.value.trim() ?? '';
      const time = timeEl?.value.trim() ?? '';
      const message = messageEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!location) {
         setStatus(statusEl, 'Location is required.', 'is-error');
         return;
      }

      if (!talk) {
         setStatus(statusEl, 'Talk name is required.', 'is-error');
         return;
      }

      if (!time) {
         setStatus(statusEl, 'Talk time is required.', 'is-error');
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
         const result = await postJson('/set-guardians-talk-schedule', {
            talk,
            location,
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
               `${result.talk} in ${result.location} schedule was saved.`,
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
