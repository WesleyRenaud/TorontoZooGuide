import assert from 'node:assert/strict';
import test from 'node:test';

import { MapControlsBinder } from '../../../scripts/map/mapControlsBinder.js';
import { VisitDateAdapter } from '../../../scripts/visitDates/visitDateAdapter.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_BlurMapDateInput_TestInputAndActive_ExpectBlurCalls', () => {
   const blurs = [];
   const mapDateInput = { blur: () => blurs.push('input') };
   const originalActive = Object.getOwnPropertyDescriptor(document, 'activeElement');
   Object.defineProperty(document, 'activeElement', {
      configurable: true,
      get: () => ({ blur: () => blurs.push('active') }),
   });

   try {
      MapControlsBinder.blurMapDateInput(mapDateInput);
      MapControlsBinder.blurMapDateInput(null);

      assert.deepEqual(blurs, ['input', 'active', 'active']);
   } finally {
      if (originalActive) {
         Object.defineProperty(document, 'activeElement', originalActive);
      } else {
         delete document.activeElement;
      }
   }
});


test('Test_CloseMapDatePicker_TestFpAndInput_ExpectCloseAndBlur', () => {
   const closes = [];
   const blurs = [];
   const originalBlur = MapControlsBinder.blurMapDateInput;
   const input = 'input';
   MapControlsBinder.blurMapDateInput = (nextInput) => {
      blurs.push(nextInput);
   };

   try {
      MapControlsBinder.closeMapDatePicker({ close: () => closes.push(true) }, input);
      MapControlsBinder.closeMapDatePicker(null, input);

      assert.deepEqual(closes, [true]);
      assert.deepEqual(blurs, [input, input]);
   } finally {
      MapControlsBinder.blurMapDateInput = originalBlur;
   }
});


test('Test_IsSpecificDayPreset_TestSpecificDay_ExpectTrue', () => {
   const isSpecific = MapControlsBinder.isSpecificDayPreset({ value: 'specific-day' });

   assert.equal(isSpecific, true);
});


test('Test_IsSpecificDayPreset_TestToday_ExpectFalse', () => {
   const isSpecific = MapControlsBinder.isSpecificDayPreset({ value: 'today' });

   assert.equal(isSpecific, false);
});


test('Test_IsSpecificDayPreset_TestNull_ExpectFalse', () => {
   const isSpecific = MapControlsBinder.isSpecificDayPreset(null);

   assert.equal(isSpecific, false);
});


test('Test_GetCurrentDateStr_TestInput_ExpectValue', () => {
   const iso = '2026-06-15';

   const dateStr = MapControlsBinder.getCurrentDateStr({ value: iso }, null);

   assert.equal(dateStr, iso);
});


test('Test_GetCurrentDateStr_TestPickerInput_ExpectValue', () => {
   const iso = '2026-06-16';

   const dateStr = MapControlsBinder.getCurrentDateStr({ value: '' }, { input: { value: iso } });

   assert.equal(dateStr, iso);
});


test('Test_GetCurrentDateStr_TestMissing_ExpectEmpty', () => {
   const dateStr = MapControlsBinder.getCurrentDateStr(null, null);

   assert.equal(dateStr, '');
});


test('Test_SyncDateInputVisibility_TestSpecificDay_ExpectInline', () => {
   const mapDateInput = { style: { display: '' } };

   MapControlsBinder.syncDateInputVisibility({ value: 'specific-day' }, mapDateInput);

   assert.equal(mapDateInput.style.display, 'inline-block');
});


test('Test_SyncDateInputVisibility_TestToday_ExpectNone', () => {
   const mapDateInput = { style: { display: '' } };

   MapControlsBinder.syncDateInputVisibility({ value: 'today' }, mapDateInput);

   assert.equal(mapDateInput.style.display, 'none');
});


