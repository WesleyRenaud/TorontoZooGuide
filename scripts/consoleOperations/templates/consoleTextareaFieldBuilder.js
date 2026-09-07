import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsoleTextareaFieldBuilder {
   static createTextareaField({
      label,
      inputId,
      placeholder,
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
         htmlFor: inputId,
      });

      const textareaEl = document.createElement('textarea');
      textareaEl.id = inputId;
      textareaEl.className = 'console-operations-textarea';

      if (placeholder) {
         textareaEl.placeholder = placeholder;
      }

      fieldEl.append(labelEl, textareaEl);
      return fieldEl;
   }
}
