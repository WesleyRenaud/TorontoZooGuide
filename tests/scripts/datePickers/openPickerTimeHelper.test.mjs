import assert from 'node:assert/strict';
import test from 'node:test';

import { OpenPickerTimeHelper } from '../../../scripts/datePickers/openPickerTimeHelper.js';
import { ConsoleDateFactory } from '../../../scripts/datePickers/consoleDateFactory.js';

test('Test_GetPickerDateFormat_TestConfiguredAndDefault_ExpectFormat', () => {
   assert.equal(
      OpenPickerTimeHelper.getPickerDateFormat({ config: { dateFormat: 'H:i' } }),
      'H:i'
   );
   assert.equal(
      OpenPickerTimeHelper.getPickerDateFormat({}),
      ConsoleDateFactory.CONSOLE_TIME_PICKER_OPTIONS.dateFormat
   );
});

test('Test_To24HourClock_TestAmPm_ExpectConvertedHour', () => {
   assert.equal(OpenPickerTimeHelper.to24HourClock(1, 'PM'), 13);
   assert.equal(OpenPickerTimeHelper.to24HourClock(12, 'AM'), 0);
   assert.equal(OpenPickerTimeHelper.to24HourClock(11, 'AM'), 11);
   assert.equal(OpenPickerTimeHelper.to24HourClock(12, 'PM'), 12);
});

test('Test_ReadTimeFromPickerControls_TestMissingControls_ExpectEmpty', () => {
   assert.equal(
      OpenPickerTimeHelper.readTimeFromPickerControls({ hourElement: null, minuteElement: null }, 'H:i'),
      ''
   );
});

test('Test_ReadTimeFromPickerControls_Test24HourValues_ExpectFormatted', () => {
   const instance = {
      hourElement: { value: '9' },
      minuteElement: { value: '05' },
      config: { time_24hr: true },
      formatDate: (_date, dateFormat) => `formatted:${dateFormat}:09:05`,
   };

   assert.equal(
      OpenPickerTimeHelper.readTimeFromPickerControls(instance, 'H:i'),
      'formatted:H:i:09:05'
   );
});

test('Test_ReadTimeFromPickerControls_Test12HourPm_ExpectConverted', () => {
   const instance = {
      hourElement: { value: '1' },
      minuteElement: { value: '30' },
      config: { time_24hr: false },
      amPM: { textContent: 'PM' },
      formatDate: (date) => `${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`,
   };

   assert.equal(OpenPickerTimeHelper.readTimeFromPickerControls(instance, 'H:i'), '13:30');
});