test('Test_UpdateMapForCurrentControls_TestEmptyPreset_ExpectNoUpdate', () => {
   const updates = [];

   MapControlsBinder.updateMapForCurrentControls({
      mapPreset: { value: '' },
      mapDateInput: { value: '2026-06-15' },
      onUpdate: (...args) => updates.push(args),
   });

   assert.deepEqual(updates, []);
});


test('Test_UpdateMapForCurrentControls_TestSpecificDayEmpty_ExpectNoUpdate', () => {
   const updates = [];

   MapControlsBinder.updateMapForCurrentControls({
      mapPreset: { value: 'specific-day' },
      mapDateInput: { value: '' },
      fp: { input: { value: '' } },
      onUpdate: (...args) => updates.push(args),
   });

   assert.deepEqual(updates, []);
});


test('Test_UpdateMapForCurrentControls_TestSpecificDay_ExpectIso', () => {
   const updates = [];
   const preset = 'specific-day';
   const iso = '2026-06-15';

   MapControlsBinder.updateMapForCurrentControls({
      mapPreset: { value: preset },
      mapDateInput: { value: iso },
      onUpdate: (...args) => updates.push(args),
   });

   assert.deepEqual(updates, [[preset, iso]]);
});


test('Test_UpdateMapForCurrentControls_TestToday_ExpectNullDate', () => {
   const updates = [];
   const preset = 'today';

   MapControlsBinder.updateMapForCurrentControls({
      mapPreset: { value: preset },
      mapDateInput: { value: '' },
      fp: { input: { value: '' } },
      onUpdate: (...args) => updates.push(args),
   });

   assert.deepEqual(updates.at(Position.LAST), [preset, null]);
});


test('Test_BindChangeListeners_TestInputs_ExpectHandlers', () => {
   const calls = [];
   const first = document.createElement('input');
   const second = document.createElement('input');

   MapControlsBinder.bindChangeListeners([first, null, second], () => calls.push(true));
   first.listeners.change();
   second.listeners.change();

   assert.equal(calls.length, 2);
});


test('Test_BindChangeListeners_TestMissing_ExpectNoOp', () => {
   const bind = () => MapControlsBinder.bindChangeListeners(null, () => {});

   assert.doesNotThrow(bind);
});


test('Test_InitMapDatePicker_TestCallbacks_ExpectFlatpickrOptions', () => {
   const originalInit = VisitDateAdapter.initVisitDateFlatpickr;
   const originalToday = VisitDateValidator.getToday;
   const originalBlur = MapControlsBinder.blurMapDateInput;
   const optionsSeen = [];
   const specificDayChanges = [];
   const blurs = [];
   const floor = new Date('2026-06-01T12:00:00');
   const iso = '2026-06-15';

   VisitDateValidator.getToday = () => floor;
   MapControlsBinder.blurMapDateInput = (input) => {
      blurs.push(input);
   };
   VisitDateAdapter.initVisitDateFlatpickr = (input, options) => {
      optionsSeen.push({ input, options });
      return { id: 'fp', close() {}, open() {} };
   };

   try {
      const mapDateInput = { id: 'date' };
      const fp = MapControlsBinder.initMapDatePicker(mapDateInput, {
         mapPreset: { value: 'specific-day' },
         onSpecificDayChange: (nextIso) => specificDayChanges.push(nextIso),
      });
      const instance = { close() { instance.closed = true; } };
      optionsSeen.at(Position.FIRST).options.onChange(null, iso, instance);
      optionsSeen.at(Position.FIRST).options.onClose();

      assert.equal(fp.id, 'fp');
      assert.equal(optionsSeen.at(Position.FIRST).options.defaultDate, floor);
      assert.equal(optionsSeen.at(Position.FIRST).options.earliestNoon, floor);
      assert.equal(optionsSeen.at(Position.FIRST).options.clickOpens, false);
      assert.equal(instance.closed, true);
      assert.deepEqual(specificDayChanges, [iso]);
      assert.equal(blurs.length, 2);
   } finally {
      VisitDateAdapter.initVisitDateFlatpickr = originalInit;
      VisitDateValidator.getToday = originalToday;
      MapControlsBinder.blurMapDateInput = originalBlur;
   }
});


