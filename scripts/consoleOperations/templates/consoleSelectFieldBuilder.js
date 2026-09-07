import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsoleSelectFieldBuilder {
   static createSelectField({
      label,
      inputId,
      emptyOptionLabel,
      options = [],
      includeEmptyOption = true,
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
         htmlFor: inputId,
      });

      const selectEl = document.createElement('select');
      selectEl.id = inputId;
      selectEl.className = 'console-operations-input console-operations-select';

      if (includeEmptyOption) {
         selectEl.appendChild(ConsoleFieldPrimitiveBuilder.createOption({
            value: '',
            label: emptyOptionLabel,
         }));
      }

      options.forEach((option) => {
         selectEl.appendChild(ConsoleFieldPrimitiveBuilder.createOption(option));
      });

      fieldEl.append(labelEl, selectEl);
      return fieldEl;
   }
}
