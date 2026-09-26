import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RecurringScheduleBuilder } from '../../../../scripts/consoleOperations/forms/recurringScheduleBuilder.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_NormalizeRecurringScheduleRow_TestTimeAndDays_ExpectFormattedFlags', () => {
   const time = '2:30 PM';
   const monday = true;
   const tuesday = false;
   const wednesday = true;

   const row = RecurringScheduleBuilder.normalizeRecurringScheduleRow({
      time,
      monday,
      tuesday,
      wednesday,
   });

   assert.deepEqual(row, {
      time,
      monday,
      tuesday,
      wednesday,
      thursday: false,
      friday: false,
      saturday: false,
      sunday: false,
   });
});


test('Test_ValidateRecurringScheduleRows_TestEmpty_ExpectEncounterTimesMessage', () => {
   const message = RecurringScheduleBuilder.validateRecurringScheduleRows([]);

   assert.equal(
      message,
      Strings.validation.entityRequired(Strings.labels.encounterTimes)
   );
});


test('Test_ValidateRecurringScheduleRows_TestMissingTime_ExpectEncounterTimeMessage', () => {
   const rows = [{ time: '', monday: true }];

   const message = RecurringScheduleBuilder.validateRecurringScheduleRows(rows);

   assert.equal(
      message,
      Strings.validation.entityRequired(Strings.labels.encounterTime)
   );
});


test('Test_ValidateRecurringScheduleRows_TestNoDays_ExpectAtLeastOneDay', () => {
   const rows = [{ time: '11:00 AM', monday: false, tuesday: false }];

   const message = RecurringScheduleBuilder.validateRecurringScheduleRows(rows);

   assert.equal(message, Strings.validation.encounterScheduleRowNeedsDay);
});


test('Test_ValidateRecurringScheduleRows_TestDuplicateTime_ExpectOnceMessage', () => {
   const time = '11:00 AM';
   const rows = [
      { time, monday: true },
      { time, tuesday: true },
   ];

   const message = RecurringScheduleBuilder.validateRecurringScheduleRows(rows);

   assert.equal(message, Strings.validation.duplicateEncounterTime);
});


test('Test_ValidateRecurringScheduleRows_TestValidRows_ExpectNull', () => {
   const morning = '11:00 AM';
   const afternoon = '2:30 PM';
   const rows = [
      { time: morning, monday: true },
      { time: afternoon, saturday: true, sunday: true },
   ];

   const message = RecurringScheduleBuilder.validateRecurringScheduleRows(rows);

   assert.equal(message, null);
});
