import assert from 'node:assert/strict';
import test from 'node:test';

import { DatePickersBindingHelper } from '../../../../scripts/consoleOperations/bootstrap/datePickersBindingHelper.js';
import { ConsoleDateFactory } from '../../../../scripts/datePickers/consoleDateFactory.js';

test('Test_GetNestedValue_TestPath_ExpectValue', () => {
   assert.equal(DatePickersBindingHelper.getNestedValue({ a: { b: 3 } }, ['a', 'b']), 3);
   assert.equal(DatePickersBindingHelper.getNestedValue({ a: {} }, ['a', 'missing']), undefined);
});

test('Test_InitDateRangePickerBinding_TestPath_ExpectFactory', () => {
   const calls = [];
   const original = ConsoleDateFactory.initDateRangePickers;
   ConsoleDateFactory.initDateRangePickers = (...args) => { calls.push(args); };

   try {
      DatePickersBindingHelper.initDateRangePickerBinding({
         form: { startDateEl: 'start', endDateEl: 'end' },
      }, ['form']);
      assert.deepEqual(calls, [['start', 'end']]);
   } finally {
      ConsoleDateFactory.initDateRangePickers = original;
   }
});

test('Test_InitSingleDatePickerBinding_TestPath_ExpectNullEnd', () => {
   const calls = [];
   const original = ConsoleDateFactory.initDateRangePickers;
   ConsoleDateFactory.initDateRangePickers = (...args) => { calls.push(args); };

   try {
      DatePickersBindingHelper.initSingleDatePickerBinding({ dateEl: 'only' }, ['dateEl']);
      assert.deepEqual(calls, [['only', null]]);
   } finally {
      ConsoleDateFactory.initDateRangePickers = original;
   }
});

test('Test_InitDateTimePickerBinding_TestTimeFieldKeys_ExpectTimePickers', () => {
   const timeCalls = [];
   const originalTime = ConsoleDateFactory.initTimePicker;
   const originalSchedule = ConsoleDateFactory.initScheduleDateTimePickers;
   ConsoleDateFactory.initTimePicker = (el) => { timeCalls.push(el); };
   ConsoleDateFactory.initScheduleDateTimePickers = () => assert.fail('should not schedule');

   try {
      DatePickersBindingHelper.initDateTimePickerBinding({
         times: { open: 'o', close: 'c' },
      }, {
         path: ['times'],
         timeFieldKeys: ['open', 'close'],
      });
      assert.deepEqual(timeCalls, ['o', 'c']);
   } finally {
      ConsoleDateFactory.initTimePicker = originalTime;
      ConsoleDateFactory.initScheduleDateTimePickers = originalSchedule;
   }
});

test('Test_InitDateTimePickerBinding_TestSchedule_ExpectSchedulePickers', () => {
   const calls = [];
   const original = ConsoleDateFactory.initScheduleDateTimePickers;
   ConsoleDateFactory.initScheduleDateTimePickers = (...args) => { calls.push(args); };

   try {
      DatePickersBindingHelper.initDateTimePickerBinding({
         schedule: {
            startDateEl: 'sd',
            endDateEl: 'ed',
            startTimeEl: 'st',
            endTimeEl: 'et',
         },
      }, {
         path: ['schedule'],
         startTimeKey: 'startTimeEl',
         endTimeKey: 'endTimeEl',
      });
      assert.deepEqual(calls, [['sd', 'ed', 'st', 'et']]);
   } finally {
      ConsoleDateFactory.initScheduleDateTimePickers = original;
   }
});
