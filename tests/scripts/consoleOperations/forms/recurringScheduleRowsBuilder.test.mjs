import assert from 'node:assert/strict';
import test from 'node:test';

import { RecurringScheduleRowsBuilder } from '../../../../scripts/consoleOperations/forms/recurringScheduleRowsBuilder.js';
import { ConsoleDateFactory } from '../../../../scripts/datePickers/consoleDateFactory.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateDayCheckbox_TestChecked_ExpectOption', () => {
   const rowIndex = 1;
   const dayKey = 'monday';
   const label = 'Monday';
   const checked = true;

   const { inputEl, optionLabelEl } = RecurringScheduleRowsBuilder.createDayCheckbox({
      rowIndex,
      dayKey,
      label,
      checked,
   });

   assert.equal(inputEl.id, `wildEncounterScheduleRow${rowIndex}${dayKey}`);
   assert.equal(inputEl.checked, checked);
   assert.match(optionLabelEl.textContent, new RegExp(label));
});


test('Test_CreateScheduleRow_TestAllowRemove_ExpectRowParts', () => {
   const original = ConsoleDateFactory.initTimePicker;
   const inits = [];
   const time = '11:00 AM';
   ConsoleDateFactory.initTimePicker = (el) => {
      inits.push(el);
   };

   try {
      const row = RecurringScheduleRowsBuilder.createScheduleRow({
         rowIndex: 0,
         initialRow: { time, monday: true },
         allowRemove: true,
      });

      assert.equal(row.rowEl.className, 'console-operations-schedule-row');
      assert.equal(row.timeInputEl.placeholder, Strings.placeholders.time);
      assert.equal(row.dayInputEls.monday.checked, true);
      assert.ok(row.removeButtonEl);
      assert.equal(inits.length, 1);
   } finally {
      ConsoleDateFactory.initTimePicker = original;
   }
});


test('Test_CreateScheduleRow_TestDisallowRemove_ExpectNoRemoveButton', () => {
   const original = ConsoleDateFactory.initTimePicker;
   ConsoleDateFactory.initTimePicker = () => {};

   try {
      const row = RecurringScheduleRowsBuilder.createScheduleRow({
         rowIndex: 2,
         allowRemove: false,
      });

      assert.equal(row.removeButtonEl, null);
   } finally {
      ConsoleDateFactory.initTimePicker = original;
   }
});
