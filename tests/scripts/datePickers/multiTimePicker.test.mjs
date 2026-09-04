import assert from 'node:assert/strict';
import { test } from 'node:test';

import { MultiTimePicker } from '../../../scripts/datePickers/multiTimePicker.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';

function createMockPickerInstance(inputEl, overrides = {}) {
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

function createFlatpickrSpy() {
   const calls = [];

   return {
      calls,
      initFlatpickrFn: (inputEl, options) => {
         calls.push({ inputEl, options });
         return createMockPickerInstance(inputEl);
      },
   };
}

function dispatchKeydown(inputEl, key) {
   inputEl.listeners.keydown?.({
      key,
      preventDefault() {},
      stopImmediatePropagation() {},
   });
}

test('Test_InitMultiTimePicker_TestPickerCloses_ExpectCommit', async () => {
   const inputEl = createDomNode('input');
   const committedTimes = [];
   const { calls, initFlatpickrFn } = createFlatpickrSpy();

   MultiTimePicker.initMultiTimePicker(inputEl, {
      onCommitTime: (time) => {
         committedTimes.push(time);
      },
   }, initFlatpickrFn);

   inputEl.value = '1:00 PM';
   calls[0].options.onClose([], '1:00 PM', {
      setDate() {},
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.deepEqual(committedTimes, [ '1:00 PM' ]);
   assert.equal(inputEl.value, '');
});

test('Test_InitMultiTimePicker_TestChangeEvents_ExpectNoCommit', () => {
   const inputEl = createDomNode('input');
   const { calls, initFlatpickrFn } = createFlatpickrSpy();

   MultiTimePicker.initMultiTimePicker(inputEl, {}, initFlatpickrFn);

   assert.equal(calls[0].options.onChange, undefined);
});

test('Test_InitMultiTimePicker_TestBlurWhileOpen_ExpectNoCommit', async () => {
   const inputEl = createDomNode('input');
   const committedTimes = [];

   MultiTimePicker.initMultiTimePicker(inputEl, {
      onCommitTime: (time) => {
         committedTimes.push(time);
      },
   }, (_element, options) => {
      const instance = createMockPickerInstance(inputEl, {
         isOpen: true,
      });

      options.onReady?.([], '', instance);
      return instance;
   });

   inputEl.value = '12:00 PM';
   inputEl.listeners.blur?.();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.deepEqual(committedTimes, []);
});

test('Test_InitMultiTimePicker_TestEnterTyped_ExpectCommit', () => {
   const inputEl = createDomNode('input');
   const committedTimes = [];

   MultiTimePicker.initMultiTimePicker(inputEl, {
      onCommitTime: (time) => {
         committedTimes.push(time);
      },
   }, createFlatpickrSpy().initFlatpickrFn);

   inputEl.value = '2:30 PM';
   dispatchKeydown(inputEl, 'Enter');

   assert.deepEqual(committedTimes, [ '2:30 PM' ]);
   assert.equal(inputEl.value, '');
});

test('Test_InitMultiTimePicker_TestEnterEmpty_ExpectCommitDefault', () => {
   const inputEl = createDomNode('input');
   const committedTimes = [];

   MultiTimePicker.initMultiTimePicker(inputEl, {
      onCommitTime: (time) => {
         committedTimes.push(time);
      },
   }, (_element, options) => {
      const instance = createMockPickerInstance(inputEl, {
         close() {
            this.isOpen = false;
         },
      });

      options.onReady?.([], '', instance);
      return instance;
   });

   dispatchKeydown(inputEl, 'Enter');

   assert.deepEqual(committedTimes, [ '12:00 PM' ]);
   assert.equal(inputEl.value, '');
});

test('Test_InitMultiTimePicker_TestBackspaceEmpty_ExpectRemoveLast', () => {
   const inputEl = createDomNode('input');
   let removed = false;

   MultiTimePicker.initMultiTimePicker(inputEl, {
      onRemoveLastTime: () => {
         removed = true;
         return true;
      },
   }, createFlatpickrSpy().initFlatpickrFn);

   dispatchKeydown(inputEl, 'Backspace');

   assert.equal(removed, true);
});

test('Test_InitMultiTimePicker_TestBackspaceWithText_ExpectNoRemove', () => {
   const inputEl = createDomNode('input');
   let removed = false;

   MultiTimePicker.initMultiTimePicker(inputEl, {
      onRemoveLastTime: () => {
         removed = true;
         return true;
      },
   }, createFlatpickrSpy().initFlatpickrFn);

   inputEl.value = '2';
   dispatchKeydown(inputEl, 'Backspace');

   assert.equal(removed, false);
});
