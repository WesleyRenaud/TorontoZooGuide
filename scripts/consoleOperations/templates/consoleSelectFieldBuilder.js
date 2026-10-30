import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsoleSelectFieldBuilder {
   static createSelectField({
      label,
      inputId,
      emptyOptionLabel,
      options = [],
      includeEmptyOption = true,
      disabled = false,
      invisible = false,
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();

      if (invisible) {
         fieldEl.classList.add('is-invisible');
      }
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
         htmlFor: inputId,
      });

      const selectEl = document.createElement('select');
      selectEl.id = inputId;
      selectEl.className = 'console-operations-input console-operations-select';
      selectEl.disabled = disabled;

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
