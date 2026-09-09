import assert from 'node:assert/strict';
import test from 'node:test';

import { RecurringScheduleRowsController } from '../../../../scripts/consoleOperations/forms/recurringScheduleRowsController.js';
import { RecurringScheduleRowsBuilder } from '../../../../scripts/consoleOperations/forms/recurringScheduleRowsBuilder.js';
import { RecurringScheduleBuilder } from '../../../../scripts/consoleOperations/forms/recurringScheduleBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createRowController({ rowIndex, allowRemove, initialRow = {} }) {
   const removeButtonEl = allowRemove ? document.createElement('button') : null;
   const dayInputEls = {};
   RecurringScheduleBuilder.RECURRING_SCHEDULE_WEEKDAY_KEYS.forEach((dayKey) => {
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

test('Test_CreateRecurringScheduleRowsController_TestAddGetValidateReset_ExpectRows', () => {
   const originalCreate = RecurringScheduleRowsBuilder.createScheduleRow;
   const originalNormalize = RecurringScheduleBuilder.normalizeRecurringScheduleRow;
   const originalValidate = RecurringScheduleBuilder.validateRecurringScheduleRows;
   const created = [];

   RecurringScheduleRowsBuilder.createScheduleRow = (options) => {
      const row = _createRowController(options);
      created.push(options);
      return row;
   };
   RecurringScheduleBuilder.normalizeRecurringScheduleRow = (row) => row;
   RecurringScheduleBuilder.validateRecurringScheduleRows = (rows) => {
      return rows.length ? null : 'missing';
   };

   try {
      const rowsEl = document.createElement('div');
      const addRowButtonEl = document.createElement('button');
      const controller = RecurringScheduleRowsController.createRecurringScheduleRowsController({
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
      RecurringScheduleRowsBuilder.createScheduleRow = originalCreate;
      RecurringScheduleBuilder.normalizeRecurringScheduleRow = originalNormalize;
      RecurringScheduleBuilder.validateRecurringScheduleRows = originalValidate;
   }
});

test('Test_CreateRecurringScheduleRowsController_TestRemoveRow_ExpectKeepsFirst', () => {
   const originalCreate = RecurringScheduleRowsBuilder.createScheduleRow;
   const originalNormalize = RecurringScheduleBuilder.normalizeRecurringScheduleRow;
   const rowControllers = [];

   RecurringScheduleRowsBuilder.createScheduleRow = (options) => {
      const row = _createRowController({
         ...options,
         allowRemove: true,
      });
      rowControllers.push(row);
      return row;
   };
   RecurringScheduleBuilder.normalizeRecurringScheduleRow = (row) => row;

   try {
      const rowsEl = document.createElement('div');
      const controller = RecurringScheduleRowsController.createRecurringScheduleRowsController({
         rowsEl,
         addRowButtonEl: document.createElement('button'),
      });

      controller.addRow({ time: '1:00 PM' });
      controller.addRow({ time: '2:00 PM' });
      assert.equal(controller.getRows().length, 3);

      rowControllers[0].removeButtonEl.listeners.click();
      assert.equal(controller.getRows().length, 3);

      rowControllers[2].removeButtonEl.listeners.click();
      assert.equal(controller.getRows().length, 2);
      assert.equal(rowsEl.children.length, 2);

      RecurringScheduleRowsController.createRecurringScheduleRowsController({
         addRowButtonEl: document.createElement('button'),
      });
   } finally {
      RecurringScheduleRowsBuilder.createScheduleRow = originalCreate;
      RecurringScheduleBuilder.normalizeRecurringScheduleRow = originalNormalize;
   }
});
