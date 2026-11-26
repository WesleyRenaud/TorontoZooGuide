import assert from 'node:assert/strict';
import test from 'node:test';

import { FlatpickrActivationBinder } from '../../../scripts/datePickers/flatpickrActivationBinder.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


function _createKeyEvent(key, extras = {}) {
   const prevented = [];
   return {
      key,
      altKey: false,
      ctrlKey: false,
      metaKey: false,
      preventDefault() {
         prevented.push('default');
      },
      stopPropagation() {
         prevented.push('stop');
      },
      prevented,
      ...extras,
   };
}


function _createPickerInstance(overrides = {}) {
   const selectedDateElem = document.createElement('span');
   const focusCalls = [];
   selectedDateElem.focus = () => {
      focusCalls.push('day');
   };

   const calendar = document.createElement('div');
   calendar.appendChild(selectedDateElem);
   const instance = {
      isOpen: false,
      openCalls: 0,
      calendarContainer: calendar,
      selectedDateElem,
      todayDateElem: null,
      hourElement: null,
      focusCalls,
      config: {
         onOpen: [],
         onClose: [],
      },
      open() {
         this.isOpen = true;
         this.openCalls += 1;
         this.config.onOpen.forEach((hook) => hook());
      },
      close() {
         this.isOpen = false;
         this.config.onClose.forEach((hook) => hook());
      },
      ...overrides,
   };

   return instance;
}


function _createBoundInput(instanceOverrides = {}) {
   const inputEl = document.createElement('input');
   inputEl.focusCalls = 0;
   inputEl.focus = () => {
      inputEl.focusCalls += 1;
   };
   const instance = _createPickerInstance(instanceOverrides);
   FlatpickrActivationBinder.install(inputEl, () => instance);
   return { inputEl, instance };
}


test('Test_Install_TestMissingArgs_ExpectNoop', () => {
   const inputEl = document.createElement('input');

   assert.doesNotThrow(() => FlatpickrActivationBinder.install(null, () => ({})));
   assert.doesNotThrow(() => FlatpickrActivationBinder.install(inputEl, null));
   assert.doesNotThrow(() => FlatpickrActivationBinder.install(inputEl, 'not-a-function'));
   assert.equal(inputEl.getAttribute('aria-haspopup'), null);
});


test('Test_Install_TestDecoratesInput_ExpectDialogPopup', () => {
   const { inputEl, instance } = _createBoundInput();

   assert.equal(
      inputEl.getAttribute('aria-haspopup'),
      FlatpickrActivationBinder.HAS_POPUP_VALUE
   );
   assert.equal(
      inputEl.getAttribute('aria-expanded'),
      FlatpickrActivationBinder.EXPANDED_FALSE
   );
   assert.equal(
      inputEl.getAttribute('aria-controls'),
      instance.calendarContainer.id
   );
   assert.match(
      instance.calendarContainer.id,
      new RegExp(`^${FlatpickrActivationBinder.CALENDAR_ID_PREFIX}\\d+$`)
   );
});


test('Test_Install_TestExistingCalendarId_ExpectReused', () => {
   const calendar = document.createElement('div');
   calendar.id = 'existing-picker-id';
   const { inputEl } = _createBoundInput({ calendarContainer: calendar });

   assert.equal(inputEl.getAttribute('aria-controls'), 'existing-picker-id');
   assert.equal(calendar.id, 'existing-picker-id');
});


test('Test_Install_TestSecondCall_ExpectIdempotent', () => {
   const { inputEl, instance } = _createBoundInput();
   let added = 0;
   const originalAdd = inputEl.addEventListener.bind(inputEl);
   inputEl.addEventListener = (...args) => {
      added += 1;
      originalAdd(...args);
   };

   FlatpickrActivationBinder.install(inputEl, () => instance);

   assert.equal(added, 0);
});


test('Test_Install_TestFocus_ExpectPickerStaysClosed', () => {
   const { inputEl, instance } = _createBoundInput();

   inputEl.listeners.focus?.({ type: 'focus' });

   assert.equal(instance.isOpen, false);
   assert.equal(instance.openCalls, 0);
   assert.equal(
      inputEl.getAttribute('aria-expanded'),
      FlatpickrActivationBinder.EXPANDED_FALSE
   );
});


test('Test_HandlePointerActivation_TestMouseDown_ExpectOpensWithoutMovingFocus', () => {
   const { inputEl, instance } = _createBoundInput();

   inputEl.listeners.mousedown({ button: 0 });

   assert.equal(instance.isOpen, true);
   assert.equal(instance.openCalls, 1);
   assert.equal(FlatpickrActivationBinder.wasOpenedByPointer(inputEl), true);
   assert.equal(
      inputEl.getAttribute('aria-expanded'),
      FlatpickrActivationBinder.EXPANDED_TRUE
   );
   assert.deepEqual(instance.focusCalls, []);
});


