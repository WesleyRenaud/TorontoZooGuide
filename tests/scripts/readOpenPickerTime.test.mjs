import assert from 'node:assert/strict';
import { test } from 'node:test';

import { readOpenPickerTime } from '../../scripts/datePickers/readOpenPickerTime.js';
import { createDomNode } from './helpers/domNodeMock.mjs';

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

test('readOpenPickerTime reads the open picker default time controls', () => {
   const time = readOpenPickerTime(createMockPickerInstance());

   assert.equal(time, '12:00 PM');
});

test('readOpenPickerTime prefers selectedDates over picker controls', () => {
   const selectedDate = new Date();
   selectedDate.setHours(14, 30, 0, 0);

   const time = readOpenPickerTime(createMockPickerInstance({
      selectedDates: [ selectedDate ],
   }));

   assert.equal(time, '2:30 PM');
});
