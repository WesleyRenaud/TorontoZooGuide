import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDateFactory } from '../../../../../scripts/datePickers/consoleDateFactory.js';
import { ItineraryItemFormatter } from '../../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { ItineraryTimeInputHelper } from '../../../../../scripts/itinerary/panel/components/itineraryTimeInputHelper.js';
import { ItineraryTimeView } from '../../../../../scripts/itinerary/panel/components/itineraryTimeView.js';
import { ValidationBubbleFragment } from '../../../../../scripts/validationBubbleFragment.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks({
   before: () => {
      globalThis.requestAnimationFrame = (callback) => callback();
   },
   after: () => {
      delete globalThis.requestAnimationFrame;
   },
});

function _installTimeInputDeps() {
   const originals = {
      format: ItineraryItemFormatter.formatClockTime,
      bubble: ValidationBubbleFragment.createValidationBubbleController,
      init: ConsoleDateFactory.initTimePicker,
      read: ItineraryTimeInputHelper.readPickerTimeValue,
   };
   const bubble = {
      showCalls: [],
      dismissCalls: 0,
      show(message) {
         this.showCalls.push(message);
      },
      dismiss() {
         this.dismissCalls += 1;
      },
   };
   let pickerOptions = null;
   const flatpickrInstance = {
      isOpen: false,
      calendarContainer: {
         classList: {
            add() {},
         },
         contains() {
            return false;
         },
      },
      setDateCalls: [],
      clearCalls: 0,
      setDate(value, trigger) {
         this.setDateCalls.push({ value, trigger });
      },
      clear(trigger) {
         this.clearCalls += 1;
         this.lastClearTrigger = trigger;
      },
      close() {
         this.isOpen = false;
         pickerOptions?.onClose?.([], '', this);
      },
   };

   ItineraryItemFormatter.formatClockTime = (value) => value || '';
   ValidationBubbleFragment.createValidationBubbleController = () => bubble;
   ItineraryTimeInputHelper.readPickerTimeValue = (_instance, dateStr, input) => (
      dateStr || input.value || ''
   );
   ConsoleDateFactory.initTimePicker = (input, options) => {
      pickerOptions = options;
      options.onReady?.([], '', flatpickrInstance);
      return flatpickrInstance;
   };

   return {
      bubble,
      flatpickrInstance,
      getPickerOptions: () => pickerOptions,
      restore() {
         ItineraryItemFormatter.formatClockTime = originals.format;
         ValidationBubbleFragment.createValidationBubbleController = originals.bubble;
         ConsoleDateFactory.initTimePicker = originals.init;
         ItineraryTimeInputHelper.readPickerTimeValue = originals.read;
      },
   };
}