test('Test_HandlePointerActivation_TestRightClick_ExpectStaysClosed', () => {
   const { inputEl, instance } = _createBoundInput();

   inputEl.listeners.mousedown({ button: 2 });

   assert.equal(instance.isOpen, false);
   assert.equal(instance.openCalls, 0);
});


test('Test_HandlePointerActivation_TestAlreadyOpen_ExpectNoSecondOpen', () => {
   const { inputEl, instance } = _createBoundInput();
   instance.open();
   const openCallsAfterFirst = instance.openCalls;

   inputEl.listeners.mousedown({ button: 0 });

   assert.equal(instance.openCalls, openCallsAfterFirst);
});


test('Test_HandlePointerActivation_TestDisabledInput_ExpectStaysClosed', () => {
   const { inputEl, instance } = _createBoundInput();
   inputEl.disabled = true;

   inputEl.listeners.mousedown({ button: 0 });

   assert.equal(instance.isOpen, false);
});


test('Test_HandleKeyboardActivation_TestEnter_ExpectOpensAndFocusesPicker', () => {
   const { inputEl, instance } = _createBoundInput();
   const event = _createKeyEvent(FlatpickrActivationBinder.ENTER_KEY);

   inputEl.listeners.keydown(event);

   assert.equal(instance.isOpen, true);
   assert.equal(FlatpickrActivationBinder.wasOpenedByPointer(inputEl), false);
   assert.deepEqual(event.prevented, ['default', 'stop']);
   assert.deepEqual(instance.focusCalls, ['day']);
   assert.equal(
      inputEl.getAttribute('aria-expanded'),
      FlatpickrActivationBinder.EXPANDED_TRUE
   );
});


test('Test_HandleKeyboardActivation_TestSpaceAndArrowDown_ExpectOpen', () => {
   const spaceBinding = _createBoundInput();
   const arrowBinding = _createBoundInput();

   spaceBinding.inputEl.listeners.keydown(
      _createKeyEvent(FlatpickrActivationBinder.SPACE_KEY)
   );
   arrowBinding.inputEl.listeners.keydown(
      _createKeyEvent(FlatpickrActivationBinder.ARROW_DOWN_KEY)
   );

   assert.equal(spaceBinding.instance.isOpen, true);
   assert.equal(arrowBinding.instance.isOpen, true);
});


test('Test_HandleKeyboardActivation_TestTab_ExpectStaysClosed', () => {
   const { inputEl, instance } = _createBoundInput();
   const event = _createKeyEvent('Tab');

   inputEl.listeners.keydown(event);

   assert.equal(instance.isOpen, false);
   assert.deepEqual(event.prevented, []);
});


test('Test_HandleKeyboardActivation_TestModifierEnter_ExpectStaysClosed', () => {
   const { inputEl, instance } = _createBoundInput();

   inputEl.listeners.keydown(
      _createKeyEvent(FlatpickrActivationBinder.ENTER_KEY, { ctrlKey: true })
   );
   inputEl.listeners.keydown(
      _createKeyEvent(FlatpickrActivationBinder.ENTER_KEY, { altKey: true })
   );
   inputEl.listeners.keydown(
      _createKeyEvent(FlatpickrActivationBinder.ENTER_KEY, { metaKey: true })
   );

   assert.equal(instance.isOpen, false);
});


test('Test_HandleKeyboardActivation_TestAlreadyOpen_ExpectLeavesPicker', () => {
   const { inputEl, instance } = _createBoundInput();
   instance.open();
   const event = _createKeyEvent(FlatpickrActivationBinder.ENTER_KEY);

   inputEl.listeners.keydown(event);

   assert.equal(instance.openCalls, 1);
   assert.deepEqual(event.prevented, []);
   assert.deepEqual(instance.focusCalls, []);
});


test('Test_HandleKeyboardActivation_TestDisabledInput_ExpectStaysClosed', () => {
   const { inputEl, instance } = _createBoundInput();
   inputEl.disabled = true;

   inputEl.listeners.keydown(_createKeyEvent(FlatpickrActivationBinder.ENTER_KEY));

   assert.equal(instance.isOpen, false);
});


test('Test_OnClose_TestKeyboardOpen_ExpectFocusReturnsToField', () => {
   const { inputEl, instance } = _createBoundInput();
   inputEl.listeners.keydown(_createKeyEvent(FlatpickrActivationBinder.ENTER_KEY));
   document.activeElement = instance.selectedDateElem;

   instance.close();

   assert.equal(inputEl.focusCalls, 1);
   assert.equal(
      inputEl.getAttribute('aria-expanded'),
      FlatpickrActivationBinder.EXPANDED_FALSE
   );
});


