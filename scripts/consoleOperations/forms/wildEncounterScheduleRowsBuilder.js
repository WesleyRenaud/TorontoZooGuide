import { ConsoleDateFactory } from '../../datePickers/consoleDateFactory.js';
import { Strings } from '../../strings.js';
import { WildEncounterScheduleBuilder } from './wildEncounterScheduleBuilder.js';

export class WildEncounterScheduleRowsBuilder {
   static createDayCheckbox({
      rowIndex,
      dayKey,
      label,
      checked = false,
   } = {}) {
      const optionLabelEl = document.createElement('label');
      optionLabelEl.className = 'console-operations-checkbox-option';

      const inputEl = document.createElement('input');
      inputEl.type = 'checkbox';
      inputEl.id = `wildEncounterScheduleRow${rowIndex}${dayKey}`;
      inputEl.checked = checked;

      const textEl = document.createElement('span');
      textEl.textContent = label;

      optionLabelEl.append(inputEl, textEl);
      return {
         inputEl,
         optionLabelEl,
      };
   }

   static createScheduleRow({
      rowIndex,
      initialRow = {},
      allowRemove = true,
   } = {}) {
      const rowEl = document.createElement('div');
      rowEl.className = 'console-operations-schedule-row';

      const timeFieldEl = document.createElement('div');
      timeFieldEl.className = 'console-operations-schedule-row-time';

      const timeInputEl = document.createElement('input');
      timeInputEl.id = `wildEncounterScheduleRow${rowIndex}Time`;
      timeInputEl.type = 'text';
      timeInputEl.className = 'console-operations-input console-operations-datetime';
      timeInputEl.placeholder = Strings.placeholders.time;
      timeInputEl.setAttribute('aria-label', Strings.labels.encounterTime);
      timeInputEl.autocomplete = 'off';

      const normalizedRow = WildEncounterScheduleBuilder.normalizeWildEncounterScheduleRow(initialRow);

      if (normalizedRow.time) {
         timeInputEl.value = normalizedRow.time;
      }

      timeFieldEl.appendChild(timeInputEl);

      const daysEl = document.createElement('div');
      daysEl.className = 'console-operations-checkbox-grid console-operations-schedule-row-days';

      const dayInputEls = {};

      WildEncounterScheduleBuilder.WILD_ENCOUNTER_SCHEDULE_WEEKDAY_KEYS.forEach((dayKey) => {
         const { inputEl, optionLabelEl } = WildEncounterScheduleRowsBuilder.createDayCheckbox({
            rowIndex,
            dayKey,
            label: Strings.schedule.dayLabels[dayKey],
            checked: normalizedRow[dayKey],
         });

         dayInputEls[dayKey] = inputEl;
         daysEl.appendChild(optionLabelEl);
      });

      rowEl.append(timeFieldEl, daysEl);

      const removeSlotEl = document.createElement('div');
      removeSlotEl.className = 'console-operations-schedule-row-remove-slot';

      let removeButtonEl = null;

      if (allowRemove) {
         removeButtonEl = document.createElement('button');
         removeButtonEl.type = 'button';
         removeButtonEl.className = 'console-operations-schedule-row-remove';
         removeButtonEl.setAttribute(
            'aria-label',
            Strings.help.removeEncounterScheduleRow
         );
         removeButtonEl.textContent = Strings.common.closeSymbol;
         removeSlotEl.appendChild(removeButtonEl);
      }

      rowEl.appendChild(removeSlotEl);

      ConsoleDateFactory.initTimePicker(timeInputEl);

      return {
         rowEl,
         timeInputEl,
         dayInputEls,
         removeButtonEl,
      };
   }
}
