import assert from 'node:assert/strict';
import { test } from 'node:test';

import { AttractionHoursSchedule } from '../../../../../scripts/consoleOperations/attractions/controllers/attractionHoursSchedule.js';
import { ConsoleDatePickers } from '../../../../../scripts/datePickers/consoleDatePickers.js';
import { Strings } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';

const WEEKDAY_BOUNDS = {
   openTime: '9:30 AM',
   closeTime: '6:00 PM',
};

const WEEKEND_BOUNDS = {
   openTime: '9:30 AM',
   closeTime: '7:00 PM',
};

function createFlatpickrSpy() {
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

function createField(value = '') {
   return {
      value,
      addEventListener() {},
   };
}

function createStatusEl() {
   return {
      textContent: '',
      classList: {
         remove() {},
         add() {},
      },
   };
}

function createController(overrides = {}) {
   return AttractionHoursSchedule.createAttractionHoursScheduleController({
      attractionEl: createField('Conservation Carousel'),
      startDateEl: createField(),
      endDateEl: createField(),
      weekdayStartTimeEl: createField('10:00 AM'),
      weekdayEndTimeEl: createField('4:00 PM'),
      weekendHolidayStartTimeEl: createField('10:00 AM'),
      weekendHolidayEndTimeEl: createField('5:00 PM'),
      statusEl: createStatusEl(),
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
   const controller = createController({
      weekdayStartTimeEl: { value: '' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      Strings.validation.attractionHoursTimesRequired
   );
});

test('Test_CreateAttractionHoursScheduleController_TestMissingAttraction_ExpectValidationError', () => {
   const controller = createController({
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
   const controller = createController({
      weekdayStartTimeEl: { value: '4:00 PM' },
      weekdayEndTimeEl: { value: '10:00 AM' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      Strings.validation.attractionHoursWeekdayOrder
   );
});

test('Test_CreateAttractionHoursScheduleController_TestWeekendOrder_ExpectValidationError', () => {
   const controller = createController({
      weekendHolidayStartTimeEl: { value: '5:00 PM' },
      weekendHolidayEndTimeEl: { value: '10:00 AM' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      Strings.validation.attractionHoursWeekendHolidayOrder
   );
});

test('Test_CreateAttractionHoursScheduleController_TestValidPayload_ExpectAccepted', () => {
   const controller = createController();

   assert.equal(controller.validateForm(controller.getFormValues()), null);
});

test('Test_CreateAttractionHoursScheduleController_TestOutOfBoundsTimes_ExpectNoClientValidation', () => {
   const controller = createController({
      weekdayStartTimeEl: createField('8:00 AM'),
      weekdayEndTimeEl: createField('8:00 PM'),
      weekendHolidayStartTimeEl: createField('8:00 AM'),
      weekendHolidayEndTimeEl: createField('8:00 PM'),
   });

   assert.equal(controller.validateForm(controller.getFormValues()), null);
});

test('Test_CreateAttractionHoursScheduleController_TestEndBeforeStart_ExpectValidationError', () => {
   const controller = createController({
      startDateEl: createField('2026-06-20'),
      endDateEl: createField('2026-06-15'),
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
   const controller = createController({
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
   const controller = createController({
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
   const statusEl = createStatusEl();
   const controller = createController({
      attractionEl: createField('Face Painting, Caricatures and Henna! - Front Gates'),
      startDateEl: createField('2026-07-29'),
      endDateEl: createField('2026-09-07'),
      weekdayStartTimeEl: createField('11:00 AM'),
      weekdayEndTimeEl: createField('4:00 PM'),
      weekendHolidayStartTimeEl: createField('11:00 AM'),
      weekendHolidayEndTimeEl: createField('5:00 PM'),
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
   const statusEl = createStatusEl();
   const controller = createController({
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

test('Test_ApplyScheduleTimePickerBounds_TestSetAndClear_ExpectLimits', () => {
   const values = {};
   const picker = {
      set(property, value) {
         values[property] = value;
      },
   };

   ConsoleDatePickers.applyScheduleTimePickerBounds(picker, {
      openTime: '9:30 AM',
      closeTime: '6:00 PM',
   });

   assert.equal(values.minTime, '9:30 AM');
   assert.equal(values.maxTime, '6:00 PM');

   ConsoleDatePickers.applyScheduleTimePickerBounds(picker, null);

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
   const { calls, initFlatpickrFn } = createFlatpickrSpy();

   const pickers = ConsoleDatePickers.initAttractionHoursSchedulePickers({
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
