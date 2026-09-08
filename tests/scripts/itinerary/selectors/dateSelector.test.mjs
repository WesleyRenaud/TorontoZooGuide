import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DateSelector } from '../../../../scripts/itinerary/selectors/dateSelector.js';
import { DateSelectorView } from '../../../../scripts/itinerary/selectors/dateSelectorView.js';
import { Strings } from '../../../../scripts/strings.js';
import { VisitDateValidator } from '../../../../scripts/visitDates/visitDateValidator.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';

const floor = makeNoonDate(2026, 5, 15);

function _createStubPicker() {
   return {
      init() {},
      close() {},
      syncBounds() {},
   };
}

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
   },
   after: () => {
      delete globalThis.localStorage;
   },
});

test('Test_DateSelectorView_TestDateSelectorViewBuildDateSelectorViewRendersTheVisitDateSelectorShell_ExpectOk', () => {
   const view = DateSelectorView.buildDateSelectorView();

   assert.equal(view.root.className, 'itin-overlay');
   assert.equal(
      view.root.querySelector('.itin-h1')?.textContent,
      Strings.itinerary.selectors.titleDate
   );
   assert.equal(view.inputEl.className, 'itin-date-input');
   assert.equal(
      view.nextButtonEl.textContent,
      Strings.itinerary.actions.next
   );
});

test('Test_DateSelector_TestDateSelectorCreateItineraryDateSelectorControllerShowAndHideManageTheMount_ExpectOk', () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const controller = DateSelector.createItineraryDateSelectorController({
      mountEl,
      earliestSelectableDate: floor,
      deps: {
         getTodayFn: () => floor,
         createPicker: _createStubPicker,
      },
   });

   controller.show();

   assert.equal(mountEl.children.length, 1);
   assert.ok(mountEl.querySelector('.itin-date-input'));

   controller.hide();

   assert.equal(mountEl.children.length, 0);
});

test('Test_DateSelector_TestDateSelectorCreateItineraryDateSelectorControllerCommitsTheSelectedDateOnNext_ExpectOk', () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const savedDates = [];
   const controller = DateSelector.createItineraryDateSelectorController({
      mountEl,
      earliestSelectableDate: floor,
      onSave: (isoDate) => {
         savedDates.push(isoDate);
      },
      deps: {
         getTodayFn: () => floor,
         createPicker: _createStubPicker,
      },
   });

   controller.show();
   controller.setDate(makeNoonDate(2026, 5, 16));
   mountEl.querySelector('.itin-next')?.click();

   assert.deepEqual(savedDates, ['2026-06-16']);
   assert.equal(mountEl.children.length, 1);
});

test('Test_DateSelector_TestDateSelectorCreateItineraryDateSelectorControllerCallsOnCloseFromTheCloseButton_ExpectOk', () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const closeCalls = [];
   const controller = DateSelector.createItineraryDateSelectorController({
      mountEl,
      earliestSelectableDate: floor,
      onClose: () => {
         closeCalls.push('closed');
      },
      deps: {
         getTodayFn: () => floor,
         createPicker: _createStubPicker,
      },
   });

   controller.show();
   mountEl.querySelector('.itin-close')?.click();

   assert.deepEqual(closeCalls, ['closed']);
});

test('Test_DateSelector_TestMissingMountTitlesFinishAndHideNext_ExpectBranches', () => {
   const finished = [];
   const mountEl = createDomNode('div', 'wizard-mount');
   const controller = DateSelector.createItineraryDateSelectorController({
      mountEl,
      earliestSelectableDate: floor,
      hideNextButton: true,
      titleText: 'Pick a day',
      subtitleText: 'Visit soon',
      onFinish: (isoDate) => { finished.push(isoDate); },
      deps: {
         getTodayFn: () => floor,
         createPicker: _createStubPicker,
      },
   });

   controller.show();
   controller.show();
   assert.equal(mountEl.querySelector('.itin-h1')?.textContent, 'Pick a day');
   assert.equal(mountEl.querySelector('.itin-subtitle')?.textContent, 'Visit soon');
   const nextOnly = [...mountEl.querySelectorAll('.itin-next')]
      .find((button) => !button.classList.contains('itin-finish'));
   assert.equal(nextOnly?.hidden, true);

   controller.setDate(makeNoonDate(2026, 5, 17));
   mountEl.querySelector('.itin-finish')?.click();
   assert.deepEqual(finished, ['2026-06-17']);

   const noMount = DateSelector.createItineraryDateSelectorController({
      earliestSelectableDate: floor,
      deps: {
         getTodayFn: () => floor,
         createPicker: _createStubPicker,
      },
   });
   assert.doesNotThrow(() => {
      noMount.show();
      noMount.hide();
   });

   const noInput = DateSelector.createItineraryDateSelectorController({
      mountEl: createDomNode('div'),
      earliestSelectableDate: floor,
      deps: {
         getTodayFn: () => floor,
         createPicker: _createStubPicker,
         buildView: () => ({
            root: createDomNode('div'),
            inputEl: null,
            nextButtonEl: createDomNode('button', 'itin-next'),
            finishButtonEl: createDomNode('button', 'itin-finish'),
            closeButtonEl: createDomNode('button', 'itin-close'),
         }),
      },
   });
   assert.doesNotThrow(() => {
      noInput.show();
   });

   const blockedMount = createDomNode('div', 'wizard-mount');
   const saved = [];
   const blocked = DateSelector.createItineraryDateSelectorController({
      mountEl: blockedMount,
      earliestSelectableDate: floor,
      onSave: (isoDate) => { saved.push(isoDate); },
      deps: {
         getTodayFn: () => floor,
         createPicker: _createStubPicker,
      },
   });
   blocked.show();
   const originalNormalize = VisitDateValidator.normalizeDate;
   VisitDateValidator.normalizeDate = () => null;
   try {
      [...blockedMount.querySelectorAll('.itin-next')]
         .find((button) => !button.classList.contains('itin-finish'))
         ?.click();
      assert.deepEqual(saved, []);
   } finally {
      VisitDateValidator.normalizeDate = originalNormalize;
   }
});
