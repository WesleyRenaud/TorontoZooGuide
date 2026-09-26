import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DateSelector } from '../../../../scripts/itinerary/selectors/dateSelector.js';
import { DateSelectorView } from '../../../../scripts/itinerary/selectors/dateSelectorView.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { VisitDateValidator } from '../../../../scripts/visitDates/visitDateValidator.js';
import { createDomNode } from '../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';
import { createLocalStorageMock } from '../../helpers/localStorageMock.mjs';
import { makeNoonDate } from '../../helpers/visitDateMock.mjs';

const floor = makeNoonDate(2026, 5, 15);
const _openTime = '9:30 AM';
const _closeTime = '6:00 PM';
const _lastAdmissionTime = '5:00 PM';
const _zooHours = {
   openTime: _openTime,
   closeTime: _closeTime,
   lastAdmissionTime: _lastAdmissionTime,
};

function _createStubPicker() {
   return {
      init() {},
      close() {},
      syncBounds() {},
   };
}

function _createStubTimeInput({ label }) {
   const field = createDomNode('label', 'itinerary-day-time-control');
   field.appendChild(createDomNode('span', 'itinerary-day-time-control-label', label));
   return field;
}

function _createController(options = {}) {
   const { deps = {}, ...controllerOptions } = options;

   return DateSelector.createItineraryDateSelectorController({
      earliestSelectableDate: floor,
      ...controllerOptions,
      deps: {
         getTodayFn: () => floor,
         createPicker: _createStubPicker,
         getZooHoursFn: async () => _zooHours,
         makeTimeInput: _createStubTimeInput,
         ...deps,
      },
   });
}

installDomTestHooks({
   before: () => {
      globalThis.localStorage = createLocalStorageMock();
   },
   after: () => {
      delete globalThis.localStorage;
   },
});


test('Test_BuildDateSelectorView_TestShell_ExpectVisitDateParts', () => {
   const view = DateSelectorView.buildDateSelectorView();

   assert.equal(view.root.className, 'itin-overlay');
   assert.equal(
      view.root.querySelector('.itin-h1')?.textContent,
      Strings.itinerary.selectors.titleDate
   );
   assert.equal(view.inputEl.className, 'itin-date-input');
   assert.equal(view.nextButtonEl.textContent, Strings.itinerary.actions.next);
});


test('Test_CreateItineraryDateSelectorController_TestShowAndHide_ExpectMountManaged', () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const controller = _createController({
      mountEl,
   });

   controller.show();

   assert.equal(mountEl.children.length, 1);
   assert.ok(mountEl.querySelector('.itin-date-input'));

   controller.hide();

   assert.equal(mountEl.children.length, 0);
});


test('Test_CreateItineraryDateSelectorController_TestNext_ExpectSavedDate', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const savedDates = [];
   const selectedDate = makeNoonDate(2026, 5, 16);
   const controller = _createController({
      mountEl,
      onSave: (isoDate) => {
         savedDates.push(isoDate);
      },
   });
   controller.show();
   controller.setDate(selectedDate);

   mountEl.querySelector('.itin-next')?.click();
   await Promise.resolve();

   assert.deepEqual(savedDates, [VisitDateValidator.toISODate(selectedDate)]);
   assert.equal(mountEl.children.length, 1);
});


test('Test_CreateItineraryDateSelectorController_TestClose_ExpectOnClose', () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const closeCalls = [];
   const closed = 'closed';
   const controller = _createController({
      mountEl,
      onClose: () => {
         closeCalls.push(closed);
      },
   });
   controller.show();

   mountEl.querySelector('.itin-close')?.click();

   assert.deepEqual(closeCalls, [closed]);
});


