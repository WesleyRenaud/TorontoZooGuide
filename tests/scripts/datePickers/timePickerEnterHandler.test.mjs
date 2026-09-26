import assert from 'node:assert/strict';
import test from 'node:test';

import { ReadOpenPickerFormatter } from '../../../scripts/datePickers/readOpenPickerFormatter.js';
import { TimePickerEnterHandler } from '../../../scripts/datePickers/timePickerEnterHandler.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ResolveOpenTimePickerValue_TestInputValue_ExpectPreferInput', () => {
   const original = ReadOpenPickerFormatter.readOpenPickerTime;
   const time = '1:00 PM';
   ReadOpenPickerFormatter.readOpenPickerTime = () => '3:00 PM';

   try {
      const resolved = TimePickerEnterHandler.resolveOpenTimePickerValue({ value: ` ${time} ` }, {});

      assert.equal(resolved, time);
   } finally {
      ReadOpenPickerFormatter.readOpenPickerTime = original;
   }
});


test('Test_ResolveOpenTimePickerValue_TestBlankInput_ExpectPickerTime', () => {
   const original = ReadOpenPickerFormatter.readOpenPickerTime;
   const pickerTime = '3:00 PM';
   ReadOpenPickerFormatter.readOpenPickerTime = () => pickerTime;

   try {
      const resolved = TimePickerEnterHandler.resolveOpenTimePickerValue({ value: '  ' }, {});

      assert.equal(resolved, pickerTime);
   } finally {
      ReadOpenPickerFormatter.readOpenPickerTime = original;
   }
});


test('Test_ResolveOpenTimePickerValue_TestNullInput_ExpectPickerTime', () => {
   const original = ReadOpenPickerFormatter.readOpenPickerTime;
   const pickerTime = '3:00 PM';
   ReadOpenPickerFormatter.readOpenPickerTime = () => pickerTime;

   try {
      const resolved = TimePickerEnterHandler.resolveOpenTimePickerValue(null, {});

      assert.equal(resolved, pickerTime);
   } finally {
      ReadOpenPickerFormatter.readOpenPickerTime = original;
   }
});


test('Test_CommitTimeToInput_TestSetDate_ExpectCommitted', () => {
   const time = '2:00 PM';
   const setDates = [];
   const closes = [];

   TimePickerEnterHandler.commitTimeToInput(time, {
      setDate: (...args) => { setDates.push(args); },
      close: () => { closes.push(true); },
   }, null);

   assert.deepEqual(setDates, [[time, true]]);
   assert.deepEqual(closes, [true]);
});


test('Test_CommitTimeToInput_TestFallback_ExpectInputValue', () => {
   const time = '4:00 PM';
   const inputEl = { value: '' };

   TimePickerEnterHandler.commitTimeToInput(time, { close: () => {} }, inputEl);

   assert.equal(inputEl.value, time);
});


test('Test_WireTimePickerEnterCommit_TestEnter_ExpectCommit', () => {
   const commits = [];
   const time = '11:00 AM';
   const inputEl = document.createElement('input');
   inputEl.value = time;
   const instance = {
      calendarContainer: document.createElement('div'),
   };

   TimePickerEnterHandler.wireTimePickerEnterCommit(inputEl, instance, (nextTime) => {
      commits.push(nextTime);
   });
   TimePickerEnterHandler.wireTimePickerEnterCommit(inputEl, instance, () => {});
   const prevented = [];
   inputEl.listeners.keydown({
      key: 'Enter',
      preventDefault: () => { prevented.push('default'); },
      stopImmediatePropagation: () => { prevented.push('stop'); },
   });

   assert.deepEqual(commits, [time]);
   assert.deepEqual(prevented, ['default', 'stop']);
});


test('Test_WireTimePickerEnterCommit_TestTab_ExpectNoCommit', () => {
   const commits = [];
   const time = '11:00 AM';
   const inputEl = document.createElement('input');
   inputEl.value = time;
   const instance = {
      calendarContainer: document.createElement('div'),
   };
   TimePickerEnterHandler.wireTimePickerEnterCommit(inputEl, instance, (nextTime) => {
      commits.push(nextTime);
   });

   inputEl.listeners.keydown({ key: 'Tab', preventDefault() {}, stopImmediatePropagation() {} });

   assert.deepEqual(commits, []);
});


test('Test_WireTimePickerEnterCommit_TestMissingArgs_ExpectNoop', () => {
   const wireMissingInput = () => TimePickerEnterHandler.wireTimePickerEnterCommit(null, {}, () => {});
   const wireMissingInstance = () => TimePickerEnterHandler.wireTimePickerEnterCommit({}, null, () => {});
   const wireMissingCommit = () => TimePickerEnterHandler.wireTimePickerEnterCommit({}, {}, null);

   assert.doesNotThrow(wireMissingInput);
   assert.doesNotThrow(wireMissingInstance);
   assert.doesNotThrow(wireMissingCommit);
});


test('Test_WireTimePickerEnterCommit_TestEnterEmpty_ExpectNoCommit', () => {
   const original = ReadOpenPickerFormatter.readOpenPickerTime;
   ReadOpenPickerFormatter.readOpenPickerTime = () => '';
   const commits = [];
   const inputEl = document.createElement('input');
   inputEl.value = '';
   const instance = {
      calendarContainer: document.createElement('div'),
   };

   try {
      TimePickerEnterHandler.wireTimePickerEnterCommit(inputEl, instance, (time) => {
         commits.push(time);
      });
      inputEl.listeners.keydown({
         key: 'Enter',
         preventDefault() {},
         stopImmediatePropagation() {},
      });

      assert.deepEqual(commits, []);
      assert.equal(commits.length, Position.FIRST);
   } finally {
      ReadOpenPickerFormatter.readOpenPickerTime = original;
   }
});
