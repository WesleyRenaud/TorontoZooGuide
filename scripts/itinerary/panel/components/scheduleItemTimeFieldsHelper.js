import { ItineraryItemFormatter } from '../itineraryItemFormatter.js';
import { ItineraryPanelHelper } from '../itineraryPanelHelper.js';

export class ScheduleItemTimeFieldsHelper {
   static createFieldLabel(text) {
      return ItineraryPanelHelper.el('label', 'schedule-item-field-label', text);
   }

   static readPickerTimeValue(instance, dateStr, inputEl) {
      return ItineraryItemFormatter.formatClockTime(dateStr || instance?.input?.value || inputEl.value || '');
   }
}
