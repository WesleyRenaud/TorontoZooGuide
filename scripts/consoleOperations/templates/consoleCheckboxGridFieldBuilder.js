import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsoleCheckboxGridFieldBuilder {
   static createCheckboxGridField({
      label,
      options = [],
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
      });

      const gridEl = document.createElement('div');
      gridEl.className = 'console-operations-checkbox-grid';

      options.forEach((option) => {
         const optionLabelEl = document.createElement('label');
         optionLabelEl.className = 'console-operations-checkbox-option';

         const inputEl = ConsoleFieldPrimitiveBuilder.createInput({
            inputId: option.id,
            type: option.type || 'checkbox',
            className: '',
            autocomplete: '',
         });

         const textEl = document.createElement('span');
         textEl.textContent = option.label;

         optionLabelEl.append(inputEl, textEl);
         gridEl.appendChild(optionLabelEl);
      });

      fieldEl.append(labelEl, gridEl);
      return fieldEl;
   }
}
