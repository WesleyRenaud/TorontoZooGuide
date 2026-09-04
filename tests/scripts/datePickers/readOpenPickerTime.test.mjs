import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ReadOpenPickerTime } from '../../../scripts/datePickers/readOpenPickerTime.js';
function createMockPickerInstance(overrides = {}) {
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
   const time = ReadOpenPickerTime.readOpenPickerTime(createMockPickerInstance());

   assert.equal(time, '12:00 PM');
});

test('Test_ReadOpenPickerTime_TestSelectedDatesPresent_ExpectSelectedOverControls', () => {
   const selectedDate = new Date();
   selectedDate.setHours(14, 30, 0, 0);

   const time = ReadOpenPickerTime.readOpenPickerTime(createMockPickerInstance({
      selectedDates: [ selectedDate ],
   }));

   assert.equal(time, '2:30 PM');
});
