import { WildEncounterScheduleBuilder } from './wildEncounterScheduleBuilder.js';
import { WildEncounterScheduleRowsBuilder } from './wildEncounterScheduleRowsBuilder.js';

export class WildEncounterScheduleRowsController {
   static createWildEncounterScheduleRowsController({
      rowsEl,
      addRowButtonEl,
   } = {}) {
      let nextRowIndex = 0;
      const rowControllers = [];

      function readRowValues(rowController) {
         const row = {
            time: rowController.timeInputEl.value,
         };

         WildEncounterScheduleBuilder.WILD_ENCOUNTER_SCHEDULE_WEEKDAY_KEYS.forEach((dayKey) => {
            row[dayKey] = Boolean(rowController.dayInputEls[dayKey]?.checked);
         });

         return WildEncounterScheduleBuilder.normalizeWildEncounterScheduleRow(row);
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
         const rowController = WildEncounterScheduleRowsBuilder.createScheduleRow({
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
         return WildEncounterScheduleBuilder.validateWildEncounterScheduleRows(getRows());
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
}
