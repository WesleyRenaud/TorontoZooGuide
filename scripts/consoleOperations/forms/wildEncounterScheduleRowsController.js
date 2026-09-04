import { ConsoleDatePickers } from '../../datePickers/consoleDatePickers.js';
import { APP_STRINGS } from '../../strings.js';
import { common } from '../../strings/common.js';
import { WildEncounterScheduleRows } from './wildEncounterScheduleRows.js';

function createDayCheckbox({
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

function createScheduleRow({
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
   timeInputEl.placeholder = APP_STRINGS.placeholders.time;
   timeInputEl.setAttribute('aria-label', APP_STRINGS.labels.encounterTime);
   timeInputEl.autocomplete = 'off';

   const normalizedRow = WildEncounterScheduleRows.normalizeWildEncounterScheduleRow(initialRow);

   if (normalizedRow.time) {
      timeInputEl.value = normalizedRow.time;
   }

   timeFieldEl.appendChild(timeInputEl);

   const daysEl = document.createElement('div');
   daysEl.className = 'console-operations-checkbox-grid console-operations-schedule-row-days';

   const dayInputEls = {};

   WildEncounterScheduleRows.WILD_ENCOUNTER_SCHEDULE_WEEKDAY_KEYS.forEach((dayKey) => {
      const { inputEl, optionLabelEl } = createDayCheckbox({
         rowIndex,
         dayKey,
         label: APP_STRINGS.schedule.dayLabels[dayKey],
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
         APP_STRINGS.help.removeEncounterScheduleRow
      );
      removeButtonEl.textContent = common.closeSymbol;
      removeSlotEl.appendChild(removeButtonEl);
   }

   rowEl.appendChild(removeSlotEl);

   ConsoleDatePickers.initTimePicker(timeInputEl);

   return {
      rowEl,
      timeInputEl,
      dayInputEls,
      removeButtonEl,
   };
}

export function createWildEncounterScheduleRowsController({
   rowsEl,
   addRowButtonEl,
} = {}) {
   let nextRowIndex = 0;
   const rowControllers = [];

   function readRowValues(rowController) {
      const row = {
         time: rowController.timeInputEl.value,
      };

      WildEncounterScheduleRows.WILD_ENCOUNTER_SCHEDULE_WEEKDAY_KEYS.forEach((dayKey) => {
         row[dayKey] = Boolean(rowController.dayInputEls[dayKey]?.checked);
      });

      return WildEncounterScheduleRows.normalizeWildEncounterScheduleRow(row);
   }

   function render() {
      if (!rowsEl) {
         return;
      }

      rowsEl.replaceChildren();

      rowControllers.forEach((rowController) => {
         rowsEl.appendChild(rowController.rowEl);
      });
   }

   function removeRow(rowController) {
      const rowIndex = rowControllers.indexOf(rowController);

      if (rowIndex <= 0) {
         return;
      }

      rowControllers.splice(rowIndex, 1);
      render();
   }

   function addRow(initialRow = {}) {
      const rowController = createScheduleRow({
         rowIndex: nextRowIndex,
         initialRow,
         allowRemove: rowControllers.length > 0,
      });

      nextRowIndex += 1;

      rowController.removeButtonEl?.addEventListener('click', () => {
         removeRow(rowController);
      });

      rowControllers.push(rowController);
      render();
      return rowController;
   }

   function getRows() {
      return rowControllers.map(readRowValues);
   }

   function validate() {
      return WildEncounterScheduleRows.validateWildEncounterScheduleRows(getRows());
   }

   function setRows(rows = []) {
      rowControllers.length = 0;
      nextRowIndex = 0;

      if (rows.length > 0) {
         rows.forEach((row) => {
            addRow(row);
         });
         return;
      }

      addRow();
   }

   function reset() {
      setRows();
   }

   addRowButtonEl?.addEventListener('click', () => {
      addRow();
   });

   reset();

   return {
      addRow,
      getRows,
      setRows,
      validate,
      reset,
   };
}
