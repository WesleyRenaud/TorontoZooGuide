import { setStatus, populateGuardiansTalkDropdown } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

export function createCancelGuardiansTalkOccurrenceController({
   showButtonEl,
   panelEl,
   cancelButtonEl,
   submitButtonEl,
   statusEl,
   talkNameEl,
   locationEl,
   dateEl,
   timeEl,
   activatePanel,
   hidePanels,
   talkLocationFilterController = null,
} = {}) {

   let occurrences = [];

   function populateDateDropdown(occurrenceDates) {
      if (dateEl?.tagName !== 'SELECT') {
         return;
      }

      dateEl.innerHTML = '';

      const placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = 'Select a date';
      dateEl.appendChild(placeholder);

      occurrenceDates.forEach(date => {
         const option = document.createElement('option');
         option.value = date;
         option.textContent = date;
         dateEl.appendChild(option);
      });
   }

   function populateTimeDropdown(occurrenceTimes) {
      if (timeEl?.tagName !== 'SELECT') {
         return;
      }

      timeEl.innerHTML = '';

      const placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = 'Select a time';
      timeEl.appendChild(placeholder);

      occurrenceTimes.forEach(time => {
         const option = document.createElement('option');
         option.value = time;
         option.textContent = time;
         timeEl.appendChild(option);
      });
   }

   function clearOccurrenceDropdowns() {
      occurrences = [];
      populateDateDropdown([]);
      populateTimeDropdown([]);
   }

   function resetTalkDropdown() {
      if (talkLocationFilterController?.clear) {
         talkLocationFilterController.clear();
      }
      else if (talkNameEl?.tagName === 'SELECT') {
         populateGuardiansTalkDropdown(talkNameEl, []);
      }
      else if (talkNameEl) {
         talkNameEl.value = '';
      }

      clearOccurrenceDropdowns();
   }

   function resetForm() {
      if (locationEl) locationEl.value = '';
      if (talkNameEl) talkNameEl.value = '';
      if (dateEl) dateEl.value = '';
      if (timeEl) timeEl.value = '';

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

   async function loadOccurrencesForSelectedTalk() {
      const talk = talkNameEl?.value.trim() ?? '';
      const location = locationEl?.value.trim() ?? '';

      clearOccurrenceDropdowns();

      if (!talk || !location) {
         return;
      }

      try {
         const result = await postJson('/get-guardians-talk-occurrences', {
            talk,
            location
         });

         occurrences = result?.occurrences ?? [];

         const occurrenceDates = [
            ...new Set(
               occurrences
                  .map(occurrence => occurrence.date ?? occurrence.DATE ?? '')
                  .filter(Boolean)
            )
         ];

         populateDateDropdown(occurrenceDates);
      }
      catch(err) {
         clearOccurrenceDropdowns();
      }
   }

   function loadTimesForSelectedDate() {
      const selectedDate = dateEl?.value.trim() ?? '';

      populateTimeDropdown([]);

      if (!selectedDate) {
         return;
      }

      const occurrenceTimes = [
         ...new Set(
            occurrences
               .filter(occurrence => ( occurrence.date ?? occurrence.DATE ?? '' ) === selectedDate)
               .map(occurrence => occurrence.time ?? occurrence.TIME ?? '')
               .filter(Boolean)
         )
      ];

      populateTimeDropdown(occurrenceTimes);
   }

   async function onShowClick() {
      setStatus(statusEl, '');

      try {
         resetForm();

         if (talkLocationFilterController?.refreshLocations) {
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
      const date = dateEl?.value.trim() ?? '';
      const time = timeEl?.value.trim() ?? '';

      setStatus(statusEl, '');

      if (!location) {
         setStatus(statusEl, 'Location is required.', 'is-error');
         return;
      }

      if (!talk) {
         setStatus(statusEl, 'Talk name is required.', 'is-error');
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

         const result = await postJson('/cancel-guardians-talk-occurrence', {
            talk,
            location,
            date,
            time
         });

         if (result.success) {
            setStatus(
               statusEl,
               `${result.talk} in ${result.location} on ${result.date} at ${result.time} was cancelled.`,
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

   talkNameEl?.addEventListener('change', async () => {
      if (dateEl) dateEl.value = '';
      if (timeEl) timeEl.value = '';
      await loadOccurrencesForSelectedTalk();
   });

   dateEl?.addEventListener('change', () => {
      if (timeEl) timeEl.value = '';
      loadTimesForSelectedDate();
   });

   showButtonEl?.addEventListener('click', onShowClick);
   cancelButtonEl?.addEventListener('click', hide);
   submitButtonEl?.addEventListener('click', onSubmitClick);

   return {
      show,
      hide,
   };

}