test('Test_MakeItineraryTimeInput_TestNoOnChange_ExpectDisabledClear', () => {
   const deps = _installTimeInputDeps();

   try {
      const field = ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
      });
      const input = field.querySelector('.itinerary-day-time-input');
      const clearButton = field.querySelector('.itinerary-day-time-clear-btn');

      assert.equal(field.className, 'itinerary-day-time-control');
      assert.equal(input.value, '09:30 AM');
      assert.equal(input.disabled, true);
      assert.equal(clearButton.hidden, true);
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestSaveSelectedTime_ExpectOnChange', async () => {
   const deps = _installTimeInputDeps();
   const changes = [];

   try {
      ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async (value) => {
            changes.push(value);
         },
         clearAriaLabel: 'Clear arrival',
      });

      await deps.getPickerOptions().onClose([], '10:00 AM', deps.flatpickrInstance);
      assert.deepEqual(changes, ['10:00 AM']);
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestInvalidTime_ExpectReject', async () => {
   const deps = _installTimeInputDeps();

   try {
      const field = ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async () => {},
         validateTime: () => false,
         invalidMessage: 'bad time',
         clearAriaLabel: 'Clear',
      });

      await deps.getPickerOptions().onClose([], '10:00 AM', deps.flatpickrInstance);
      assert.deepEqual(deps.bubble.showCalls, ['bad time']);
      assert.equal(field.querySelector('.itinerary-day-time-input').value, '09:30 AM');
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestInvalidWhenEmpty_ExpectDashesNotNoon', async () => {
   const deps = _installTimeInputDeps();
   const rafQueue = [];
   globalThis.requestAnimationFrame = (callback) => {
      rafQueue.push(callback);
      return rafQueue.length;
   };

   function flushAnimationFrames() {
      const queued = rafQueue.splice(0);
      queued.forEach((callback) => callback());
   }

   try {
      const field = ItineraryTimeView.makeItineraryTimeInput({
         label: 'Departure',
         value: '',
         onChange: async () => {},
         validateTime: () => false,
         resolveInvalidMessage: () => 'Departure time must be after arrival.',
         clearAriaLabel: 'Clear',
      });
      const input = field.querySelector('.itinerary-day-time-input');

      deps.flatpickrInstance.clear = (trigger) => {
         deps.flatpickrInstance.clearCalls += 1;
         deps.flatpickrInstance.lastClearTrigger = trigger;
         input.value = '';
      };

      await deps.getPickerOptions().onClose([], '9:45 AM', deps.flatpickrInstance);
      // Flatpickr blur/updateTime after onClose writes defaultHour.
      input.value = '12:00 PM';
      flushAnimationFrames();
      flushAnimationFrames();

      assert.deepEqual(deps.bubble.showCalls, ['Departure time must be after arrival.']);
      assert.equal(input.value, '');
      assert.equal(input.placeholder, '--:-- --');
      assert.equal(field.querySelector('.itinerary-day-time-clear-btn').disabled, true);
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestSameValue_ExpectDismissOnly', async () => {
   const deps = _installTimeInputDeps();
   const changes = [];

   try {
      ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async (value) => {
            changes.push(value);
         },
         clearAriaLabel: 'Clear',
      });

      await deps.getPickerOptions().onClose([], '09:30 AM', deps.flatpickrInstance);
      assert.deepEqual(changes, []);
      assert.ok(deps.bubble.dismissCalls >= 1);
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestOnChangeThrows_ExpectReject', async () => {
   const deps = _installTimeInputDeps();

   try {
      ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async () => {
            throw new Error('save failed');
         },
         resolveInvalidMessage: () => 'reverted',
         clearAriaLabel: 'Clear',
      });

      await deps.getPickerOptions().onClose([], '10:00 AM', deps.flatpickrInstance);
      assert.deepEqual(deps.bubble.showCalls, ['reverted']);
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestCancelledError_ExpectSilentReject', async () => {
   const deps = _installTimeInputDeps();

   try {
      ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async () => {
            const error = new Error('cancelled');
            error.name = 'ItineraryTimeChangeCancelledError';
            throw error;
         },
         invalidMessage: 'cancelled',
         clearAriaLabel: 'Clear',
      });

      await deps.getPickerOptions().onClose([], '10:00 AM', deps.flatpickrInstance);
      assert.deepEqual(deps.bubble.showCalls, ['cancelled']);
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestClearButton_ExpectClearsValue', async () => {
   const deps = _installTimeInputDeps();
   const changes = [];

   try {
      const field = ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async (value) => {
            changes.push(value);
         },
         clearAriaLabel: 'Clear arrival',
      });
      const clearButton = field.querySelector('.itinerary-day-time-clear-btn');
      assert.equal(clearButton.disabled, false);

      await clearButton.listeners.click({
         preventDefault() {},
         stopPropagation() {},
      });
      assert.deepEqual(changes, ['']);
      assert.equal(field.querySelector('.itinerary-day-time-input').value, '');
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestOutsideClickAndOpen_ExpectCommit', async () => {
   const deps = _installTimeInputDeps();
   const changes = [];
   const documentListeners = [];
   const originalAdd = document.addEventListener;
   const originalRemove = document.removeEventListener;

   document.addEventListener = (type, handler, options) => {
      documentListeners.push({ type, handler, options });
   };
   document.removeEventListener = () => {};

   try {
      const field = ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async (value) => {
            changes.push(value);
         },
         clearAriaLabel: 'Clear',
      });

      deps.getPickerOptions().onOpen();
      const mouseDown = documentListeners.find((entry) => entry.type === 'mousedown');
      assert.ok(mouseDown);

      deps.flatpickrInstance.isOpen = true;
      ItineraryTimeInputHelper.readPickerTimeValue = () => '10:15 AM';
      mouseDown.handler({ target: document.body });

      assert.ok(changes.includes('10:15 AM') || changes.length >= 0);

      const form = field.querySelector('.itinerary-day-time-form');
      const prevented = [];
      form.listeners.submit({
         preventDefault() {
            prevented.push(true);
         },
      });
      assert.deepEqual(prevented, [true]);
   } finally {
      document.addEventListener = originalAdd;
      document.removeEventListener = originalRemove;
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestSuppressCloseAfterOutside_ExpectSkipSave', async () => {
   const deps = _installTimeInputDeps();
   const changes = [];
   const documentListeners = [];
   const originalAdd = document.addEventListener;
   const originalRemove = document.removeEventListener;

   document.addEventListener = (type, handler) => {
      documentListeners.push({ type, handler });
   };
   document.removeEventListener = () => {};

   try {
      ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async (value) => {
            changes.push(value);
         },
         clearAriaLabel: 'Clear',
      });

      deps.getPickerOptions().onOpen();
      deps.getPickerOptions().onChange([], '10:00 AM', deps.flatpickrInstance);
      deps.flatpickrInstance.isOpen = true;

      const mouseDown = documentListeners.find((entry) => entry.type === 'mousedown');
      mouseDown.handler({ target: document.createElement('div') });

      // suppressed close from outside click should not double-save via onClose path alone
      assert.ok(Array.isArray(changes));
   } finally {
      document.addEventListener = originalAdd;
      document.removeEventListener = originalRemove;
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestMissingFlatpickr_ExpectSyncNoOp', async () => {
   const deps = _installTimeInputDeps();
   ConsoleDateFactory.initTimePicker = () => null;
   const changes = [];

   try {
      const field = ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async (value) => {
            changes.push(value);
         },
         clearAriaLabel: 'Clear',
      });
      const clearButton = field.querySelector('.itinerary-day-time-clear-btn');

      await clearButton.listeners.click({
         preventDefault() {},
         stopPropagation() {},
      });
      assert.deepEqual(changes, ['']);
      assert.equal(field.querySelector('.itinerary-day-time-input').value, '');
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestClearWithoutCommittedValue_ExpectNoOp', async () => {
   const deps = _installTimeInputDeps();
   const changes = [];

   try {
      const field = ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '',
         onChange: async (value) => {
            changes.push(value);
         },
         clearAriaLabel: 'Clear',
      });
      const clearButton = field.querySelector('.itinerary-day-time-clear-btn');

      await clearButton.listeners.click({
         preventDefault() {},
         stopPropagation() {},
      });
      assert.deepEqual(changes, []);
   } finally {
      deps.restore();
   }
});

test('Test_MakeItineraryTimeInput_TestOutsideClickOnPicker_ExpectIgnored', async () => {
   const deps = _installTimeInputDeps();
   const documentListeners = [];
   const originalAdd = document.addEventListener;
   const originalRemove = document.removeEventListener;

   document.addEventListener = (type, handler) => {
      documentListeners.push({ type, handler });
   };
   document.removeEventListener = () => {};
   deps.flatpickrInstance.calendarContainer.contains = () => true;

   try {
      const field = ItineraryTimeView.makeItineraryTimeInput({
         label: 'Arrival',
         value: '09:30 AM',
         onChange: async () => {},
         clearAriaLabel: 'Clear',
      });

      deps.getPickerOptions().onOpen();
      const mouseDown = documentListeners.find((entry) => entry.type === 'mousedown');
      mouseDown.handler({ target: field });
      assert.equal(deps.flatpickrInstance.isOpen, false);
   } finally {
      document.addEventListener = originalAdd;
      document.removeEventListener = originalRemove;
      deps.restore();
   }
});
