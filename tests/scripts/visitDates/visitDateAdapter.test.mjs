import assert from 'node:assert/strict';
import { test } from 'node:test';

import { VisitDateAdapter } from '../../../scripts/visitDates/visitDateAdapter.js';
import { VisitDateValidator } from '../../../scripts/visitDates/visitDateValidator.js';
import { createDomNode } from '../helpers/domNodeMock.mjs';
import { makeNoonDate } from '../helpers/visitDateMock.mjs';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';
import { Position } from '../../../scripts/shared/enums/position.js';

const floor = makeNoonDate(2026, 5, 15);

installDomTestHooks();


test('Test_InitVisitDateFlatpickr_TestMissingInput_ExpectNull', () => {
   const inputEl = null;

   const instance = VisitDateAdapter.initVisitDateFlatpickr(inputEl);

   assert.equal(instance, null);
});


test('Test_InitVisitDateFlatpickr_TestCallbacks_ExpectReadonlyWired', () => {
   const inputEl = createDomNode('input', 'itin-date-input');
   const readyCalls = [];
   const changeCalls = [];
   const closeCalls = [];
   const flatpickrOptions = [];
   const readyDate = makeNoonDate(2026, 5, 16);
   const changeDate = makeNoonDate(2026, 5, 17);
   const readyIso = VisitDateValidator.toISODate(readyDate);
   const changeIso = VisitDateValidator.toISODate(changeDate);

   const instance = VisitDateAdapter.initVisitDateFlatpickr(inputEl, {
      defaultDate: readyDate,
      daysAhead: 2,
      earliestNoon: floor,
      getTodayFn: () => floor,
      getMaxDateFn: () => changeDate,
      onReady: (...args) => {
         readyCalls.push(args);
      },
      onChange: (...args) => {
         changeCalls.push(args);
      },
      onClose: (...args) => {
         closeCalls.push(args);
      },
      initFlatpickr: (_input, options) => {
         flatpickrOptions.push(options);
         const picker = {
            setDate() {},
         };
         options.onReady([readyDate], readyIso, picker);
         options.onChange([changeDate], changeIso, picker);
         options.onClose([], '', picker);
         return picker;
      },
   });

   assert.ok(instance);
   assert.equal(inputEl.getAttribute('readonly'), 'true');
   assert.equal(flatpickrOptions.length, Position.SECOND);
   assert.equal(flatpickrOptions.at(Position.FIRST).minDate, floor);
   assert.equal(flatpickrOptions.at(Position.FIRST).clickOpens, true);
   assert.equal(readyCalls.length, Position.SECOND);
   assert.equal(changeCalls.length, Position.SECOND);
   assert.equal(closeCalls.length, Position.SECOND);
   assert.equal(readyCalls.at(Position.FIRST).at(Position.SECOND), readyIso);
   assert.equal(changeCalls.at(Position.FIRST).at(Position.SECOND), changeIso);
});


test('Test_InitVisitDateFlatpickr_TestOmitMaxDateFn_ExpectDerivedMax', () => {
   const inputEl = createDomNode('input', 'itin-date-input');
   const flatpickrOptions = [];
   const daysAhead = 2;
   const defaultDate = makeNoonDate(2026, 5, 16);

   VisitDateAdapter.initVisitDateFlatpickr(inputEl, {
      defaultDate,
      daysAhead,
      earliestNoon: floor,
      getTodayFn: () => floor,
      initFlatpickr: (_input, options) => {
         flatpickrOptions.push(options);
         return { setDate() {} };
      },
   });

   assert.equal(
      VisitDateValidator.toISODate(flatpickrOptions.at(Position.FIRST).maxDate),
      VisitDateValidator.toISODate(VisitDateValidator.getMaxDate(daysAhead, floor))
   );
});
