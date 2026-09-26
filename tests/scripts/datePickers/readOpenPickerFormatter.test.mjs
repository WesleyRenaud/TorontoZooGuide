import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ReadOpenPickerFormatter } from '../../../scripts/datePickers/readOpenPickerFormatter.js';


function _createMockPickerInstance(overrides = {}) {
   return {
      isOpen: true,
      config: {
         dateFormat: 'h:i K',
         time_24hr: false,
      },
      selectedDates: [],
      hourElement: { value: '12' },
      minuteElement: { value: '00' },
      amPM: { textContent: 'PM' },
      formatDate(date) {
         const hours = date.getHours();
         const minutes = String(date.getMinutes()).padStart(2, '0');
         const isPm = hours >= 12;
         const displayHour = hours % 12 || 12;

         return `${displayHour}:${minutes} ${isPm ? 'PM' : 'AM'}`;
      },
      ...overrides,
   };
}


test('Test_ReadOpenPickerTime_TestOpenDefaultControls_ExpectControlTime', () => {
   const instance = _createMockPickerInstance();

   const time = ReadOpenPickerFormatter.readOpenPickerTime(instance);

   assert.equal(time, `${instance.hourElement.value}:${instance.minuteElement.value} ${instance.amPM.textContent}`);
});


test('Test_ReadOpenPickerTime_TestSelectedDatesPresent_ExpectSelectedOverControls', () => {
   const hours = 14;
   const minutes = 30;
   const selectedDate = new Date();
   selectedDate.setHours(hours, minutes, 0, 0);
   const instance = _createMockPickerInstance({
      selectedDates: [selectedDate],
   });

   const time = ReadOpenPickerFormatter.readOpenPickerTime(instance);

   assert.equal(time, instance.formatDate(selectedDate));
});


test('Test_ReadOpenPickerTime_TestClosedPicker_ExpectEmpty', () => {
   const instance = _createMockPickerInstance({ isOpen: false });

   const time = ReadOpenPickerFormatter.readOpenPickerTime(instance);

   assert.equal(time, '');
});


test('Test_ReadOpenPickerTime_TestNull_ExpectEmpty', () => {
   const instance = null;

   const time = ReadOpenPickerFormatter.readOpenPickerTime(instance);

   assert.equal(time, '');
});


test('Test_ReadOpenPickerTime_TestLatestSelectedFallback_ExpectFormatted', () => {
   const hours = 9;
   const minutes = 15;
   const latestSelectedDateObj = new Date();
   latestSelectedDateObj.setHours(hours, minutes, 0, 0);
   const instance = _createMockPickerInstance({
      selectedDates: [],
      hourElement: { value: '' },
      minuteElement: { value: '' },
      amPM: { textContent: '' },
      latestSelectedDateObj,
   });

   const time = ReadOpenPickerFormatter.readOpenPickerTime(instance);

   assert.equal(time, instance.formatDate(latestSelectedDateObj));
});
