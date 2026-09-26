import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ConsoleDateFactory } from '../../../scripts/datePickers/consoleDateFactory.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';


function _createMockPickerInstance(inputEl, overrides = {}) {
   return {
      close() {
         this.isOpen = false;
      },
      isOpen: true,
      config: {
         dateFormat: ConsoleDateFactory.CONSOLE_TIME_PICKER_OPTIONS.dateFormat,
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
         this.selectedDates = [new Date()];
      },
      set(property, value) {
         this[property] = value;
      },
      ...overrides,
   };
}


function _createFlatpickrSpy() {
   const calls = [];

   return {
      calls,
      initFlatpickrFn: (inputEl, options) => {
         calls.push({ inputEl, options });
         const instance = _createMockPickerInstance(inputEl);
         options.onReady?.([], '', instance);
         return instance;
      },
   };
}


function _dispatchKeydown(target, key) {
   target.listeners.keydown?.({
      key,
      preventDefault() {},
      stopImmediatePropagation() {},
   });
}


test('Test_InitTimePicker_TestDefaults_ExpectConsoleOptions', () => {
   const inputEl = createDomNode('input');
   const { calls, initFlatpickrFn } = _createFlatpickrSpy();

   ConsoleDateFactory.initTimePicker(inputEl, {}, initFlatpickrFn);
   const options = calls.at(Position.FIRST).options;

   assert.equal(calls.length, Position.SECOND);
   assert.equal(options.enableTime, ConsoleDateFactory.CONSOLE_TIME_PICKER_OPTIONS.enableTime);
   assert.equal(options.noCalendar, ConsoleDateFactory.CONSOLE_TIME_PICKER_OPTIONS.noCalendar);
   assert.equal(options.dateFormat, ConsoleDateFactory.CONSOLE_TIME_PICKER_OPTIONS.dateFormat);
});


test('Test_InitTimePicker_TestEnterFromPicker_ExpectPopulated', () => {
   const inputEl = createDomNode('input');
   const { initFlatpickrFn } = _createFlatpickrSpy();
   const picker = ConsoleDateFactory.initTimePicker(inputEl, {}, initFlatpickrFn);
   const expected = `${picker.hourElement.value}:${picker.minuteElement.value} ${picker.amPM.textContent}`;

   _dispatchKeydown(inputEl, 'Enter');

   assert.equal(inputEl.value, expected);
   assert.equal(picker.isOpen, false);
});


test('Test_InitTimePicker_TestCalendarEnterEmpty_ExpectPopulated', () => {
   const inputEl = createDomNode('input');
   const { initFlatpickrFn } = _createFlatpickrSpy();
   const picker = ConsoleDateFactory.initTimePicker(inputEl, {}, initFlatpickrFn);
   const expected = `${picker.hourElement.value}:${picker.minuteElement.value} ${picker.amPM.textContent}`;

   _dispatchKeydown(picker.calendarContainer, 'Enter');

   assert.equal(inputEl.value, expected);
   assert.equal(picker.isOpen, false);
});


test('Test_InitTimePicker_TestEnterTyped_ExpectKept', () => {
   const inputEl = createDomNode('input');
   const { initFlatpickrFn } = _createFlatpickrSpy();
   const time = '2:30 PM';
   ConsoleDateFactory.initTimePicker(inputEl, {}, initFlatpickrFn);
   inputEl.value = time;

   _dispatchKeydown(inputEl, 'Enter');

   assert.equal(inputEl.value, time);
});


test('Test_InitDateRangePickers_TestStartChange_ExpectEndMinDate', () => {
   const startDateEl = createDomNode('input');
   const endDateEl = createDomNode('input');
   const { calls, initFlatpickrFn } = _createFlatpickrSpy();
   const minDate = '2026-06-01';
   const startDate = '2026-06-15';
   const nextStartDate = '2026-06-20';
   startDateEl.value = startDate;

   const { endPicker } = ConsoleDateFactory.initDateRangePickers(startDateEl, endDateEl, {
      minDate,
      initFlatpickrFn,
   });
   startDateEl.value = nextStartDate;
   startDateEl.listeners.change?.();

   assert.equal(calls.length, 2);
   assert.equal(calls.at(Position.FIRST).options.minDate, minDate);
   assert.equal(calls.at(Position.SECOND).options.minDate, minDate);
   assert.equal(endPicker.minDate, nextStartDate);
});


