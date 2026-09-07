import { ItineraryItemFormatter } from '../itineraryItemFormatter.js';
import { ItineraryPanelDom } from '../itineraryPanelDom.js';

export class ScheduleItemTimeFieldsHelpers {
   static createFieldLabel(text) {
      return ItineraryPanelDom.el('label', 'schedule-item-field-label', text);
   }

   static readPickerTimeValue(instance, dateStr, inputEl) {
      return ItineraryItemFormatter.formatClockTime(dateStr || instance?.input?.value || inputEl.value || '');
   }
}
