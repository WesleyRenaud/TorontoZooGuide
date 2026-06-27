import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   initDateRangePickers,
   initScheduleDateTimePickers,
   initTimePicker,
} from '../../scripts/datePickers/consoleDatePickers.js';
import { createDomNode } from './helpers/domNodeMock.mjs';

function createFlatpickrSpy() {
   const calls = [];

   return {
      calls,
      initFlatpickrFn: (inputEl, options) => {
         calls.push({ inputEl, options });

         return {
            close() {},
            set(property, value) {
               this[property] = value;
            },
            setDate() {
               inputEl.value = '';
            },
         };
      },
   };
}

test('initTimePicker wires console time picker defaults', () => {
   const inputEl = createDomNode('input');
   const { calls, initFlatpickrFn } = createFlatpickrSpy();

   initTimePicker(inputEl, {}, initFlatpickrFn);

   assert.equal(calls.length, 1);
   assert.equal(calls[0].options.enableTime, true);
   assert.equal(calls[0].options.noCalendar, true);
   assert.equal(calls[0].options.dateFormat, 'h:i K');
});

test('initDateRangePickers binds end-date minDate to the start input', () => {
   const startDateEl = createDomNode('input');
   const endDateEl = createDomNode('input');
   const { calls, initFlatpickrFn } = createFlatpickrSpy();

   startDateEl.value = '2026-06-15';

   const { endPicker } = initDateRangePickers(startDateEl, endDateEl, {
      minDate: '2026-06-01',
      initFlatpickrFn,
   });

   assert.equal(calls.length, 2);
   assert.equal(calls[0].options.minDate, '2026-06-01');
   assert.equal(calls[1].options.minDate, '2026-06-01');
   assert.equal(endPicker.minDate, '2026-06-15');

   startDateEl.value = '2026-06-20';
   startDateEl.listeners.change?.();

   assert.equal(endPicker.minDate, '2026-06-20');
});

test('initScheduleDateTimePickers initializes all four pickers', () => {
   const startDateEl = createDomNode('input');
   const endDateEl = createDomNode('input');
   const dailyStartTimeEl = createDomNode('input');
   const dailyEndTimeEl = createDomNode('input');
   const { calls, initFlatpickrFn } = createFlatpickrSpy();

   const pickers = initScheduleDateTimePickers(
      startDateEl,
      endDateEl,
      dailyStartTimeEl,
      dailyEndTimeEl,
      { initFlatpickrFn }
   );

   assert.equal(calls.length, 4);
   assert.equal(calls[0].inputEl, startDateEl);
   assert.equal(calls[1].inputEl, endDateEl);
   assert.equal(calls[2].inputEl, dailyStartTimeEl);
   assert.equal(calls[3].inputEl, dailyEndTimeEl);
   assert.equal(calls[2].options.enableTime, true);
   assert.ok(pickers.startDatePicker);
   assert.ok(pickers.dailyEndTimePicker);
});
