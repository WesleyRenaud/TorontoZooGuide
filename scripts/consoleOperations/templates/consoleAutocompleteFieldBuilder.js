import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsoleAutocompleteFieldBuilder {
   static createAutocompleteField({
      label,
      inputId,
      resultsId,
      placeholder,
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
         htmlFor: inputId,
      });

      const inputEl = ConsoleFieldPrimitiveBuilder.createInput({
         inputId,
         className: 'console-operations-input',
         placeholder,
         autocomplete: 'off',
      });

      const resultsEl = document.createElement('div');
      resultsEl.id = resultsId;
      resultsEl.className = 'console-operations-autocomplete';

      fieldEl.append(labelEl, inputEl, resultsEl);
      return fieldEl;
   }
}
