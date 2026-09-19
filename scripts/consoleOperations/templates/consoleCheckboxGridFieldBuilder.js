import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsoleCheckboxGridFieldBuilder {
   static createCheckboxOption({
      id,
      label,
      value = '',
      checked = false,
      disabled = false,
   } = {}) {
      const optionLabelEl = document.createElement('label');
      optionLabelEl.className = 'console-operations-checkbox-option';

      const inputEl = ConsoleFieldPrimitiveBuilder.createInput({
         inputId: id,
         type: 'checkbox',
         className: '',
         autocomplete: '',
      });
      inputEl.value = value;
      inputEl.checked = checked;
      inputEl.disabled = disabled;

      const textEl = document.createElement('span');
      textEl.textContent = label;

      optionLabelEl.append(inputEl, textEl);
      return optionLabelEl;
   }


   static createCheckboxGridField({
      label,
      gridId,
      options = [],
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
      });

      const gridEl = document.createElement('div');
      gridEl.className = 'console-operations-checkbox-grid';

      if (gridId) {
         gridEl.id = gridId;
      }

      options.forEach((option) => {
         gridEl.appendChild(ConsoleCheckboxGridFieldBuilder.createCheckboxOption(option));
      });

      fieldEl.append(labelEl, gridEl);
      return fieldEl;
   }
}
