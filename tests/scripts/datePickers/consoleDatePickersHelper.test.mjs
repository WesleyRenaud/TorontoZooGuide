import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDatePickersHelper } from '../../../scripts/datePickers/consoleDatePickersHelper.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_InitDatePicker_TestOptions_ExpectMerged', () => {
   const calls = [];
   const inputEl = document.createElement('input');

   ConsoleDatePickersHelper.initDatePicker(inputEl, { allowInput: true }, (el, options) => {
      calls.push({ el, options });
      return { id: 'picker' };
   });

   assert.equal(calls.length, 1);
   assert.equal(calls[0].el, inputEl);
   assert.deepEqual(calls[0].options, {
      ...ConsoleDatePickersHelper.DATE_PICKER_OPTIONS,
      allowInput: true,
   });
});

test('Test_BindEndDateMinDate_TestMissingArgs_ExpectNoOp', () => {
   ConsoleDatePickersHelper.bindEndDateMinDate(null, { set() {} });
   ConsoleDatePickersHelper.bindEndDateMinDate(document.createElement('input'), null);
});

test('Test_BindEndDateMinDate_TestChange_ExpectMinDateSynced', () => {
   const startDateEl = document.createElement('input');
   const sets = [];
   const endDatePicker = {
      set(key, value) {
         sets.push({ key, value });
      },
   };

   startDateEl.value = '2026-06-15';
   ConsoleDatePickersHelper.bindEndDateMinDate(startDateEl, endDatePicker, {
      emptyMinDate: 'today',
   });

   assert.deepEqual(sets, [{ key: 'minDate', value: '2026-06-15' }]);

   startDateEl.value = '   ';
   startDateEl.listeners.change();
   assert.deepEqual(sets[1], { key: 'minDate', value: 'today' });
});
