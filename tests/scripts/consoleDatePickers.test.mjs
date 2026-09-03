import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   initDateRangePickers,
   initScheduleDateTimePickers,
   initTimePicker,
} from '../../scripts/datePickers/consoleDatePickers.js';
import { createDomNode } from './helpers/domNodeMock.mjs';

function createMockPickerInstance(inputEl, overrides = {}) {
   return {
      close() {
         this.isOpen = false;
      },
      isOpen: true,
      config: {
         dateFormat: 'h:i K',
         time_24hr: false,
      },
      selectedDates: [],
      hourElement: { value: '12' },
      minuteElement: { value: '00' },
      amPM: { textContent: 'PM' },
      calendarContainer: createDomNode('div'),
      formatDate(date) {
         const hours = date.getHours();
         const minutes = String(date.getMinutes()).padStart(2, '0');
         const isPm = hours >= 12;
         const displayHour = hours % 12 || 12;

         return `${displayHour}:${minutes} ${isPm ? 'PM' : 'AM'}`;
      },
      setDate(time) {
         inputEl.value = time;
         this.selectedDates = [ new Date() ];
      },
      set(property, value) {
         this[property] = value;
      },
      ...overrides,
   };
}

function createFlatpickrSpy() {
   const calls = [];

   return {
      calls,
      initFlatpickrFn: (inputEl, options) => {
         calls.push({ inputEl, options });

         const instance = createMockPickerInstance(inputEl);
         options.onReady?.([], '', instance);
         return instance;
      },
   };
}

function dispatchKeydown(target, key) {
   target.listeners.keydown?.({
      key,
      preventDefault() {},
      stopImmediatePropagation() {},
   });
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

test('initTimePicker populates the field from the open picker on Enter', () => {
   const inputEl = createDomNode('input');
   const { initFlatpickrFn } = createFlatpickrSpy();
   const picker = initTimePicker(inputEl, {}, initFlatpickrFn);

   dispatchKeydown(inputEl, 'Enter');

   assert.equal(inputEl.value, '12:00 PM');
   assert.equal(picker.isOpen, false);
});

test('initTimePicker populates the field from calendar Enter when the input is empty', () => {
   const inputEl = createDomNode('input');
   const { initFlatpickrFn } = createFlatpickrSpy();
   const picker = initTimePicker(inputEl, {}, initFlatpickrFn);

   dispatchKeydown(picker.calendarContainer, 'Enter');

   assert.equal(inputEl.value, '12:00 PM');
   assert.equal(picker.isOpen, false);
});

test('initTimePicker keeps typed input on Enter', () => {
   const inputEl = createDomNode('input');
   const { initFlatpickrFn } = createFlatpickrSpy();

   initTimePicker(inputEl, {}, initFlatpickrFn);
   inputEl.value = '2:30 PM';
   dispatchKeydown(inputEl, 'Enter');

   assert.equal(inputEl.value, '2:30 PM');
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
