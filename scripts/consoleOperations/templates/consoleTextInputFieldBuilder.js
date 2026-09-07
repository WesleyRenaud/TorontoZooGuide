import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsoleTextInputFieldBuilder {
   static createTextInputField({
      label,
      inputId,
      placeholder,
      inputClass = 'console-operations-input',
      helpText = '',
      type = 'text',
      autocomplete = 'off',
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
         htmlFor: inputId,
      });

      const inputEl = ConsoleFieldPrimitiveBuilder.createInput({
         inputId,
         type,
         className: inputClass,
         placeholder,
         autocomplete,
      });

      fieldEl.append(labelEl, inputEl);
      ConsoleFieldPrimitiveBuilder.appendChild(
         fieldEl,
         ConsoleFieldPrimitiveBuilder.createHelpText(helpText)
      );

      return fieldEl;
   }
}
