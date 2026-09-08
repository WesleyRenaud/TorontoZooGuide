import assert from 'node:assert/strict';
import test from 'node:test';

import { MapControlsBinder } from '../../../scripts/map/mapControlsBinder.js';
import { VisitDateAdapter } from '../../../scripts/visitDates/visitDateAdapter.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
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

   MapControlsBinder.blurMapDateInput = (input) => { blurs.push(input); };

   try {
      MapControlsBinder.closeMapDatePicker({ close: () => closes.push(true) }, 'input');
      MapControlsBinder.closeMapDatePicker(null, 'input');
      assert.deepEqual(closes, [true]);
      assert.deepEqual(blurs, ['input', 'input']);
   } finally {
      MapControlsBinder.blurMapDateInput = originalBlur;
   }
});

test('Test_IsSpecificDayPreset_TestValues_ExpectBoolean', () => {
   assert.equal(MapControlsBinder.isSpecificDayPreset({ value: 'specific-day' }), true);
   assert.equal(MapControlsBinder.isSpecificDayPreset({ value: 'today' }), false);
   assert.equal(MapControlsBinder.isSpecificDayPreset(null), false);
});

test('Test_GetCurrentDateStr_TestFallback_ExpectInputOrFp', () => {
   assert.equal(MapControlsBinder.getCurrentDateStr({ value: '2026-06-15' }, null), '2026-06-15');
   assert.equal(
      MapControlsBinder.getCurrentDateStr({ value: '' }, { input: { value: '2026-06-16' } }),
      '2026-06-16'
   );
   assert.equal(MapControlsBinder.getCurrentDateStr(null, null), '');
});

test('Test_SyncDateInputVisibility_TestPreset_ExpectDisplay', () => {
   const mapDateInput = { style: { display: '' } };

   MapControlsBinder.syncDateInputVisibility({ value: 'specific-day' }, mapDateInput);
   assert.equal(mapDateInput.style.display, 'inline-block');

   MapControlsBinder.syncDateInputVisibility({ value: 'today' }, mapDateInput);
   assert.equal(mapDateInput.style.display, 'none');
});

test('Test_UpdateMapForCurrentControls_TestPresets_ExpectOnUpdate', () => {
   const updates = [];
   const onUpdate = (...args) => updates.push(args);

   MapControlsBinder.updateMapForCurrentControls({
      mapPreset: { value: '' },
      mapDateInput: { value: '2026-06-15' },
      onUpdate,
   });
   assert.deepEqual(updates, []);

   MapControlsBinder.updateMapForCurrentControls({
      mapPreset: { value: 'specific-day' },
      mapDateInput: { value: '' },
      fp: { input: { value: '' } },
      onUpdate,
   });
   assert.deepEqual(updates, []);

   MapControlsBinder.updateMapForCurrentControls({
      mapPreset: { value: 'specific-day' },
      mapDateInput: { value: '2026-06-15' },
      onUpdate,
   });
   assert.deepEqual(updates, [['specific-day', '2026-06-15']]);

   MapControlsBinder.updateMapForCurrentControls({
      mapPreset: { value: 'today' },
      mapDateInput: { value: '' },
      fp: { input: { value: '' } },
      onUpdate,
   });
   assert.deepEqual(updates.at(-1), ['today', null]);
});

test('Test_BindChangeListeners_TestInputs_ExpectHandlers', () => {
   const calls = [];
   const a = document.createElement('input');
   const b = document.createElement('input');

   MapControlsBinder.bindChangeListeners([a, null, b], () => calls.push(true));
   a.listeners.change();
   b.listeners.change();
   assert.equal(calls.length, 2);

   MapControlsBinder.bindChangeListeners(null, () => {});
});

