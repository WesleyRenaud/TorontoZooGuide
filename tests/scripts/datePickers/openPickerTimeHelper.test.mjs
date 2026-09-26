import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDateFactory } from '../../../scripts/datePickers/consoleDateFactory.js';
import { OpenPickerTimeHelper } from '../../../scripts/datePickers/openPickerTimeHelper.js';


test('Test_GetPickerDateFormat_TestConfigured_ExpectFormat', () => {
   const dateFormat = 'H:i';
   const instance = { config: { dateFormat } };

   const format = OpenPickerTimeHelper.getPickerDateFormat(instance);

   assert.equal(format, dateFormat);
});


test('Test_GetPickerDateFormat_TestDefault_ExpectConsoleFormat', () => {
   const instance = {};

   const format = OpenPickerTimeHelper.getPickerDateFormat(instance);

   assert.equal(format, ConsoleDateFactory.CONSOLE_TIME_PICKER_OPTIONS.dateFormat);
});


test('Test_To24HourClock_TestAfternoon_ExpectConvertedHour', () => {
   const hour = 1;
   const period = 'PM';

   const converted = OpenPickerTimeHelper.to24HourClock(hour, period);

   assert.equal(converted, hour + 12);
});


test('Test_To24HourClock_TestMidnight_ExpectZero', () => {
   const hour = 12;
   const period = 'AM';

   const converted = OpenPickerTimeHelper.to24HourClock(hour, period);

   assert.equal(converted, 0);
});


test('Test_To24HourClock_TestMorning_ExpectSameHour', () => {
   const hour = 11;
   const period = 'AM';

   const converted = OpenPickerTimeHelper.to24HourClock(hour, period);

   assert.equal(converted, hour);
});


test('Test_To24HourClock_TestNoon_ExpectTwelve', () => {
   const hour = 12;
   const period = 'PM';

   const converted = OpenPickerTimeHelper.to24HourClock(hour, period);

   assert.equal(converted, hour);
});


test('Test_ReadTimeFromPickerControls_TestMissingControls_ExpectEmpty', () => {
   const instance = { hourElement: null, minuteElement: null };
   const dateFormat = 'H:i';

   const time = OpenPickerTimeHelper.readTimeFromPickerControls(instance, dateFormat);

   assert.equal(time, '');
});


test('Test_ReadTimeFromPickerControls_TestInvalidHour_ExpectEmpty', () => {
   const instance = {
      hourElement: { value: 'x' },
      minuteElement: { value: '05' },
      config: { time_24hr: true },
   };
   const dateFormat = 'H:i';

   const time = OpenPickerTimeHelper.readTimeFromPickerControls(instance, dateFormat);

   assert.equal(time, '');
});


test('Test_ReadTimeFromPickerControls_Test24HourValues_ExpectFormatted', () => {
   const dateFormat = 'H:i';
   const instance = {
      hourElement: { value: '9' },
      minuteElement: { value: '05' },
      config: { time_24hr: true },
      formatDate: (_date, format) => `formatted:${format}:09:05`,
   };

   const time = OpenPickerTimeHelper.readTimeFromPickerControls(instance, dateFormat);

   assert.equal(time, `formatted:${dateFormat}:09:05`);
});


test('Test_ReadTimeFromPickerControls_Test12HourPm_ExpectConverted', () => {
   const hour = 1;
   const minutes = 30;
   const dateFormat = 'H:i';
   const instance = {
      hourElement: { value: String(hour) },
      minuteElement: { value: String(minutes) },
      config: { time_24hr: false },
      amPM: { textContent: 'PM' },
      formatDate: (date) => `${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`,
   };

   const time = OpenPickerTimeHelper.readTimeFromPickerControls(instance, dateFormat);

   assert.equal(time, `${hour + 12}:${String(minutes).padStart(2, '0')}`);
});


test('Test_ReadTimeFromPickerControls_TestNaNHour_ExpectEmpty', () => {
   const instance = {
      hourElement: { value: 'abc' },
      minuteElement: { value: '05' },
      config: { time_24hr: true },
   };
   const dateFormat = 'H:i';

   const time = OpenPickerTimeHelper.readTimeFromPickerControls(instance, dateFormat);

   assert.equal(time, '');
});


test('Test_ReadTimeFromPickerControls_TestNaNMinute_ExpectEmpty', () => {
   const instance = {
      hourElement: { value: '9' },
      minuteElement: { value: 'xyz' },
      config: { time_24hr: true },
   };
   const dateFormat = 'H:i';

   const time = OpenPickerTimeHelper.readTimeFromPickerControls(instance, dateFormat);

   assert.equal(time, '');
});
