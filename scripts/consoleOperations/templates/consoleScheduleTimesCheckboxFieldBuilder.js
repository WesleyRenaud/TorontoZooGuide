import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';
import { Strings } from '../../strings.js';

export class ConsoleScheduleTimesCheckboxFieldBuilder {
   static createScheduleTimesCheckboxField({
      label,
      inputId,
      helpText = '',
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
      });

      const listEl = document.createElement('div');
      listEl.id = inputId;
      listEl.className = 'console-operations-schedule-times-list';

      const placeholderEl = document.createElement('div');
      placeholderEl.className = 'console-operations-schedule-times-placeholder';
      placeholderEl.textContent = Strings.placeholders.selectWildEncounterFirst;

      listEl.appendChild(placeholderEl);
      fieldEl.append(labelEl, listEl);
      ConsoleFieldPrimitiveBuilder.appendChild(
         fieldEl,
         ConsoleFieldPrimitiveBuilder.createHelpText(helpText)
      );

      return fieldEl;
   }
}