test('Test_CreateItineraryDateSelectorController_TestHideNextAndTitles_ExpectCustomCopy', async () => {
   const finished = [];
   const mountEl = createDomNode('div', 'wizard-mount');
   const titleText = 'Pick a day';
   const subtitleText = 'Visit soon';
   const selectedDate = makeNoonDate(2026, 5, 17);
   const controller = _createController({
      mountEl,
      hideNextButton: true,
      titleText,
      subtitleText,
      onFinish: (isoDate) => { finished.push(isoDate); },
   });
   controller.show();
   controller.show();
   controller.setDate(selectedDate);

   mountEl.querySelector('.itin-finish')?.click();
   await Promise.resolve();

   assert.equal(mountEl.querySelector('.itin-h1')?.textContent, titleText);
   assert.equal(mountEl.querySelector('.itin-subtitle')?.textContent, subtitleText);
   const nextOnly = [...mountEl.querySelectorAll('.itin-next')]
      .find((button) => !button.classList.contains('itin-finish'));
   assert.equal(nextOnly?.hidden, true);
   assert.deepEqual(finished, [VisitDateValidator.toISODate(selectedDate)]);
});


test('Test_CreateItineraryDateSelectorController_TestMissingMount_ExpectNoOp', () => {
   const noMount = _createController();

   assert.doesNotThrow(() => {
      noMount.show();
      noMount.hide();
   });
});


test('Test_CreateItineraryDateSelectorController_TestMissingInput_ExpectNoThrow', () => {
   const noInput = _createController({
      mountEl: createDomNode('div'),
      deps: {
         buildView: () => ({
            root: createDomNode('div'),
            inputEl: null,
            timesMountEl: null,
            nextButtonEl: createDomNode('button', 'itin-next'),
            finishButtonEl: createDomNode('button', 'itin-finish'),
            closeButtonEl: createDomNode('button', 'itin-close'),
         }),
      },
   });

   assert.doesNotThrow(() => {
      noInput.show();
   });
});


test('Test_CreateItineraryDateSelectorController_TestInvalidDate_ExpectNotSaved', () => {
   const blockedMount = createDomNode('div', 'wizard-mount');
   const saved = [];
   const blocked = _createController({
      mountEl: blockedMount,
      onSave: (isoDate) => { saved.push(isoDate); },
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


test('Test_CreateItineraryDateSelectorController_TestTimeFields_ExpectMountedAndReadable', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const arrivalTime = '10:00 AM';
   const departureTime = '4:00 PM';
   const hoursDates = [];
   const controller = _createController({
      mountEl,
      initialArrivalTime: arrivalTime,
      initialDepartureTime: departureTime,
      deps: {
         getZooHoursFn: async (isoDate) => {
            hoursDates.push(isoDate);
            return _zooHours;
         },
      },
   });

   controller.show();
   await Promise.resolve();

   assert.equal(controller.getArrivalTime(), arrivalTime);
   assert.equal(controller.getDepartureTime(), departureTime);
   assert.ok(mountEl.querySelector('.itin-date-time-fields'));
   assert.equal(hoursDates.length, 1);
});


test('Test_CreateItineraryDateSelectorController_TestTimeChange_ExpectGettersUpdated', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const nextArrivalTime = '11:00 AM';
   const nextDepartureTime = '3:00 PM';
   const timeChanges = [];
   const controller = _createController({
      mountEl,
      deps: {
         makeTimeInput: (config) => {
            timeChanges.push(config.onChange);
            return _createStubTimeInput(config);
         },
      },
   });

   controller.show();
   await Promise.resolve();
   timeChanges.at(Position.FIRST)(nextArrivalTime);
   timeChanges.at(Position.SECOND)(nextDepartureTime);

   assert.equal(controller.getArrivalTime(), nextArrivalTime);
   assert.equal(controller.getDepartureTime(), nextDepartureTime);
});


test('Test_CreateItineraryDateSelectorController_TestInvalidTimeOrder_ExpectNotSaved', async () => {
   const mountEl = createDomNode('div', 'wizard-mount');
   const savedDates = [];
   const selectedDate = makeNoonDate(2026, 5, 16);
   const controller = _createController({
      mountEl,
      initialArrivalTime: '4:00 PM',
      initialDepartureTime: '10:00 AM',
      onSave: (isoDate) => {
         savedDates.push(isoDate);
      },
   });
   controller.show();
   controller.setDate(selectedDate);
   await Promise.resolve();

   mountEl.querySelector('.itin-next')?.click();
   await Promise.resolve();

   assert.deepEqual(savedDates, []);
});
