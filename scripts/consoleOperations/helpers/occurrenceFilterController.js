import { ControllerHelper } from './controllerHelper.js';
import { ConsoleDropdownPopulator } from '../options/consoleDropdownPopulator.js';
import { Strings } from '../../strings.js';

export class OccurrenceFilterController {
   static createOccurrenceFilterController({
      dateEl,
      timeEl = null,
      populateTimes = null,
      autoSelectSingleTime = false,
      getSelectionValues = () => ({}),
      isSelectionReady = selectionValues => Object.values(selectionValues).every(Boolean),
      loadOccurrences,
   } = {}) {
      let occurrences = [];

      function populateDateDropdown(dates) {
         ConsoleDropdownPopulator.populateValueDropdown(dateEl, dates, Strings.placeholders.date);
      }

      function populateTimeDropdown(times) {
         if (populateTimes) {
            populateTimes(times);
            return;
         }

         ConsoleDropdownPopulator.populateValueDropdown(timeEl, times, Strings.placeholders.time);
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
         const selectedDate = ControllerHelper.getFieldValue(dateEl);

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

         if (
            autoSelectSingleTime
            && occurrenceTimes.length === 1
            && timeEl?.tagName === 'SELECT'
         ) {
            timeEl.value = occurrenceTimes[0];
         }
      }

      return {
         refresh,
         refreshTimes,
         clear,
      };
   }
}
