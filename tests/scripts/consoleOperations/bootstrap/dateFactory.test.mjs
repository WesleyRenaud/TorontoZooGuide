import assert from 'node:assert/strict';
import test from 'node:test';

import { DateFactory } from '../../../../scripts/consoleOperations/bootstrap/dateFactory.js';
import { DatePickersBindingHelper } from '../../../../scripts/consoleOperations/bootstrap/datePickersBindingHelper.js';
import { ConsoleDateFactory } from '../../../../scripts/datePickers/consoleDateFactory.js';


test('Test_WireConsoleOperationDatePickers_TestBindings_ExpectHelpersCalled', () => {
   const refs = {
      attractions: {
         hoursSchedule: { start: 's' },
      },
   };
   const originalRange = DatePickersBindingHelper.initDateRangePickerBinding;
   const originalSingle = DatePickersBindingHelper.initSingleDatePickerBinding;
   const originalDateTime = DatePickersBindingHelper.initDateTimePickerBinding;
   const originalHours = ConsoleDateFactory.initAttractionHoursSchedulePickers;
   const rangeCalls = [];
   const singleCalls = [];
   const dateTimeCalls = [];
   DatePickersBindingHelper.initDateRangePickerBinding = (_wiredRefs, path) => {
      rangeCalls.push(path);
   };
   DatePickersBindingHelper.initSingleDatePickerBinding = (_wiredRefs, path) => {
      singleCalls.push(path);
   };
   DatePickersBindingHelper.initDateTimePickerBinding = (_wiredRefs, binding) => {
      dateTimeCalls.push(binding);
   };
   ConsoleDateFactory.initAttractionHoursSchedulePickers = () => ({ wired: true });

   try {
      DateFactory.wireConsoleOperationDatePickers(refs);

      assert.equal(rangeCalls.length, DateFactory.DATE_PICKER_BINDINGS.dateRanges.length);
      assert.equal(singleCalls.length, DateFactory.DATE_PICKER_BINDINGS.singleDates.length);
      assert.equal(dateTimeCalls.length, DateFactory.DATE_PICKER_BINDINGS.dateTimes.length);
      assert.equal(refs.attractions.hoursSchedule.wired, true);
   } finally {
      DatePickersBindingHelper.initDateRangePickerBinding = originalRange;
      DatePickersBindingHelper.initSingleDatePickerBinding = originalSingle;
      DatePickersBindingHelper.initDateTimePickerBinding = originalDateTime;
      ConsoleDateFactory.initAttractionHoursSchedulePickers = originalHours;
   }
});