test('Test_OnClose_TestPointerOpen_ExpectDoesNotStealFocus', () => {
   const { inputEl, instance } = _createBoundInput();
   inputEl.listeners.mousedown({ button: 0 });

   instance.close();

   assert.equal(inputEl.focusCalls, 0);
   assert.equal(FlatpickrActivationBinder.wasOpenedByPointer(inputEl), true);
});


test('Test_OnClose_TestFocusMovedElsewhere_ExpectLeavesNewFocus', () => {
   const { inputEl, instance } = _createBoundInput();
   const otherControl = document.createElement('button');
   inputEl.listeners.keydown(_createKeyEvent(FlatpickrActivationBinder.ENTER_KEY));
   document.activeElement = otherControl;

   instance.close();

   assert.equal(inputEl.focusCalls, 0);
});


test('Test_WasOpenedByPointer_TestMissingInput_ExpectFalse', () => {
   assert.equal(FlatpickrActivationBinder.wasOpenedByPointer(null), false);
   assert.equal(FlatpickrActivationBinder.wasOpenedByPointer({}), false);
});


test('Test_AppendHook_TestExistingShapes_ExpectPreserved', () => {
   const calls = [];
   const arrayInstance = { config: { onOpen: [() => { calls.push('array'); }] } };
   const functionInstance = { config: { onOpen: () => { calls.push('function'); } } };
   const emptyInstance = { config: {} };

   FlatpickrActivationBinder.appendHook(arrayInstance, 'onOpen', () => {
      calls.push('added-array');
   });
   FlatpickrActivationBinder.appendHook(functionInstance, 'onOpen', () => {
      calls.push('added-function');
   });
   FlatpickrActivationBinder.appendHook(emptyInstance, 'onOpen', () => {
      calls.push('added-empty');
   });
   FlatpickrActivationBinder.appendHook(emptyInstance, 'onClose', null);

   arrayInstance.config.onOpen.forEach((hook) => hook());
   functionInstance.config.onOpen.forEach((hook) => hook());
   emptyInstance.config.onOpen.forEach((hook) => hook());

   assert.deepEqual(calls, [
      'array',
      'added-array',
      'function',
      'added-function',
      'added-empty',
   ]);
   assert.equal(emptyInstance.config.onClose, undefined);
});


test('Test_HookInstanceLifecycle_TestMissingConfig_ExpectNoop', () => {
   assert.doesNotThrow(() => {
      FlatpickrActivationBinder.hookInstanceLifecycle(null, {
         onOpen() {},
         onClose() {},
      });
      FlatpickrActivationBinder.hookInstanceLifecycle({}, {
         onOpen() {},
         onClose() {},
      });
   });
});


test('Test_DecorateInput_TestMissingInput_ExpectNoop', () => {
   assert.doesNotThrow(() => {
      FlatpickrActivationBinder.decorateInput(null, {});
      FlatpickrActivationBinder.syncExpanded(null, true);
      FlatpickrActivationBinder.ensureCalendarId(null);
   });
   assert.equal(FlatpickrActivationBinder.ensureCalendarId({}), null);
});


test('Test_GetInitialPickerFocus_TestFallbacks_ExpectPreferredTarget', () => {
   const selected = { id: 'selected' };
   const today = { id: 'today' };
   const hour = { id: 'hour' };
   const queriedSelected = { id: 'queried-selected' };
   const queriedToday = { id: 'queried-today' };
   const queriedHour = { id: 'queried-hour' };
   const queriedDay = { id: 'queried-day' };

   assert.equal(
      FlatpickrActivationBinder.getInitialPickerFocus({ selectedDateElem: selected }),
      selected
   );
   assert.equal(
      FlatpickrActivationBinder.getInitialPickerFocus({ todayDateElem: today }),
      today
   );
   assert.equal(
      FlatpickrActivationBinder.getInitialPickerFocus({
         calendarContainer: {
            querySelector(selector) {
               if (selector === FlatpickrActivationBinder.SELECTED_DAY_SELECTOR) {
                  return queriedSelected;
               }

               return null;
            },
         },
      }),
      queriedSelected
   );
   assert.equal(
      FlatpickrActivationBinder.getInitialPickerFocus({
         calendarContainer: {
            querySelector(selector) {
               if (selector === FlatpickrActivationBinder.TODAY_DAY_SELECTOR) {
                  return queriedToday;
               }

               return null;
            },
         },
      }),
      queriedToday
   );
   assert.equal(
      FlatpickrActivationBinder.getInitialPickerFocus({ hourElement: hour }),
      hour
   );
   assert.equal(
      FlatpickrActivationBinder.getInitialPickerFocus({
         hourElement: hour,
         calendarContainer: {
            querySelector() {
               return null;
            },
         },
      }),
      hour
   );
   assert.equal(
      FlatpickrActivationBinder.getInitialPickerFocus({
         calendarContainer: {
            querySelector(selector) {
               if (selector === FlatpickrActivationBinder.HOUR_SELECTOR) {
                  return queriedHour;
               }

               return null;
            },
         },
      }),
      queriedHour
   );
   assert.equal(
      FlatpickrActivationBinder.getInitialPickerFocus({
         calendarContainer: {
            querySelector(selector) {
               if (selector === FlatpickrActivationBinder.ENABLED_DAY_SELECTOR) {
                  return queriedDay;
               }

               return null;
            },
         },
      }),
      queriedDay
   );
   assert.equal(
      FlatpickrActivationBinder.getInitialPickerFocus({
         calendarContainer: {},
         hourElement: hour,
      }),
      hour
   );
   assert.equal(FlatpickrActivationBinder.getInitialPickerFocus(null), null);
   assert.equal(FlatpickrActivationBinder.getInitialPickerFocus({}), null);
});


