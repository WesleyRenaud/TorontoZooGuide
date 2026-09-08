import assert from 'node:assert/strict';
import { test } from 'node:test';

import { AttractionHoursController } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionHoursController.js';
import { OpeningScheduleChecker } from '../../../../../scripts/consoleOperations/forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapFragment } from '../../../../../scripts/consoleOperations/forms/openingScheduleOverlapFragment.js';
import { ConsoleDateFactory } from '../../../../../scripts/datePickers/consoleDateFactory.js';
import { Strings } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

const WEEKDAY_BOUNDS = {
   openTime: '9:30 AM',
   closeTime: '6:00 PM',
};

const WEEKEND_BOUNDS = {
   openTime: '9:30 AM',
   closeTime: '7:00 PM',
};

function _createFlatpickrSpy() {
   const calls = [];

   return {
      calls,
      initFlatpickrFn: (inputEl, options) => {
         calls.push({ inputEl, options });

         return {
            close() {},
            set(property, value) {
               this[property] = value;
            },
            setDate() {
               inputEl.value = '';
            },
         };
      },
   };
}

function _createField(value = '') {
   return {
      value,
      addEventListener() {},
   };
}

function _createStatusEl() {
   return {
      textContent: '',
      classList: {
         remove() {},
         add() {},
      },
   };
}

function _createController(overrides = {}) {
   return AttractionHoursController.createAttractionHoursScheduleController({
      attractionEl: _createField('Conservation Carousel'),
      startDateEl: _createField(),
      endDateEl: _createField(),
      weekdayStartTimeEl: _createField('10:00 AM'),
      weekdayEndTimeEl: _createField('4:00 PM'),
      weekendHolidayStartTimeEl: _createField('10:00 AM'),
      weekendHolidayEndTimeEl: _createField('5:00 PM'),
      statusEl: _createStatusEl(),
      loadAttractions: async () => [ 'Conservation Carousel' ],
      loadTimeBounds: async () => ( {
         success: true,
         weekday: WEEKDAY_BOUNDS,
         weekendHoliday: WEEKEND_BOUNDS,
      } ),
      ...overrides,
   });
}

