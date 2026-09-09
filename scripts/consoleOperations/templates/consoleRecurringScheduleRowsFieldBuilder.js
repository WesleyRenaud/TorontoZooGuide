import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';
import { Strings } from '../../strings.js';

export class ConsoleRecurringScheduleRowsFieldBuilder {
   static createRecurringScheduleRowsField({
      label = Strings.labels.encounterTimes,
      rowsId,
      addRowButtonId,
      helpText = Strings.help.encounterScheduleRows,
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
      });

      const rowsEl = document.createElement('div');
      rowsEl.id = rowsId;
      rowsEl.className = 'console-operations-schedule-rows';

      const addRowButtonEl = document.createElement('button');
      addRowButtonEl.id = addRowButtonId;
      addRowButtonEl.type = 'button';
      addRowButtonEl.className = 'console-operations-secondary-btn console-operations-schedule-rows-add';
      addRowButtonEl.textContent = Strings.actions.addEncounterScheduleRow;

      fieldEl.append(labelEl, rowsEl, addRowButtonEl);
      ConsoleFieldPrimitiveBuilder.appendChild(
         fieldEl,
         ConsoleFieldPrimitiveBuilder.createHelpText(helpText)
      );

      return fieldEl;
   }
}
