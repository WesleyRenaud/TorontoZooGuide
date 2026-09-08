import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterScheduleRowsController } from '../../../../scripts/consoleOperations/forms/wildEncounterScheduleRowsController.js';
import { WildEncounterScheduleRowsBuilder } from '../../../../scripts/consoleOperations/forms/wildEncounterScheduleRowsBuilder.js';
import { WildEncounterScheduleBuilder } from '../../../../scripts/consoleOperations/forms/wildEncounterScheduleBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createRowController({ rowIndex, allowRemove, initialRow = {} }) {
   const removeButtonEl = allowRemove ? document.createElement('button') : null;
   const dayInputEls = {};
   WildEncounterScheduleBuilder.WILD_ENCOUNTER_SCHEDULE_WEEKDAY_KEYS.forEach((dayKey) => {
      dayInputEls[dayKey] = {
         checked: Boolean(initialRow[dayKey]),
      };
   });

   return {
      rowEl: document.createElement('div'),
      timeInputEl: { value: initialRow.time || '' },
      dayInputEls,
      removeButtonEl,
      rowIndex,
   };
}

test('Test_CreateWildEncounterScheduleRowsController_TestAddGetValidateReset_ExpectRows', () => {
   const originalCreate = WildEncounterScheduleRowsBuilder.createScheduleRow;
   const originalNormalize = WildEncounterScheduleBuilder.normalizeWildEncounterScheduleRow;
   const originalValidate = WildEncounterScheduleBuilder.validateWildEncounterScheduleRows;
   const created = [];

   WildEncounterScheduleRowsBuilder.createScheduleRow = (options) => {
      const row = _createRowController(options);
      created.push(options);
      return row;
   };
   WildEncounterScheduleBuilder.normalizeWildEncounterScheduleRow = (row) => row;
   WildEncounterScheduleBuilder.validateWildEncounterScheduleRows = (rows) => {
      return rows.length ? null : 'missing';
   };

   try {
      const rowsEl = document.createElement('div');
      const addRowButtonEl = document.createElement('button');
      const controller = WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController({
         rowsEl,
         addRowButtonEl,
      });

      assert.equal(created.length, 1);
      assert.equal(created[0].allowRemove, false);
      assert.equal(rowsEl.children.length, 1);

      controller.addRow({ time: '2:00 PM', tuesday: true });
      assert.equal(created.length, 2);
      assert.equal(created[1].allowRemove, true);
      assert.equal(rowsEl.children.length, 2);

      assert.deepEqual(controller.getRows(), [
         {
            time: '',
            monday: false,
            tuesday: false,
            wednesday: false,
            thursday: false,
            friday: false,
            saturday: false,
            sunday: false,
         },
         {
            time: '2:00 PM',
            monday: false,
            tuesday: true,
            wednesday: false,
            thursday: false,
            friday: false,
            saturday: false,
            sunday: false,
         },
      ]);
      assert.equal(controller.validate(), null);

      addRowButtonEl.listeners.click();
      assert.equal(created.length, 3);

      const secondRow = created[1];
      // remove is wired on the returned row controller from addRow; fetch via getRows length before remove
      controller.setRows([{ time: '11:00 AM', monday: true }]);
      assert.equal(created.length, 4);
      assert.deepEqual(controller.getRows()[0].time, '11:00 AM');

      controller.reset();
      assert.equal(controller.getRows().length, 1);
   } finally {
      WildEncounterScheduleRowsBuilder.createScheduleRow = originalCreate;
      WildEncounterScheduleBuilder.normalizeWildEncounterScheduleRow = originalNormalize;
      WildEncounterScheduleBuilder.validateWildEncounterScheduleRows = originalValidate;
   }
});

test('Test_CreateWildEncounterScheduleRowsController_TestRemoveRow_ExpectKeepsFirst', () => {
   const originalCreate = WildEncounterScheduleRowsBuilder.createScheduleRow;
   const originalNormalize = WildEncounterScheduleBuilder.normalizeWildEncounterScheduleRow;
   const rowControllers = [];

   WildEncounterScheduleRowsBuilder.createScheduleRow = (options) => {
      const row = _createRowController(options);
      rowControllers.push(row);
      return row;
   };
   WildEncounterScheduleBuilder.normalizeWildEncounterScheduleRow = (row) => row;

   try {
      const rowsEl = document.createElement('div');
      const controller = WildEncounterScheduleRowsController.createWildEncounterScheduleRowsController({
         rowsEl,
         addRowButtonEl: document.createElement('button'),
      });

      controller.addRow({ time: '1:00 PM' });
      controller.addRow({ time: '2:00 PM' });
      assert.equal(controller.getRows().length, 3);

      rowControllers[0].removeButtonEl?.listeners?.click?.();
      assert.equal(controller.getRows().length, 3);

      rowControllers[2].removeButtonEl.listeners.click();
      assert.equal(controller.getRows().length, 2);
      assert.equal(rowsEl.children.length, 2);
   } finally {
      WildEncounterScheduleRowsBuilder.createScheduleRow = originalCreate;
      WildEncounterScheduleBuilder.normalizeWildEncounterScheduleRow = originalNormalize;
   }
});
