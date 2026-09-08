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
   const time = ReadOpenPickerFormatter.readOpenPickerTime(_createMockPickerInstance());

   assert.equal(time, '12:00 PM');
});

test('Test_ReadOpenPickerTime_TestSelectedDatesPresent_ExpectSelectedOverControls', () => {
   const selectedDate = new Date();
   selectedDate.setHours(14, 30, 0, 0);

   const time = ReadOpenPickerFormatter.readOpenPickerTime(_createMockPickerInstance({
      selectedDates: [ selectedDate ],
   }));

   assert.equal(time, '2:30 PM');
});

test('Test_ReadOpenPickerTime_TestClosedPicker_ExpectEmpty', () => {
   assert.equal(
      ReadOpenPickerFormatter.readOpenPickerTime(_createMockPickerInstance({ isOpen: false })),
      ''
   );
   assert.equal(ReadOpenPickerFormatter.readOpenPickerTime(null), '');
});

test('Test_ReadOpenPickerTime_TestLatestSelectedFallback_ExpectFormatted', () => {
   const latestSelectedDateObj = new Date();
   latestSelectedDateObj.setHours(9, 15, 0, 0);

   const time = ReadOpenPickerFormatter.readOpenPickerTime(_createMockPickerInstance({
      selectedDates: [],
      hourElement: { value: '' },
      minuteElement: { value: '' },
      amPM: { textContent: '' },
      latestSelectedDateObj,
   }));

   assert.equal(time, '9:15 AM');
});
