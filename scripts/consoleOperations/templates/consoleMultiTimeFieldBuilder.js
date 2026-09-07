import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsoleMultiTimeFieldBuilder {
   static createMultiTimeField({
      label,
      listId,
      inputId,
      placeholder,
      helpText = '',
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
         htmlFor: inputId,
      });

      const compositeEl = document.createElement('div');
      compositeEl.className = 'console-operations-multi-time-field';

      const listEl = document.createElement('div');
      listEl.id = listId;
      listEl.className = 'console-operations-multi-time-list';

      const inputEl = ConsoleFieldPrimitiveBuilder.createInput({
         inputId,
         className: 'console-operations-multi-time-input console-operations-datetime',
         placeholder,
      });

      compositeEl.append(listEl, inputEl);
      fieldEl.append(labelEl, compositeEl);
      ConsoleFieldPrimitiveBuilder.appendChild(
         fieldEl,
         ConsoleFieldPrimitiveBuilder.createHelpText(helpText)
      );

      return fieldEl;
   }
}
