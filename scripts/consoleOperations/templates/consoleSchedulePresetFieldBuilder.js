import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';
import { Strings } from '../../strings.js';

export class ConsoleSchedulePresetFieldBuilder {
   static createSchedulePresetField({
      inputId,
      label = Strings.labels.schedulePreset,
   } = {}) {
      const fieldEl = ConsoleFieldPrimitiveBuilder.createFieldWrapper();
      const labelEl = ConsoleFieldPrimitiveBuilder.createLabel({
         text: label,
         htmlFor: inputId,
      });

      const selectEl = document.createElement('select');
      selectEl.id = inputId;
      selectEl.className = 'console-operations-input console-operations-select';

      [
         { value: 'everyDay', label: Strings.schedule.presetLabels.everyDay },
         { value: 'custom', label: Strings.schedule.presetLabels.custom },
         { value: 'weekendsOnly', label: Strings.schedule.presetLabels.weekendsOnly },
         { value: 'weekendsAndHolidays', label: Strings.schedule.presetLabels.weekendsAndHolidays },
      ].forEach((option) => {
         selectEl.appendChild(ConsoleFieldPrimitiveBuilder.createOption(option));
      });

      fieldEl.append(labelEl, selectEl);
      return fieldEl;
   }
}