test('Test_ShouldRestoreFocus_TestActiveElementCases_ExpectRestoreOnlyWhenLostOrInPicker', () => {
   const inputEl = document.createElement('input');
   const instance = {
      calendarContainer: {
         contains(node) {
            return node?.id === 'in-picker';
         },
      },
   };
   const inPicker = { id: 'in-picker' };
   const elsewhere = { id: 'elsewhere' };

   document.activeElement = null;
   assert.equal(
      FlatpickrActivationBinder.shouldRestoreFocus(inputEl, instance),
      true
   );

   document.activeElement = inputEl;
   assert.equal(
      FlatpickrActivationBinder.shouldRestoreFocus(inputEl, instance),
      false
   );

   document.activeElement = document.body;
   assert.equal(
      FlatpickrActivationBinder.shouldRestoreFocus(inputEl, instance),
      true
   );

   if (!document.documentElement) {
      document.documentElement = document.createElement('html');
   }

   document.activeElement = document.documentElement;
   assert.equal(
      FlatpickrActivationBinder.shouldRestoreFocus(inputEl, instance),
      true
   );

   document.activeElement = inPicker;
   assert.equal(
      FlatpickrActivationBinder.shouldRestoreFocus(inputEl, instance),
      true
   );

   document.activeElement = elsewhere;
   assert.equal(
      FlatpickrActivationBinder.shouldRestoreFocus(inputEl, instance),
      false
   );

   assert.equal(FlatpickrActivationBinder.shouldRestoreFocus(null, instance), false);
});


test('Test_IsFocusInsidePicker_TestMissingCalendar_ExpectFalse', () => {
   assert.equal(
      FlatpickrActivationBinder.isFocusInsidePicker(document.body, null),
      false
   );
   assert.equal(
      FlatpickrActivationBinder.isFocusInsidePicker(null, { calendarContainer: {} }),
      false
   );
});


test('Test_HandlePointerActivation_TestMissingInstance_ExpectNoop', () => {
   const inputEl = document.createElement('input');
   FlatpickrActivationBinder.install(inputEl, () => null);

   assert.doesNotThrow(() => {
      inputEl.listeners.mousedown({ button: 0 });
      inputEl.listeners.keydown(_createKeyEvent(FlatpickrActivationBinder.ENTER_KEY));
   });
});


test('Test_FocusInsidePicker_TestMissingTarget_ExpectNoop', () => {
   assert.doesNotThrow(() => {
      FlatpickrActivationBinder.focusInsidePicker(null);
      FlatpickrActivationBinder.restoreFocusToInput(null, null);
   });
});


test('Test_ShouldRestoreFocus_TestMissingDocument_ExpectFalse', () => {
   const originalDocument = globalThis.document;
   const inputEl = document.createElement('input');

   try {
      globalThis.document = undefined;
      assert.equal(
         FlatpickrActivationBinder.shouldRestoreFocus(inputEl, {}),
         false
      );
   } finally {
      globalThis.document = originalDocument;
   }
});


test('Test_DecorateInput_TestNoCalendar_ExpectPopupWithoutControls', () => {
   const inputEl = document.createElement('input');

   FlatpickrActivationBinder.decorateInput(inputEl, { isOpen: false });

   assert.equal(
      inputEl.getAttribute('aria-haspopup'),
      FlatpickrActivationBinder.HAS_POPUP_VALUE
   );
   assert.equal(
      inputEl.getAttribute('aria-expanded'),
      FlatpickrActivationBinder.EXPANDED_FALSE
   );
   assert.equal(inputEl.getAttribute('aria-controls'), null);
});
