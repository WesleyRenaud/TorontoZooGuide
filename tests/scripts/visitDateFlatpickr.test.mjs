import assert from 'node:assert/strict';
import { test } from 'node:test';

import { initVisitDateFlatpickr } from '../../scripts/visitDates/visitDateFlatpickr.js';
import { VisitDateRules } from '../../scripts/visitDates/visitDateRules.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { makeNoonDate } from './helpers/visitDateMock.mjs';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

const floor = makeNoonDate(2026, 5, 15);

test.describe('initVisitDateFlatpickr', () => {
   installDomTestHooks();

   test('returns null when the input element is missing', () => {
      assert.equal(initVisitDateFlatpickr(null), null);
   });

   test('marks the input readonly and wires flatpickr callbacks', () => {
      const inputEl = createDomNode('input', 'itin-date-input');
      const readyCalls = [];
      const changeCalls = [];
      const closeCalls = [];
      const flatpickrOptions = [];

      const instance = initVisitDateFlatpickr(inputEl, {
         defaultDate: makeNoonDate(2026, 5, 16),
         daysAhead: 2,
         earliestNoon: floor,
         getTodayFn: () => floor,
         getMaxDateFn: () => makeNoonDate(2026, 5, 17),
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

            options.onReady(
               [makeNoonDate(2026, 5, 16)],
               '2026-06-16',
               picker
            );
            options.onChange(
               [makeNoonDate(2026, 5, 17)],
               '2026-06-17',
               picker
            );
            options.onClose([], '', picker);

            return picker;
         },
      });

      assert.ok(instance);
      assert.equal(inputEl.getAttribute('readonly'), 'true');
      assert.equal(flatpickrOptions.length, 1);
      assert.equal(flatpickrOptions[0].minDate, floor);
      assert.equal(flatpickrOptions[0].clickOpens, true);
      assert.equal(readyCalls.length, 1);
      assert.equal(changeCalls.length, 1);
      assert.equal(closeCalls.length, 1);
      assert.equal(readyCalls[0][1], '2026-06-16');
      assert.equal(changeCalls[0][1], '2026-06-17');
   });

   test('derives maxDate from getTodayFn when getMaxDateFn is omitted', () => {
      const inputEl = createDomNode('input', 'itin-date-input');
      const flatpickrOptions = [];

      initVisitDateFlatpickr(inputEl, {
         defaultDate: makeNoonDate(2026, 5, 16),
         daysAhead: 2,
         earliestNoon: floor,
         getTodayFn: () => floor,
         initFlatpickr: (_input, options) => {
            flatpickrOptions.push(options);
            return { setDate() {} };
         },
      });

      assert.equal(VisitDateRules.toISODate(flatpickrOptions[0].maxDate), '2026-06-17');
   });
});