test('Test_InitScheduleDateTimePickers_TestFourInputs_ExpectInitialized', () => {
   const startDateEl = createDomNode('input');
   const endDateEl = createDomNode('input');
   const dailyStartTimeEl = createDomNode('input');
   const dailyEndTimeEl = createDomNode('input');
   const { calls, initFlatpickrFn } = _createFlatpickrSpy();

   const pickers = ConsoleDateFactory.initScheduleDateTimePickers(
      startDateEl,
      endDateEl,
      dailyStartTimeEl,
      dailyEndTimeEl,
      { initFlatpickrFn }
   );

   assert.equal(calls.length, 4);
   assert.equal(calls.at(Position.FIRST).inputEl, startDateEl);
   assert.equal(calls.at(Position.SECOND).inputEl, endDateEl);
   assert.equal(calls.at(Position.THIRD).inputEl, dailyStartTimeEl);
   assert.equal(calls.at(Position.FOURTH).inputEl, dailyEndTimeEl);
   assert.equal(calls.at(Position.THIRD).options.enableTime, true);
   assert.ok(pickers.startDatePicker);
   assert.ok(pickers.dailyEndTimePicker);
});


test('Test_InitTimePicker_TestMissingInput_ExpectNull', () => {
   const inputEl = null;

   const picker = ConsoleDateFactory.initTimePicker(inputEl);

   assert.equal(picker, null);
});


test('Test_ApplyScheduleTimePickerBounds_TestMissingPicker_ExpectNoOp', () => {
   const apply = () => ConsoleDateFactory.applyScheduleTimePickerBounds(null, {
      openTime: '09:00 AM',
      closeTime: '05:00 PM',
   });

   assert.doesNotThrow(apply);
});


test('Test_ApplyScheduleTimePickerBounds_TestMissingBounds_ExpectCleared', () => {
   const picker = { sets: [], set(property, value) { this.sets.push([property, value]); } };

   ConsoleDateFactory.applyScheduleTimePickerBounds(picker, null);

   assert.deepEqual(picker.sets, [
      ['minTime', null],
      ['maxTime', null],
   ]);
});


test('Test_ApplyScheduleTimePickerBounds_TestPartialBounds_ExpectCleared', () => {
   const picker = { sets: [], set(property, value) { this.sets.push([property, value]); } };
   const openTime = '09:00 AM';

   ConsoleDateFactory.applyScheduleTimePickerBounds(picker, { openTime });

   assert.deepEqual(picker.sets, [
      ['minTime', null],
      ['maxTime', null],
   ]);
});


test('Test_ApplyScheduleTimePickerBounds_TestBounds_ExpectSet', () => {
   const picker = { sets: [], set(property, value) { this.sets.push([property, value]); } };
   const openTime = '09:00 AM';
   const closeTime = '05:00 PM';

   ConsoleDateFactory.applyScheduleTimePickerBounds(picker, {
      openTime,
      closeTime,
   });

   assert.deepEqual(picker.sets, [
      ['minTime', openTime],
      ['maxTime', closeTime],
   ]);
});


test('Test_InitAttractionHoursSchedulePickers_TestSixInputs_ExpectInitialized', () => {
   const startDateEl = createDomNode('input');
   const endDateEl = createDomNode('input');
   const weekdayStartTimeEl = createDomNode('input');
   const weekdayEndTimeEl = createDomNode('input');
   const weekendHolidayStartTimeEl = createDomNode('input');
   const weekendHolidayEndTimeEl = createDomNode('input');
   const { calls, initFlatpickrFn } = _createFlatpickrSpy();

   const pickers = ConsoleDateFactory.initAttractionHoursSchedulePickers({
      startDateEl,
      endDateEl,
      weekdayStartTimeEl,
      weekdayEndTimeEl,
      weekendHolidayStartTimeEl,
      weekendHolidayEndTimeEl,
   }, { initFlatpickrFn });

   assert.equal(calls.length, 6);
   assert.equal(calls.at(Position.FIRST).inputEl, startDateEl);
   assert.equal(calls.at(Position.SECOND).inputEl, endDateEl);
   assert.equal(calls.at(Position.THIRD).inputEl, weekdayStartTimeEl);
   assert.equal(calls.at(Position.FOURTH).inputEl, weekdayEndTimeEl);
   assert.ok(pickers.startPicker);
   assert.ok(pickers.endPicker);
   assert.ok(pickers.weekdayStartTimePicker);
   assert.ok(pickers.weekendHolidayEndTimePicker);
});
