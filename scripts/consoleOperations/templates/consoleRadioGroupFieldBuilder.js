import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsoleRadioGroupFieldBuilder {
   static createRadioGroupField({
      label,
      name,
      options = [],
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
      });

      const groupEl = document.createElement('div');
      groupEl.className = 'console-operations-radio-group';

      options.forEach((option) => {
         const optionLabelEl = document.createElement('label');
         optionLabelEl.className = 'console-operations-radio-option';

         const inputEl = ConsoleFieldPrimitiveBuilder.createInput({
            inputId: option.id,
            type: 'radio',
            className: '',
            autocomplete: '',
            value: option.value,
         });
         inputEl.name = name;

         if (option.checked) {
            inputEl.checked = true;
         }

         const textEl = document.createElement('span');
         textEl.textContent = option.label;

         optionLabelEl.append(inputEl, textEl);
         groupEl.appendChild(optionLabelEl);
      });

      fieldEl.append(labelEl, groupEl);
      return fieldEl;
   }
}
