import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RecurringScheduleBuilder } from '../../../../scripts/consoleOperations/forms/recurringScheduleBuilder.js';

test('Test_NormalizeRecurringScheduleRow_TestTimeAndDays_ExpectFormattedFlags', () => {
   assert.deepEqual(
      RecurringScheduleBuilder.normalizeRecurringScheduleRow({
         time: '2:30 PM',
         monday: true,
         tuesday: false,
         wednesday: true,
      }),
      {
         time: '2:30 PM',
         monday: true,
         tuesday: false,
         wednesday: true,
         thursday: false,
         friday: false,
         saturday: false,
         sunday: false,
      }
   );
});

test('Test_ValidateRecurringScheduleRows_TestInvalidAndValidRows_ExpectMessagesOrNull', () => {
   assert.match(
      RecurringScheduleBuilder.validateRecurringScheduleRows([]) ?? '',
      /Encounter times/
   );

   assert.match(
      RecurringScheduleBuilder.validateRecurringScheduleRows([
         { time: '', monday: true },
      ]) ?? '',
      /Encounter time/
   );

   assert.match(
      RecurringScheduleBuilder.validateRecurringScheduleRows([
         { time: '11:00 AM', monday: false, tuesday: false },
      ]) ?? '',
      /at least one day/i
   );

   assert.match(
      RecurringScheduleBuilder.validateRecurringScheduleRows([
         { time: '11:00 AM', monday: true },
         { time: '11:00 AM', tuesday: true },
      ]) ?? '',
      /only be added once/i
   );

   assert.equal(
      RecurringScheduleBuilder.validateRecurringScheduleRows([
         { time: '11:00 AM', monday: true },
         { time: '2:30 PM', saturday: true, sunday: true },
      ]),
      null
   );
});
