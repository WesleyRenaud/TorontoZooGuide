import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDatePickersHelper } from '../../../scripts/datePickers/consoleDatePickersHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_InitDatePicker_TestOptions_ExpectMerged', () => {
   const calls = [];
   const inputEl = document.createElement('input');

   ConsoleDatePickersHelper.initDatePicker(inputEl, { allowInput: true }, (el, options) => {
      calls.push({ el, options });
      return { id: 'picker' };
   });

   assert.equal(calls.length, Position.SECOND);
   assert.equal(calls.at(Position.FIRST).el, inputEl);
   assert.deepEqual(calls.at(Position.FIRST).options, {
      ...ConsoleDatePickersHelper.DATE_PICKER_OPTIONS,
      allowInput: true,
   });
});


test('Test_BindEndDateMinDate_TestMissingStart_ExpectNoOp', () => {
   const endDatePicker = { set() {} };

   const bind = () => ConsoleDatePickersHelper.bindEndDateMinDate(null, endDatePicker);

   assert.doesNotThrow(bind);
});


test('Test_BindEndDateMinDate_TestMissingPicker_ExpectNoOp', () => {
   const startDateEl = document.createElement('input');

   const bind = () => ConsoleDatePickersHelper.bindEndDateMinDate(startDateEl, null);

   assert.doesNotThrow(bind);
});


test('Test_BindEndDateMinDate_TestChange_ExpectMinDateSynced', () => {
   const startDateEl = document.createElement('input');
   const date = '2026-06-15';
   const emptyMinDate = 'today';
   const sets = [];
   const endDatePicker = {
      set(key, value) {
         sets.push({ key, value });
      },
   };
   startDateEl.value = date;

   ConsoleDatePickersHelper.bindEndDateMinDate(startDateEl, endDatePicker, {
      emptyMinDate,
   });

   assert.deepEqual(sets, [{ key: 'minDate', value: date }]);
});


test('Test_BindEndDateMinDate_TestBlankChange_ExpectEmptyMinDate', () => {
   const startDateEl = document.createElement('input');
   const date = '2026-06-15';
   const emptyMinDate = 'today';
   const sets = [];
   const endDatePicker = {
      set(key, value) {
         sets.push({ key, value });
      },
   };
   startDateEl.value = date;
   ConsoleDatePickersHelper.bindEndDateMinDate(startDateEl, endDatePicker, {
      emptyMinDate,
   });
   startDateEl.value = '   ';

   startDateEl.listeners.change();

   assert.deepEqual(sets.at(Position.SECOND), { key: 'minDate', value: emptyMinDate });
});
