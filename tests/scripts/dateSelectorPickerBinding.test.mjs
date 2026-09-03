import assert from 'node:assert/strict';
import test from 'node:test';

import { createDatePickerBinding } from '../../scripts/itinerary/selectors/dateSelectorPickerBinding.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { makeNoonDate } from './helpers/visitDateMock.mjs';

const floor = makeNoonDate(2026, 5, 15);
const maxDate = makeNoonDate(2026, 5, 17);

test('createDatePickerBinding wires flatpickr callbacks into the selection model', () => {
   const inputEl = createDomNode('input', 'itin-date-input');
   const syncedDates = [];
   let currentDate = floor;
   let syncedMaxDate = null;
   const flatpickrCalls = [];

   const binding = createDatePickerBinding({
      inputEl,
      getDate: () => currentDate,
      setDate: (date, { updateInput = true } = {}) => {
         currentDate = date;

         if (updateInput) {
            syncedDates.push(date);
         }

         return true;
      },
      syncInputValue: (date) => {
         syncedDates.push(date);
      },
      earliestDateFloor: floor,
      getTodayFn: () => floor,
      getMaxDateFn: () => maxDate,
      daysAhead: 2,
      initFlatpickr: (_input, options) => {
         const instance = {
            input: _input,
            close() {
               flatpickrCalls.push('close');
            },
            set(property, value) {
               if (property === 'maxDate') {
                  syncedMaxDate = value;
               }

               flatpickrCalls.push(`${property}:${value}`);
            },
            setDate() {},
         };

         options.onReady(floor, '2026-06-15', instance);
         options.onChange(makeNoonDate(2026, 5, 16), '2026-06-16', instance);
         options.onClose();

         return instance;
      },
   });

   binding.init();
   binding.syncBounds();
   binding.close();

   assert.equal(currentDate.getDate(), 16);
   assert.match(inputEl.value, /June 16, 2026/);
   assert.equal(syncedDates.length, 3);
   assert.equal(syncedMaxDate, maxDate);
   assert.ok(flatpickrCalls.includes('close'));
});
