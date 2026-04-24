import { populateValueDropdown } from '../options/dropdowns.js';

export function createOccurrenceFilterController({
   dateEl,
   timeEl,
   getSelectionValues = () => ({}),
   isSelectionReady = selectionValues => Object.values(selectionValues).every(Boolean),
   loadOccurrences,
} = {}) {
   let occurrences = [];

   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function populateDateDropdown(dates) {
      populateValueDropdown(dateEl, dates, 'Select a date');
   }

   function populateTimeDropdown(times) {
      populateValueDropdown(timeEl, times, 'Select a time');
   }

   function getOccurrenceValues(field) {
      return [
         ...new Set(
            occurrences
               .map(occurrence => occurrence?.[field] ?? '')
               .filter(Boolean)
         )
      ];
   }

   function clear() {
      occurrences = [];
      populateDateDropdown([]);
      populateTimeDropdown([]);
   }

   async function refresh() {
      const selectionValues = getSelectionValues();

      clear();

      if (!isSelectionReady(selectionValues)) {
         return;
      }

      try {
         occurrences = await loadOccurrences?.(selectionValues) ?? [];
         populateDateDropdown(getOccurrenceValues('date'));
      }
      catch (err) {
         clear();
      }
   }

   function refreshTimes() {
      const selectedDate = getFieldValue(dateEl);

      populateTimeDropdown([]);

      if (!selectedDate) {
         return;
      }

      const occurrenceTimes = [
         ...new Set(
            occurrences
               .filter(occurrence => (occurrence.date ?? '') === selectedDate)
               .map(occurrence => occurrence.time ?? '')
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
