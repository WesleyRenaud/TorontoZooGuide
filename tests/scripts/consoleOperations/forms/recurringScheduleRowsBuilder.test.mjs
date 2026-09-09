import assert from 'node:assert/strict';
import test from 'node:test';

import { RecurringScheduleRowsBuilder } from '../../../../scripts/consoleOperations/forms/recurringScheduleRowsBuilder.js';
import { ConsoleDateFactory } from '../../../../scripts/datePickers/consoleDateFactory.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateDayCheckbox_TestChecked_ExpectOption', () => {
   const { inputEl, optionLabelEl } = RecurringScheduleRowsBuilder.createDayCheckbox({
      rowIndex: 1,
      dayKey: 'monday',
      label: 'Monday',
      checked: true,
   });

   assert.equal(inputEl.id, 'wildEncounterScheduleRow1monday');
   assert.equal(inputEl.checked, true);
   assert.match(optionLabelEl.textContent, /Monday/);
});

test('Test_CreateScheduleRow_TestAllowRemove_ExpectRowParts', () => {
   const original = ConsoleDateFactory.initTimePicker;
   const inits = [];
   ConsoleDateFactory.initTimePicker = (el) => { inits.push(el); };

   try {
      const row = RecurringScheduleRowsBuilder.createScheduleRow({
         rowIndex: 0,
         initialRow: { time: '11:00 AM', monday: true },
         allowRemove: true,
      });

      assert.equal(row.rowEl.className, 'console-operations-schedule-row');
      assert.equal(row.timeInputEl.placeholder, Strings.placeholders.time);
      assert.equal(row.dayInputEls.monday.checked, true);
      assert.ok(row.removeButtonEl);
      assert.equal(inits.length, 1);

      const noRemove = RecurringScheduleRowsBuilder.createScheduleRow({
         rowIndex: 2,
         allowRemove: false,
      });
      assert.equal(noRemove.removeButtonEl, null);
   } finally {
      ConsoleDateFactory.initTimePicker = original;
   }
});
