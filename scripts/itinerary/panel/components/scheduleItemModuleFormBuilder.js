import { ItineraryPanelDom } from '../itineraryPanelDom.js';

export class ScheduleItemModuleFormBuilder {
   static createFieldLabel(text) {
      return ItineraryPanelDom.el('label', 'schedule-item-field-label', text);
   }

   static createOnlyItineraryItemsCheckbox(labelText) {
      const wrap = ItineraryPanelDom.el('div', 'schedule-item-only-itinerary-wrap');
      const label = ItineraryPanelDom.el('label', 'schedule-item-only-itinerary-row');
      const checkbox = document.createElement('input');

      checkbox.type = 'checkbox';
      checkbox.className = 'schedule-item-only-itinerary-checkbox';
      checkbox.checked = false;

      const text = ItineraryPanelDom.el('span', 'schedule-item-only-itinerary-label', labelText);
      label.append(checkbox, text);
      wrap.appendChild(label);

      return { wrap, checkbox };
   }

   static createSelectField({
      label,
      options = [],
      getOptionValue = (option) => option,
      getOptionLabel = (option) => String(option),
   } = {}) {
      const field = ItineraryPanelDom.el('div', 'schedule-item-field schedule-item-type-field');
      const select = document.createElement('select');
      select.className = 'schedule-item-select';

      field.appendChild(ScheduleItemModuleFormBuilder.createFieldLabel(label));
      field.appendChild(select);

      options.forEach((option) => {
         const optionEl = document.createElement('option');
         const value = getOptionValue(option);

         optionEl.value = value;
         optionEl.textContent = getOptionLabel(option);
         optionEl.selected = Boolean(option.selected);
         select.appendChild(optionEl);
      });

      return {
         field,
         select,
      };
   }
}
