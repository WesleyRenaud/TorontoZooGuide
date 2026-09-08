import assert from 'node:assert/strict';
import test from 'node:test';

import { DateFactory } from '../../../../scripts/consoleOperations/bootstrap/dateFactory.js';
import { DatePickersBindingHelper } from '../../../../scripts/consoleOperations/bootstrap/datePickersBindingHelper.js';
import { ConsoleDateFactory } from '../../../../scripts/datePickers/consoleDateFactory.js';

test('Test_WireConsoleOperationDatePickers_TestBindings_ExpectHelpersCalled', () => {
   const rangeCalls = [];
   const singleCalls = [];
   const dateTimeCalls = [];
   const originalRange = DatePickersBindingHelper.initDateRangePickerBinding;
   const originalSingle = DatePickersBindingHelper.initSingleDatePickerBinding;
   const originalDateTime = DatePickersBindingHelper.initDateTimePickerBinding;
   const originalHours = ConsoleDateFactory.initAttractionHoursSchedulePickers;

   DatePickersBindingHelper.initDateRangePickerBinding = (refs, path) => {
      rangeCalls.push(path);
   };
   DatePickersBindingHelper.initSingleDatePickerBinding = (refs, path) => {
      singleCalls.push(path);
   };
   DatePickersBindingHelper.initDateTimePickerBinding = (refs, binding) => {
      dateTimeCalls.push(binding);
   };
   ConsoleDateFactory.initAttractionHoursSchedulePickers = () => ({ wired: true });

   try {
      const refs = {
         attractions: {
            hoursSchedule: { start: 's' },
         },
      };
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