test('Test_InitMapDatePicker_TestCallbacks_ExpectFlatpickrOptions', () => {
   const originalInit = VisitDateAdapter.initVisitDateFlatpickr;
   const originalToday = VisitDateValidator.getToday;
   const originalBlur = MapControlsBinder.blurMapDateInput;
   const optionsSeen = [];
   const specificDayChanges = [];
   const blurs = [];
   const floor = new Date('2026-06-01T12:00:00');

   VisitDateValidator.getToday = () => floor;
   MapControlsBinder.blurMapDateInput = (input) => { blurs.push(input); };
   VisitDateAdapter.initVisitDateFlatpickr = (input, options) => {
      optionsSeen.push({ input, options });
      return { id: 'fp', close() {}, open() {} };
   };

   try {
      const mapDateInput = { id: 'date' };
      const fp = MapControlsBinder.initMapDatePicker(mapDateInput, {
         mapPreset: { value: 'specific-day' },
         onSpecificDayChange: (iso) => specificDayChanges.push(iso),
      });

      assert.equal(fp.id, 'fp');
      assert.equal(optionsSeen[0].options.defaultDate, floor);
      assert.equal(optionsSeen[0].options.earliestNoon, floor);
      assert.equal(optionsSeen[0].options.clickOpens, false);

      const instance = { close() { instance.closed = true; } };
      optionsSeen[0].options.onChange(null, '2026-06-15', instance);
      assert.equal(instance.closed, true);
      assert.deepEqual(specificDayChanges, ['2026-06-15']);
      assert.equal(blurs.length, 1);

      optionsSeen[0].options.onClose();
      assert.equal(blurs.length, 2);

      MapControlsBinder.initMapDatePicker(mapDateInput, {
         mapPreset: { value: 'today' },
         earliestSelectableNoon: new Date('2026-07-01T12:00:00'),
         onSpecificDayChange: () => {},
      });
      assert.equal(
         optionsSeen[1].options.defaultDate.toISOString(),
         new Date('2026-07-01T12:00:00').toISOString()
      );
      optionsSeen[1].options.onChange(null, '2026-07-02', { close() {} });
      assert.deepEqual(specificDayChanges, ['2026-06-15']);
   } finally {
      VisitDateAdapter.initVisitDateFlatpickr = originalInit;
      VisitDateValidator.getToday = originalToday;
      MapControlsBinder.blurMapDateInput = originalBlur;
   }
});

test('Test_HandlePresetChange_TestEmptyAndValid_ExpectUpdate', () => {
   const updates = [];
   const closes = [];
   const originalSync = MapControlsBinder.syncDateInputVisibility;
   const originalClose = MapControlsBinder.closeMapDatePicker;
   const originalUpdate = MapControlsBinder.updateMapForCurrentControls;

   MapControlsBinder.syncDateInputVisibility = () => {};
   MapControlsBinder.closeMapDatePicker = () => { closes.push(true); };
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
      assert.equal(closes.length, 1);

      MapControlsBinder.handlePresetChange({
         mapPreset: { value: 'today' },
         mapDateInput: {},
         fp: {},
         onUpdate: () => {},
      });
      assert.deepEqual(updates, ['today']);
   } finally {
      MapControlsBinder.syncDateInputVisibility = originalSync;
      MapControlsBinder.closeMapDatePicker = originalClose;
      MapControlsBinder.updateMapForCurrentControls = originalUpdate;
   }
});

test('Test_InitMapControls_TestMissingElements_ExpectNull', () => {
   const originalWarn = console.warn;
   const warnings = [];
   console.warn = (...args) => { warnings.push(args); };

   try {
      assert.equal(MapControlsBinder.initMapControls({}), null);
      assert.equal(warnings.length, 1);
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

   MapControlsBinder.initMapDatePicker = (input, options) => {
      pickerOptions = options;
      return fp;
   };
   MapControlsBinder.handlePresetChange = (options) => {
      updates.push(['preset', options.mapPreset.value]);
   };
   MapControlsBinder.updateMapForCurrentControls = (options) => {
      updates.push(['update', options.mapPreset.value]);
   };
   MapControlsBinder.syncDateInputVisibility = () => { syncs.push(true); };
   MapControlsBinder.blurMapDateInput = (input) => { blurs.push(input); };

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

      assert.equal(api.flatpickr, fp);
      assert.equal(typeof api.refetch, 'function');
      assert.equal(syncs.length, 1);

      pickerOptions.onSpecificDayChange('2026-06-20');
      assert.deepEqual(updates.at(-1), ['onUpdate', 'specific-day', '2026-06-20']);

      mapPreset.listeners.change();
      assert.deepEqual(updates.at(-1), ['preset', 'specific-day']);

      mapDateInput.listeners.mousedown({ preventDefault() {} });
      assert.deepEqual(opens, [true]);

      mapDateInput.listeners.focus();
      assert.equal(blurs.at(-1), mapDateInput);

      includeOffDisplayCheckbox.listeners.change();
      radio.listeners.change();
      assert.ok(updates.some(([kind]) => kind === 'update'));

      mapPreset.value = 'today';
      mapDateInput.listeners.mousedown({ preventDefault() {} });
      assert.equal(opens.length, 1);

      api.refetch();
   } finally {
      MapControlsBinder.initMapDatePicker = originalInitPicker;
      MapControlsBinder.handlePresetChange = originalHandlePreset;
      MapControlsBinder.updateMapForCurrentControls = originalUpdate;
      MapControlsBinder.syncDateInputVisibility = originalSync;
      MapControlsBinder.blurMapDateInput = originalBlur;
   }
});
