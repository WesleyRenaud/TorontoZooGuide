import { ConsoleTextInputFieldBuilder } from './consoleTextInputFieldBuilder.js';

export class ConsoleDateFieldBuilder {
   static createDateField({
      label,
      inputId,
      placeholder,
      helpText = '',
   } = {}) {
      return ConsoleTextInputFieldBuilder.createTextInputField({
         label,
         inputId,
         placeholder,
         helpText,
         inputClass: 'console-operations-input console-operations-datetime',
      });
   }
}
