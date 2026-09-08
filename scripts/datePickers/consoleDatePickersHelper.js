import { ValueNormalizer } from '../api/valueNormalizer.js';
import { FlatpickrAdapter } from './flatpickrAdapter.js';

export class ConsoleDatePickersHelper {
   static DATE_PICKER_OPTIONS = {
      enableTime: false,
      dateFormat: 'Y-m-d',
   };

   static initDatePicker(inputEl, options = {}, initFlatpickrFn = FlatpickrAdapter.initFlatpickr) {
      return initFlatpickrFn(inputEl, {
         ...ConsoleDatePickersHelper.DATE_PICKER_OPTIONS,
         ...options,
      });
   }

   static bindEndDateMinDate(
      startDateEl,
      endDatePicker,
      {
         emptyMinDate = null,
      } = {}
   ) {
      if (!startDateEl || !endDatePicker) {
         return;
      }

      function syncMinDate() {
         const startValue = ValueNormalizer.asTrimmedString(startDateEl.value);

         endDatePicker.set('minDate', startValue || emptyMinDate);
      }

      startDateEl.addEventListener('change', syncMinDate);
      syncMinDate();
   }
}