test('Test_CreateAttractionHoursScheduleController_TestMissingTimes_ExpectValidationError', () => {
   const controller = _createController({
      weekdayStartTimeEl: { value: '' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      Strings.validation.attractionHoursTimesRequired
   );
});

test('Test_CreateAttractionHoursScheduleController_TestMissingAttraction_ExpectValidationError', () => {
   const controller = _createController({
      attractionEl: { value: '' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      Strings.validation.entityRequired(
         Strings.entityLabels.attraction
      )
   );
});

test('Test_CreateAttractionHoursScheduleController_TestWeekdayOrder_ExpectValidationError', () => {
   const controller = _createController({
      weekdayStartTimeEl: { value: '4:00 PM' },
      weekdayEndTimeEl: { value: '10:00 AM' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      Strings.validation.attractionHoursWeekdayOrder
   );
});

test('Test_CreateAttractionHoursScheduleController_TestWeekendOrder_ExpectValidationError', () => {
   const controller = _createController({
      weekendHolidayStartTimeEl: { value: '5:00 PM' },
      weekendHolidayEndTimeEl: { value: '10:00 AM' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      Strings.validation.attractionHoursWeekendHolidayOrder
   );
});

test('Test_CreateAttractionHoursScheduleController_TestValidPayload_ExpectAccepted', () => {
   const controller = _createController();

   assert.equal(controller.validateForm(controller.getFormValues()), null);
});

test('Test_CreateAttractionHoursScheduleController_TestOutOfBoundsTimes_ExpectNoClientValidation', () => {
   const controller = _createController({
      weekdayStartTimeEl: _createField('8:00 AM'),
      weekdayEndTimeEl: _createField('8:00 PM'),
      weekendHolidayStartTimeEl: _createField('8:00 AM'),
      weekendHolidayEndTimeEl: _createField('8:00 PM'),
   });

   assert.equal(controller.validateForm(controller.getFormValues()), null);
});

test('Test_CreateAttractionHoursScheduleController_TestEndBeforeStart_ExpectValidationError', () => {
   const controller = _createController({
      startDateEl: _createField('2026-06-20'),
      endDateEl: _createField('2026-06-15'),
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      Strings.validation.endDateBeforeStartDate
   );
});

test('Test_CreateAttractionHoursScheduleController_TestShow_ExpectPickerBounds', async () => {
   const applied = [];
   const weekdayStartTimePicker = {
      set(property, value) {
         applied.push({ property, value });
      },
   };
   const controller = _createController({
      weekdayStartTimePicker,
      weekdayEndTimePicker: weekdayStartTimePicker,
      weekendHolidayStartTimePicker: weekdayStartTimePicker,
      weekendHolidayEndTimePicker: weekdayStartTimePicker,
      loadTimeBounds: async () => ( {
         success: true,
         weekday: WEEKDAY_BOUNDS,
         weekendHoliday: WEEKEND_BOUNDS,
      } ),
   });

   await controller.show();

   assert.deepEqual(
      applied.filter((entry) => entry.property === 'minTime'),
      [
         { property: 'minTime', value: '9:30 AM' },
         { property: 'minTime', value: '9:30 AM' },
         { property: 'minTime', value: '9:30 AM' },
         { property: 'minTime', value: '9:30 AM' },
      ]
   );
});

test('Test_CreateAttractionHoursScheduleController_TestEndDateChange_ExpectBoundsRefresh', async () => {
   const endDateEl = { value: '', listeners: {} };
   endDateEl.addEventListener = (eventName, handler) => {
      endDateEl.listeners[eventName] = handler;
   };

   const boundCloses = [];
   const controller = _createController({
      endDateEl,
      loadTimeBounds: async ({ scheduleEndDate } = {}) => ( {
         success: true,
         weekday: {
            openTime: '9:30 AM',
            closeTime: scheduleEndDate === '2026-10-25'
               ? '4:30 PM'
               : '6:00 PM',
         },
         weekendHoliday: WEEKEND_BOUNDS,
      } ),
      weekdayEndTimePicker: {
         set(property, value) {
            if (property === 'maxTime') {
               boundCloses.push(value);
            }
         },
      },
   });

   await controller.show();
   endDateEl.value = '2026-10-25';
   await endDateEl.listeners.change?.();

   assert.deepEqual(boundCloses, [ '6:00 PM', '4:30 PM' ]);
});

test('Test_CreateAttractionHoursScheduleController_TestSubmit_ExpectBackendPayload', async () => {
   const savedPayloads = [];
   const statusEl = _createStatusEl();
   const controller = _createController({
      attractionEl: _createField('Face Painting, Caricatures and Henna! - Front Gates'),
      startDateEl: _createField('2026-07-29'),
      endDateEl: _createField('2026-09-07'),
      weekdayStartTimeEl: _createField('11:00 AM'),
      weekdayEndTimeEl: _createField('4:00 PM'),
      weekendHolidayStartTimeEl: _createField('11:00 AM'),
      weekendHolidayEndTimeEl: _createField('5:00 PM'),
      statusEl,
      saveSchedule: async (payload) => {
         savedPayloads.push(payload);
         return {
            success: true,
            attraction: payload.attraction,
         };
      },
   });

   await controller.submit();

   assert.deepEqual(savedPayloads, [
      {
         attraction: 'Face Painting, Caricatures and Henna! - Front Gates',
         scheduleStartDate: '2026-07-29',
         scheduleEndDate: '2026-09-07',
         weekdayStartTime: '11:00 AM',
         weekdayEndTime: '4:00 PM',
         weekendHolidayStartTime: '11:00 AM',
         weekendHolidayEndTime: '5:00 PM',
      },
   ]);
});

test('Test_CreateAttractionHoursScheduleController_TestSubmit_ExpectBackendError', async () => {
   const statusEl = _createStatusEl();
   const controller = _createController({
      statusEl,
      saveSchedule: async () => ( {
         success: false,
         apiErrorType: 'invalidAttractionHours',
      } ),
   });

   await controller.submit();

   assert.equal(
      statusEl.textContent,
      'Attraction hours must fall within regular zoo hours for the selected date range.'
   );
});

test('Test_CreateAttractionHoursScheduleController_TestBoundsFailureHideOverlapAndValidation_ExpectBranches', async () => {
   const statusEl = _createStatusEl();

   const boundsFail = _createController({
      statusEl,
      loadTimeBounds: async () => ({
         success: false,
         apiErrorType: 'couldNotResolveAttractionHoursTimeBounds',
      }),
   });
   assert.equal(await boundsFail.refreshTimeBounds(), false);
   assert.ok(statusEl.textContent);

   const showFail = _createController({
      statusEl,
      loadAttractions: async () => {
         throw new Error('load fail');
      },
      activatePanel: () => {},
   });
   await showFail.show();
   assert.ok(statusEl.textContent);

   const hideController = _createController({
      statusEl,
      panelEl: createDomNode('div'),
   });
   hideController.hide();

   const validationSubmit = _createController({
      statusEl,
      attractionEl: _createField(''),
   });
   await validationSubmit.submit();
   assert.ok(statusEl.textContent);

   const originalShow = OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog;
   const originalHasOverlap = OpeningScheduleChecker.resultHasOpeningScheduleOverlap;

   try {
      OpeningScheduleChecker.resultHasOpeningScheduleOverlap = () => true;
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE
      );

      const overlapReplace = _createController({
         statusEl,
         saveSchedule: async () => ({ success: false }),
         replaceScheduleOverlaps: async () => ({
            success: true,
            attraction: 'Conservation Carousel',
         }),
      });
      await overlapReplace.submit();

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => (
         OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM
      );
      const overlapTrimFail = _createController({
         statusEl,
         saveSchedule: async () => ({ success: false }),
         trimScheduleOverlaps: async () => ({
            success: false,
            apiErrorType: 'invalidAttractionHours',
         }),
      });
      await overlapTrimFail.submit();
      assert.ok(statusEl.textContent);

      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = async () => null;
      const overlapCancel = _createController({
         statusEl,
         saveSchedule: async () => ({ success: false }),
      });
      await overlapCancel.submit();

      OpeningScheduleChecker.resultHasOpeningScheduleOverlap = () => false;
      const submitThrow = _createController({
         statusEl,
         saveSchedule: async () => {
            throw new Error('network');
         },
      });
      await submitThrow.submit();
      assert.equal(statusEl.textContent, Strings.common.requestFailed);
   } finally {
      OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog = originalShow;
      OpeningScheduleChecker.resultHasOpeningScheduleOverlap = originalHasOverlap;
   }

   const showButtonEl = { listeners: {}, addEventListener(name, handler) { this.listeners[name] = handler; } };
   const cancelButtonEl = { listeners: {}, addEventListener(name, handler) { this.listeners[name] = handler; } };
   const submitButtonEl = { listeners: {}, addEventListener(name, handler) { this.listeners[name] = handler; } };
   const startDateEl = { value: '', listeners: {}, addEventListener(name, handler) { this.listeners[name] = handler; } };
   _createController({
      showButtonEl,
      cancelButtonEl,
      submitButtonEl,
      startDateEl,
      panelEl: createDomNode('div'),
      saveSchedule: async () => ({ success: true, attraction: 'Conservation Carousel' }),
   });
   showButtonEl.listeners.click?.();
   cancelButtonEl.listeners.click?.();
   submitButtonEl.listeners.click?.();
   await startDateEl.listeners.change?.();
});

test('Test_ApplyScheduleTimePickerBounds_TestSetAndClear_ExpectLimits', () => {
   const values = {};
   const picker = {
      set(property, value) {
         values[property] = value;
      },
   };

   ConsoleDateFactory.applyScheduleTimePickerBounds(picker, {
      openTime: '9:30 AM',
      closeTime: '6:00 PM',
   });

   assert.equal(values.minTime, '9:30 AM');
   assert.equal(values.maxTime, '6:00 PM');

   ConsoleDateFactory.applyScheduleTimePickerBounds(picker, null);

   assert.equal(values.minTime, null);
   assert.equal(values.maxTime, null);
});

test('Test_InitAttractionHoursSchedulePickers_TestInit_ExpectPickers', () => {
   const startDateEl = createDomNode('input');
   const endDateEl = createDomNode('input');
   const weekdayStartTimeEl = createDomNode('input');
   const weekdayEndTimeEl = createDomNode('input');
   const weekendHolidayStartTimeEl = createDomNode('input');
   const weekendHolidayEndTimeEl = createDomNode('input');
   const { calls, initFlatpickrFn } = _createFlatpickrSpy();

   const pickers = ConsoleDateFactory.initAttractionHoursSchedulePickers({
      startDateEl,
      endDateEl,
      weekdayStartTimeEl,
      weekdayEndTimeEl,
      weekendHolidayStartTimeEl,
      weekendHolidayEndTimeEl,
   }, { initFlatpickrFn });

   assert.equal(calls.length, 6);
   assert.ok(pickers.weekdayStartTimePicker);
   assert.ok(pickers.weekendHolidayEndTimePicker);
   assert.equal(calls[2].options.enableTime, true);
});
