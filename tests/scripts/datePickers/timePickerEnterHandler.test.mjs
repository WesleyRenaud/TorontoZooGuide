import assert from 'node:assert/strict';
import test from 'node:test';

import { TimePickerEnterHandler } from '../../../scripts/datePickers/timePickerEnterHandler.js';
import { ReadOpenPickerFormatter } from '../../../scripts/datePickers/readOpenPickerFormatter.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ResolveOpenTimePickerValue_TestInputAndInstance_ExpectPreferInput', () => {
   const original = ReadOpenPickerFormatter.readOpenPickerTime;
   ReadOpenPickerFormatter.readOpenPickerTime = () => '3:00 PM';

   try {
      assert.equal(
         TimePickerEnterHandler.resolveOpenTimePickerValue({ value: ' 1:00 PM ' }, {}),
         '1:00 PM'
      );
      assert.equal(
         TimePickerEnterHandler.resolveOpenTimePickerValue({ value: '  ' }, {}),
         '3:00 PM'
      );
      assert.equal(
         TimePickerEnterHandler.resolveOpenTimePickerValue(null, {}),
         '3:00 PM'
      );
   } finally {
      ReadOpenPickerFormatter.readOpenPickerTime = original;
   }
});

test('Test_CommitTimeToInput_TestSetDateAndFallback_ExpectCommitted', () => {
   const setDates = [];
   const closes = [];
   TimePickerEnterHandler.commitTimeToInput('2:00 PM', {
      setDate: (...args) => { setDates.push(args); },
      close: () => { closes.push(true); },
   }, null);
   assert.deepEqual(setDates, [['2:00 PM', true]]);
   assert.deepEqual(closes, [true]);

   const inputEl = { value: '' };
   TimePickerEnterHandler.commitTimeToInput('4:00 PM', { close: () => { closes.push(true); } }, inputEl);
   assert.equal(inputEl.value, '4:00 PM');
});

test('Test_WireTimePickerEnterCommit_TestEnter_ExpectCommit', () => {
   const commits = [];
   const inputEl = document.createElement('input');
   inputEl.value = '11:00 AM';
   const instance = {
      calendarContainer: document.createElement('div'),
   };

   TimePickerEnterHandler.wireTimePickerEnterCommit(inputEl, instance, (time) => {
      commits.push(time);
   });
   TimePickerEnterHandler.wireTimePickerEnterCommit(inputEl, instance, () => {});

   const prevented = [];
   inputEl.listeners.keydown({
      key: 'Enter',
      preventDefault: () => { prevented.push('default'); },
      stopImmediatePropagation: () => { prevented.push('stop'); },
   });
   assert.deepEqual(commits, ['11:00 AM']);
   assert.deepEqual(prevented, ['default', 'stop']);

   inputEl.listeners.keydown({ key: 'Tab', preventDefault() {}, stopImmediatePropagation() {} });
   assert.deepEqual(commits, ['11:00 AM']);
});

test('Test_WireTimePickerEnterCommit_TestMissingArgs_ExpectNoop', () => {
   TimePickerEnterHandler.wireTimePickerEnterCommit(null, {}, () => {});
   TimePickerEnterHandler.wireTimePickerEnterCommit({}, null, () => {});
   TimePickerEnterHandler.wireTimePickerEnterCommit({}, {}, null);
});
