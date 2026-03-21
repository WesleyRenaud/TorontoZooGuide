import { postJson } from '../../utils.js';

export function createWildEncounterOccurrenceFilterController({
   wildEncounterEl,
   dateEl,
   timeEl,
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

   function clear() {
      occurrences = [];
      populateDateDropdown([]);
      populateTimeDropdown([]);
   }

   async function refresh() {
      const wildEncounter = wildEncounterEl?.value.trim() ?? '';

      clear();

      if (!wildEncounter) {
         return;
      }

      try {
         const result = await postJson('/get-wild-encounter-occurrences', {
            wildEncounter
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
         clear();
      }
   }

   function refreshTimes() {
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

   return {
      refresh,
      refreshTimes,
      clear,
   };
}