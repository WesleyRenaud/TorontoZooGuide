export class UpdateOptionsFormatter {
   static createPlaceholderOption(label) {
      const optionEl = document.createElement('option');
      optionEl.value = '';
      optionEl.textContent = label;
      return optionEl;
   }

   static formatDateRange(update) {
      if (!update.end_date) {
         return `${update.start_date} onward`;
      }

      return `${update.start_date} to ${update.end_date}`;
   }

   static formatUpdateOptionLabel(update) {
      return `${update.title} (${update.type}, ${UpdateOptionsFormatter.formatDateRange(update)})`;
   }
}