test('Test_InitMapDatePicker_TestTodayFloor_ExpectEarliestNoon', () => {
   const originalInit = VisitDateAdapter.initVisitDateFlatpickr;
   const originalToday = VisitDateValidator.getToday;
   const originalBlur = MapControlsBinder.blurMapDateInput;
   const optionsSeen = [];
   const earliestSelectableNoon = new Date('2026-07-01T12:00:00');
   VisitDateValidator.getToday = () => new Date('2026-06-01T12:00:00');
   MapControlsBinder.blurMapDateInput = () => {};
   VisitDateAdapter.initVisitDateFlatpickr = (input, options) => {
      optionsSeen.push({ input, options });
      return { id: 'fp', close() {}, open() {} };
   };

   try {
      MapControlsBinder.initMapDatePicker({ id: 'date' }, {
         mapPreset: { value: 'today' },
         earliestSelectableNoon,
         onSpecificDayChange: () => {},
      });
      optionsSeen.at(Position.FIRST).options.onChange(null, '2026-07-02', { close() {} });

      assert.equal(
         optionsSeen.at(Position.FIRST).options.defaultDate.toISOString(),
         earliestSelectableNoon.toISOString()
      );
   } finally {
      VisitDateAdapter.initVisitDateFlatpickr = originalInit;
      VisitDateValidator.getToday = originalToday;
      MapControlsBinder.blurMapDateInput = originalBlur;
   }
});


test('Test_HandlePresetChange_TestEmpty_ExpectCloseOnly', () => {
   const updates = [];
   const closes = [];
   const originalSync = MapControlsBinder.syncDateInputVisibility;
   const originalClose = MapControlsBinder.closeMapDatePicker;
   const originalUpdate = MapControlsBinder.updateMapForCurrentControls;
   MapControlsBinder.syncDateInputVisibility = () => {};
   MapControlsBinder.closeMapDatePicker = () => {
      closes.push(true);
   };
   MapControlsBinder.updateMapForCurrentControls = (options) => {
      updates.push(options.mapPreset.value);
   };

   try {
      MapControlsBinder.handlePresetChange({
         mapPreset: { value: '' },
         mapDateInput: {},
         fp: {},
         onUpdate: () => {},
      });

      assert.deepEqual(updates, []);
      assert.equal(closes.length, Position.SECOND);
   } finally {
      MapControlsBinder.syncDateInputVisibility = originalSync;
      MapControlsBinder.closeMapDatePicker = originalClose;
      MapControlsBinder.updateMapForCurrentControls = originalUpdate;
   }
});


test('Test_HandlePresetChange_TestToday_ExpectUpdate', () => {
   const updates = [];
   const originalSync = MapControlsBinder.syncDateInputVisibility;
   const originalClose = MapControlsBinder.closeMapDatePicker;
   const originalUpdate = MapControlsBinder.updateMapForCurrentControls;
   const preset = 'today';
   MapControlsBinder.syncDateInputVisibility = () => {};
   MapControlsBinder.closeMapDatePicker = () => {};
   MapControlsBinder.updateMapForCurrentControls = (options) => {
      updates.push(options.mapPreset.value);
   };

   try {
      MapControlsBinder.handlePresetChange({
         mapPreset: { value: preset },
         mapDateInput: {},
         fp: {},
         onUpdate: () => {},
      });

      assert.deepEqual(updates, [preset]);
   } finally {
      MapControlsBinder.syncDateInputVisibility = originalSync;
      MapControlsBinder.closeMapDatePicker = originalClose;
      MapControlsBinder.updateMapForCurrentControls = originalUpdate;
   }
});


