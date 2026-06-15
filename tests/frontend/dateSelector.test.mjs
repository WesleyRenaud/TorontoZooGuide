import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { createItineraryDateSelectorController } from '../../scripts/itinerary/selectors/dateSelector.js';
import { buildDateSelectorView } from '../../scripts/itinerary/selectors/dateSelectorView.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

function makeNoonDate(year, monthIndex, day) {
   return new Date(year, monthIndex, day, 12, 0, 0, 0);
}

const floor = makeNoonDate(2026, 5, 15);

function createStubPicker() {
   return {
      init() {},
      close() {},
      syncBounds() {},
   };
}

test.describe('dateSelector', () => {
   beforeEach(() => {
      installTestWindow();
      installDocument();
   });

   afterEach(() => {
      teardownDocument();
      delete globalThis.window;
   });

   test('buildDateSelectorView renders the visit-date selector shell', () => {
      const view = buildDateSelectorView();

      assert.equal(view.root.className, 'itin-overlay');
      assert.equal(
         view.root.querySelector('.itin-h1')?.textContent,
         APP_STRINGS.itinerary.selectors.titleDate
      );
      assert.equal(view.inputEl.className, 'itin-date-input');
      assert.equal(
         view.nextButtonEl.textContent,
         APP_STRINGS.itinerary.actions.next
      );
   });

   test('createItineraryDateSelectorController show and hide manage the mount element', () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const controller = createItineraryDateSelectorController({
         mountEl,
         earliestSelectableDate: floor,
         deps: {
            getTodayFn: () => floor,
            createPicker: createStubPicker,
         },
      });

      controller.show();

      assert.equal(mountEl.children.length, 1);
      assert.ok(mountEl.querySelector('.itin-date-input'));

      controller.hide();

      assert.equal(mountEl.children.length, 0);
   });

   test('createItineraryDateSelectorController commits the selected date on next', () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const savedDates = [];
      const controller = createItineraryDateSelectorController({
         mountEl,
         earliestSelectableDate: floor,
         onSave: (isoDate) => {
            savedDates.push(isoDate);
         },
         deps: {
            getTodayFn: () => floor,
            createPicker: createStubPicker,
         },
      });

      controller.show();
      controller.setDate(makeNoonDate(2026, 5, 16));
      mountEl.querySelector('.itin-next')?.click();

      assert.deepEqual(savedDates, ['2026-06-16']);
      assert.equal(mountEl.children.length, 1);
   });

   test('createItineraryDateSelectorController calls onClose from the close button', () => {
      const mountEl = createDomNode('div', 'wizard-mount');
      const closeCalls = [];
      const controller = createItineraryDateSelectorController({
         mountEl,
         earliestSelectableDate: floor,
         onClose: () => {
            closeCalls.push('closed');
         },
         deps: {
            getTodayFn: () => floor,
            createPicker: createStubPicker,
         },
      });

      controller.show();
      mountEl.querySelector('.itin-close')?.click();

      assert.deepEqual(closeCalls, ['closed']);
   });
});
