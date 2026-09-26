import assert from 'node:assert/strict';
import { test } from 'node:test';

import { MultiTimeController } from '../../../scripts/datePickers/multiTimeController.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';


function _createMockPickerInstance(inputEl, overrides = {}) {
   return {
      close() {},
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
      setDate() {
         inputEl.value = '';
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
         return _createMockPickerInstance(inputEl);
      },
   };
}


function _dispatchKeydown(inputEl, key) {
   inputEl.listeners.keydown?.({
      key,
      preventDefault() {},
      stopImmediatePropagation() {},
   });
}


test('Test_InitMultiTimePicker_TestMissingInput_ExpectNull', () => {
   const inputEl = null;

   const picker = MultiTimeController.initMultiTimePicker(inputEl, {});

   assert.equal(picker, null);
});


test('Test_InitMultiTimePicker_TestMissingOptions_ExpectNull', () => {
   const inputEl = null;

   const picker = MultiTimeController.initMultiTimePicker(inputEl);

   assert.equal(picker, null);
});


test('Test_InitMultiTimePicker_TestPickerCloses_ExpectCommit', async () => {
   const inputEl = createDomNode('input');
   const committedTimes = [];
   const time = '1:00 PM';
   const { calls, initFlatpickrFn } = _createFlatpickrSpy();
   MultiTimeController.initMultiTimePicker(inputEl, {
      onCommitTime: (nextTime) => {
         committedTimes.push(nextTime);
      },
   }, initFlatpickrFn);
   inputEl.value = time;

   calls.at(Position.FIRST).options.onClose([], time, {
      setDate() {},
   });
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.deepEqual(committedTimes, [time]);
   assert.equal(inputEl.value, '');
});


test('Test_InitMultiTimePicker_TestChangeEvents_ExpectNoCommit', () => {
   const inputEl = createDomNode('input');
   const { calls, initFlatpickrFn } = _createFlatpickrSpy();

   MultiTimeController.initMultiTimePicker(inputEl, {}, initFlatpickrFn);

   assert.equal(calls.at(Position.FIRST).options.onChange, undefined);
});


test('Test_InitMultiTimePicker_TestBlurWhileOpen_ExpectNoCommit', async () => {
   const inputEl = createDomNode('input');
   const committedTimes = [];
   const time = '12:00 PM';

   MultiTimeController.initMultiTimePicker(inputEl, {
      onCommitTime: (nextTime) => {
         committedTimes.push(nextTime);
      },
   }, (_element, options) => {
      const instance = _createMockPickerInstance(inputEl, {
         isOpen: true,
      });
      options.onReady?.([], '', instance);
      return instance;
   });
   inputEl.value = time;
   inputEl.listeners.blur?.();
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.deepEqual(committedTimes, []);
});


test('Test_InitMultiTimePicker_TestEnterTyped_ExpectCommit', () => {
   const inputEl = createDomNode('input');
   const committedTimes = [];
   const time = '2:30 PM';

   MultiTimeController.initMultiTimePicker(inputEl, {
      onCommitTime: (nextTime) => {
         committedTimes.push(nextTime);
      },
   }, _createFlatpickrSpy().initFlatpickrFn);
   inputEl.value = time;
   _dispatchKeydown(inputEl, 'Enter');

   assert.deepEqual(committedTimes, [time]);
   assert.equal(inputEl.value, '');
});


test('Test_InitMultiTimePicker_TestEnterEmpty_ExpectCommitDefault', () => {
   const inputEl = createDomNode('input');
   const committedTimes = [];
   let instance;

   MultiTimeController.initMultiTimePicker(inputEl, {
      onCommitTime: (time) => {
         committedTimes.push(time);
      },
   }, (_element, options) => {
      instance = _createMockPickerInstance(inputEl, {
         close() {
            this.isOpen = false;
         },
      });
      options.onReady?.([], '', instance);
      return instance;
   });
   _dispatchKeydown(inputEl, 'Enter');

   assert.deepEqual(
      committedTimes,
      [`${instance.hourElement.value}:${instance.minuteElement.value} ${instance.amPM.textContent}`]
   );
   assert.equal(inputEl.value, '');
});


test('Test_InitMultiTimePicker_TestBackspaceEmpty_ExpectRemoveLast', () => {
   const inputEl = createDomNode('input');
   let removed = false;

   MultiTimeController.initMultiTimePicker(inputEl, {
      onRemoveLastTime: () => {
         removed = true;
         return true;
      },
   }, _createFlatpickrSpy().initFlatpickrFn);
   _dispatchKeydown(inputEl, 'Backspace');

   assert.equal(removed, true);
});


test('Test_InitMultiTimePicker_TestBackspaceWithText_ExpectNoRemove', () => {
   const inputEl = createDomNode('input');
   let removed = false;

   MultiTimeController.initMultiTimePicker(inputEl, {
      onRemoveLastTime: () => {
         removed = true;
         return true;
      },
   }, _createFlatpickrSpy().initFlatpickrFn);
   inputEl.value = '2';
   _dispatchKeydown(inputEl, 'Backspace');

   assert.equal(removed, false);
});
