import assert from 'node:assert/strict';
import { test } from 'node:test';

import { createAttractionHoursScheduleController } from '../../scripts/consoleOperations/attractions/controllers/attractionHoursSchedule.js';
import {
   applyScheduleTimePickerBounds,
   initAttractionHoursSchedulePickers,
} from '../../scripts/datePickers/consoleDatePickers.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';

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
   return createAttractionHoursScheduleController({
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

test('attraction hours form requires all four times', () => {
   const controller = createController({
      weekdayStartTimeEl: { value: '' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      APP_STRINGS.validation.attractionHoursTimesRequired
   );
});

test('attraction hours form requires an attraction', () => {
   const controller = createController({
      attractionEl: { value: '' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      APP_STRINGS.validation.entityRequired(
         APP_STRINGS.entityLabels.attraction
      )
   );
});

test('attraction hours form requires weekday start before end', () => {
   const controller = createController({
      weekdayStartTimeEl: { value: '4:00 PM' },
      weekdayEndTimeEl: { value: '10:00 AM' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      APP_STRINGS.validation.attractionHoursWeekdayOrder
   );
});

test('attraction hours form requires weekend start before end', () => {
   const controller = createController({
      weekendHolidayStartTimeEl: { value: '5:00 PM' },
      weekendHolidayEndTimeEl: { value: '10:00 AM' },
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      APP_STRINGS.validation.attractionHoursWeekendHolidayOrder
   );
});

test('attraction hours form accepts a complete valid payload', () => {
   const controller = createController();

   assert.equal(controller.validateForm(controller.getFormValues()), null);
});

test('attraction hours form does not client-validate zoo hours bounds', () => {
   const controller = createController({
      weekdayStartTimeEl: createField('8:00 AM'),
      weekdayEndTimeEl: createField('8:00 PM'),
      weekendHolidayStartTimeEl: createField('8:00 AM'),
      weekendHolidayEndTimeEl: createField('8:00 PM'),
   });

   assert.equal(controller.validateForm(controller.getFormValues()), null);
});

test('attraction hours form rejects end date before start date', () => {
   const controller = createController({
      startDateEl: createField('2026-06-20'),
      endDateEl: createField('2026-06-15'),
   });

   assert.equal(
      controller.validateForm(controller.getFormValues()),
      APP_STRINGS.validation.endDateBeforeStartDate
   );
});

test('attraction hours show applies zoo hours bounds to time pickers', async () => {
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

test('attraction hours refreshes picker bounds when the schedule end date changes', async () => {
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

test('attraction hours submit sends current field values to the backend', async () => {
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

test('attraction hours submit surfaces backend zoo hours errors', async () => {
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

test('applyScheduleTimePickerBounds sets and clears picker limits', () => {
   const values = {};
   const picker = {
      set(property, value) {
         values[property] = value;
      },
   };

   applyScheduleTimePickerBounds(picker, {
      openTime: '9:30 AM',
      closeTime: '6:00 PM',
   });

   assert.equal(values.minTime, '9:30 AM');
   assert.equal(values.maxTime, '6:00 PM');

   applyScheduleTimePickerBounds(picker, null);

   assert.equal(values.minTime, null);
   assert.equal(values.maxTime, null);
});

test('initAttractionHoursSchedulePickers initializes date and time pickers', () => {
   const startDateEl = createDomNode('input');
   const endDateEl = createDomNode('input');
   const weekdayStartTimeEl = createDomNode('input');
   const weekdayEndTimeEl = createDomNode('input');
   const weekendHolidayStartTimeEl = createDomNode('input');
   const weekendHolidayEndTimeEl = createDomNode('input');
   const { calls, initFlatpickrFn } = createFlatpickrSpy();

   const pickers = initAttractionHoursSchedulePickers({
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