test('Test_InitMapControls_TestMissingElements_ExpectNull', () => {
   const originalWarn = console.warn;
   const warnings = [];
   console.warn = (...args) => {
      warnings.push(args);
   };

   try {
      const api = MapControlsBinder.initMapControls({});

      assert.equal(api, null);
      assert.equal(warnings.length, Position.SECOND);
   } finally {
      console.warn = originalWarn;
   }
});


test('Test_InitMapControls_TestWired_ExpectRefetchAndEvents', () => {
   const originalInitPicker = MapControlsBinder.initMapDatePicker;
   const originalHandlePreset = MapControlsBinder.handlePresetChange;
   const originalUpdate = MapControlsBinder.updateMapForCurrentControls;
   const originalSync = MapControlsBinder.syncDateInputVisibility;
   const originalBlur = MapControlsBinder.blurMapDateInput;
   const opens = [];
   const updates = [];
   const syncs = [];
   const blurs = [];
   let pickerOptions = null;
   const fp = {
      open: () => opens.push(true),
      close() {},
   };
   const iso = '2026-06-20';

   MapControlsBinder.initMapDatePicker = (_input, options) => {
      pickerOptions = options;
      return fp;
   };
   MapControlsBinder.handlePresetChange = (options) => {
      updates.push(['preset', options.mapPreset.value]);
   };
   MapControlsBinder.updateMapForCurrentControls = (options) => {
      updates.push(['update', options.mapPreset.value]);
   };
   MapControlsBinder.syncDateInputVisibility = () => {
      syncs.push(true);
   };
   MapControlsBinder.blurMapDateInput = (input) => {
      blurs.push(input);
   };

   const mapPreset = document.createElement('select');
   mapPreset.value = 'specific-day';
   const mapDateInput = document.createElement('input');
   const includeOffDisplayCheckbox = document.createElement('input');
   includeOffDisplayCheckbox.type = 'checkbox';
   const radio = document.createElement('input');
   radio.type = 'radio';

   try {
      const api = MapControlsBinder.initMapControls({
         mapPreset,
         mapDateInput,
         includeOffDisplayCheckbox,
         includeClosedRestaurantsCheckbox: null,
         includeClosedRestroomsCheckbox: null,
         includeClosedGiftShopsCheckbox: null,
         includeClosedAttractionsCheckbox: null,
         transportationRouteRadios: [radio],
         earliestSelectableNoon: new Date('2026-06-01T12:00:00'),
         onUpdate: (...args) => updates.push(['onUpdate', ...args]),
      });
      pickerOptions.onSpecificDayChange(iso);
      mapPreset.listeners.change();
      mapDateInput.listeners.mousedown({ preventDefault() {} });
      mapDateInput.listeners.focus();
      includeOffDisplayCheckbox.listeners.change();
      radio.listeners.change();
      mapPreset.value = 'today';
      mapDateInput.listeners.mousedown({ preventDefault() {} });
      api.refetch();

      assert.equal(api.flatpickr, fp);
      assert.equal(typeof api.refetch, 'function');
      assert.equal(syncs.length, Position.SECOND);
      assert.deepEqual(updates.at(Position.FIRST), ['onUpdate', 'specific-day', iso]);
      assert.ok(updates.some(([kind]) => kind === 'preset'));
      assert.deepEqual(opens, [true]);
      assert.equal(blurs.at(Position.LAST), mapDateInput);
      assert.ok(updates.some(([kind]) => kind === 'update'));
      assert.equal(opens.length, Position.SECOND);
   } finally {
      MapControlsBinder.initMapDatePicker = originalInitPicker;
      MapControlsBinder.handlePresetChange = originalHandlePreset;
      MapControlsBinder.updateMapForCurrentControls = originalUpdate;
      MapControlsBinder.syncDateInputVisibility = originalSync;
      MapControlsBinder.blurMapDateInput = originalBlur;
   }
});
