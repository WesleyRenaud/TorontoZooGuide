import assert from 'node:assert/strict';
import test from 'node:test';

import { DatePickersBindingHelper } from '../../../../scripts/consoleOperations/bootstrap/datePickersBindingHelper.js';
import { ConsoleDateFactory } from '../../../../scripts/datePickers/consoleDateFactory.js';


test('Test_GetNestedValue_TestPath_ExpectValue', () => {
   const value = 3;
   const source = { a: { b: value } };
   const path = ['a', 'b'];

   const nested = DatePickersBindingHelper.getNestedValue(source, path);

   assert.equal(nested, value);
});


test('Test_GetNestedValue_TestMissingKey_ExpectUndefined', () => {
   const source = { a: {} };
   const path = ['a', 'missing'];

   const nested = DatePickersBindingHelper.getNestedValue(source, path);

   assert.equal(nested, undefined);
});


test('Test_InitDateRangePickerBinding_TestPath_ExpectFactory', () => {
   const startDateEl = 'start';
   const endDateEl = 'end';
   const refs = {
      form: { startDateEl, endDateEl },
   };
   const original = ConsoleDateFactory.initDateRangePickers;
   const calls = [];
   ConsoleDateFactory.initDateRangePickers = (...args) => {
      calls.push(args);
   };

   try {
      DatePickersBindingHelper.initDateRangePickerBinding(refs, ['form']);

      assert.deepEqual(calls, [[startDateEl, endDateEl]]);
   } finally {
      ConsoleDateFactory.initDateRangePickers = original;
   }
});


test('Test_InitSingleDatePickerBinding_TestPath_ExpectNullEnd', () => {
   const dateEl = 'only';
   const refs = { dateEl };
   const original = ConsoleDateFactory.initDateRangePickers;
   const calls = [];
   ConsoleDateFactory.initDateRangePickers = (...args) => {
      calls.push(args);
   };

   try {
      DatePickersBindingHelper.initSingleDatePickerBinding(refs, ['dateEl']);

      assert.deepEqual(calls, [[dateEl, null]]);
   } finally {
      ConsoleDateFactory.initDateRangePickers = original;
   }
});


test('Test_InitDateTimePickerBinding_TestTimeFieldKeys_ExpectTimePickers', () => {
   const open = 'o';
   const close = 'c';
   const refs = {
      times: { open, close },
   };
   const originalTime = ConsoleDateFactory.initTimePicker;
   const originalSchedule = ConsoleDateFactory.initScheduleDateTimePickers;
   const timeCalls = [];
   ConsoleDateFactory.initTimePicker = (el) => {
      timeCalls.push(el);
   };
   ConsoleDateFactory.initScheduleDateTimePickers = () => assert.fail('should not schedule');

   try {
      DatePickersBindingHelper.initDateTimePickerBinding(refs, {
         path: ['times'],
         timeFieldKeys: ['open', 'close'],
      });

      assert.deepEqual(timeCalls, [open, close]);
   } finally {
      ConsoleDateFactory.initTimePicker = originalTime;
      ConsoleDateFactory.initScheduleDateTimePickers = originalSchedule;
   }
});


test('Test_InitDateTimePickerBinding_TestSchedule_ExpectSchedulePickers', () => {
   const startDateEl = 'sd';
   const endDateEl = 'ed';
   const startTimeEl = 'st';
   const endTimeEl = 'et';
   const refs = {
      schedule: {
         startDateEl,
         endDateEl,
         startTimeEl,
         endTimeEl,
      },
   };
   const original = ConsoleDateFactory.initScheduleDateTimePickers;
   const calls = [];
   ConsoleDateFactory.initScheduleDateTimePickers = (...args) => {
      calls.push(args);
   };

   try {
      DatePickersBindingHelper.initDateTimePickerBinding(refs, {
         path: ['schedule'],
         startTimeKey: 'startTimeEl',
         endTimeKey: 'endTimeEl',
      });

      assert.deepEqual(calls, [[startDateEl, endDateEl, startTimeEl, endTimeEl]]);
   } finally {
      ConsoleDateFactory.initScheduleDateTimePickers = original;
   }
});
