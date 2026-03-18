import {
   postJson,
   setStatus,
   populateGuardiansTalkDropdown
} from '../../utils.js';

export function createEndGuardiansTalkScheduleController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   talkNameEl,
   locationEl,
   endDateEl,
   activatePanel,
   hidePanels,
   talkLocationFilterController = null,
} = {}) {

   function resetTalkDropdown() {
      if(talkLocationFilterController?.clear) {
         talkLocationFilterController.clear();
         return;
      }

      if(talkNameEl?.tagName === 'SELECT') {
         populateGuardiansTalkDropdown(talkNameEl, []);
      }
      else if(talkNameEl) {
         talkNameEl.value = '';
      }
   }

   function resetForm() {
      if(locationEl) locationEl.value = '';
      if(talkNameEl) talkNameEl.value = '';
      if(endDateEl) endDateEl.value = '';

      resetTalkDropdown();
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
         resetForm();

         if(talkLocationFilterController?.refreshLocations) {
            await talkLocationFilterController.refreshLocations();
         }

         setStatus(statusEl, '');
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
      const endDate = endDateEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if(!location) {
         setStatus(statusEl, 'Location is required.', 'is-error');
         return;
      }

      if(!talk) {
         setStatus(statusEl, 'Talk name is required.', 'is-error');
         return;
      }

      try {

         const result = await postJson('/end-guardians-talk-schedule', {
            talk,
            location,
            endDate: endDate || null
         });

         if(result.success) {
            setStatus(
               statusEl,
               `${result.talk} in ${result.location} schedule was ended.`,
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