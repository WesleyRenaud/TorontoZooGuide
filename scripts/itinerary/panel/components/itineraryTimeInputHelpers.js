import { ItineraryItemFormatter } from '../itineraryItemFormatter.js';

export class ItineraryTimeInputHelpers {
   static readPickerTimeValue(instance, dateStr, inputEl) {
      return ItineraryItemFormatter.formatClockTime(dateStr || instance?.input?.value || inputEl.value || '');
   }
}
