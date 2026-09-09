import { Strings } from '../../../strings.js';

export class UpdateOptionsFormatter {
   static createPlaceholderOption(label) {
      const optionEl = document.createElement('option');
      optionEl.value = '';
      optionEl.textContent = label;
      return optionEl;
   }

   static formatDateRange(update) {
      if (!update.end_date) {
         return Strings.format.dateOnward(update.start_date);
      }

      return Strings.format.dateRangeTo(update.start_date, update.end_date);
   }

   static formatUpdateOptionLabel(update) {
      return `${update.title} (${update.type}, ${UpdateOptionsFormatter.formatDateRange(update)})`;
   }
}
