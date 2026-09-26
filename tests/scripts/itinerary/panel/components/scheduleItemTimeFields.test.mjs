import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemTimeFields } from '../../../../../scripts/itinerary/panel/components/scheduleItemTimeFields.js';
import { ConsoleDateFactory } from '../../../../../scripts/datePickers/consoleDateFactory.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _getTimeInput(fields) {
   const timeField = fields.fields[Position.FIRST];

   return timeField.children.find((child) => (
      child.className?.includes('schedule-item-time-input')
   ));
}

function _getDurationInput(fields) {
   const durationField = fields.fields[Position.SECOND];

   return durationField.children.find((child) => (
      child.className?.includes('schedule-item-duration-input')
   ));
}

function _getTimeField(fields) {
   return fields.fields[Position.FIRST];
}

function _getDurationField(fields) {
   return fields.fields[Position.SECOND];
}

installDomTestHooks({
   after: () => {
      delete globalThis.fetch;
   },
});


test('Test_MakeScheduleItemTimeFields_TestSubmit_ExpectInputValue', () => {
   const startTime = '12:00 PM';

   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = _getTimeInput(fields);
   timeInput.value = startTime;
   const options = fields.getScheduleTimeOptions();

   assert.deepEqual(options, {
      startTime,
      durationMinutes: null,
   });
});


test('Test_MakeScheduleItemTimeFields_TestFixedTime_ExpectDisabledEmpty', () => {
   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = _getTimeInput(fields);
   const durationInput = _getDurationInput(fields);
   const timeField = _getTimeField(fields);
   const durationField = _getDurationField(fields);
   timeInput.value = '12:00 PM';
   durationInput.value = '30';

   fields.setFixedTimeScheduleMode({ lockTimes: true });
   const options = fields.getScheduleTimeOptions();

   assert.equal(timeInput.disabled, true);
   assert.equal(timeInput.value, '');
   assert.equal(durationInput.disabled, true);
   assert.equal(durationInput.value, '');
   assert.equal(timeField.classList.contains('is-disabled'), true);
   assert.equal(durationField.classList.contains('is-disabled'), true);
   assert.deepEqual(options, {
      startTime: '',
      durationMinutes: null,
   });
});


test('Test_MakeScheduleItemTimeFields_TestClearFixedTime_ExpectEnabled', () => {
   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = _getTimeInput(fields);
   const durationInput = _getDurationInput(fields);
   const timeField = _getTimeField(fields);
   const durationField = _getDurationField(fields);

   fields.setFixedTimeScheduleMode({ lockTimes: true });
   fields.reset();

   assert.equal(timeInput.disabled, false);
   assert.equal(timeInput.value, '');
   assert.equal(durationInput.disabled, false);
   assert.equal(durationInput.value, '');
   assert.equal(timeField.classList.contains('is-disabled'), false);
   assert.equal(durationField.classList.contains('is-disabled'), false);
});


test('Test_MakeScheduleItemTimeFields_TestDurationOnly_ExpectAllowed', () => {
   const durationValue = '25';

   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const durationInput = _getDurationInput(fields);
   durationInput.value = durationValue;
   const options = fields.getScheduleTimeOptions();

   assert.equal(durationInput.disabled, false);
   assert.deepEqual(options, {
      startTime: '',
      durationMinutes: Number(durationValue),
   });
});


test('Test_MakeScheduleItemTimeFields_TestFixedDuration_ExpectEditableStart', () => {
   const startTime = '10:00 AM';
   const durationMinutes = 75;

   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = _getTimeInput(fields);
   const durationInput = _getDurationInput(fields);
   const durationField = _getDurationField(fields);
   timeInput.value = startTime;
   durationInput.value = '30';

   fields.setFixedDurationScheduleMode({
      lockDuration: true,
      durationMinutes,
   });
   const options = fields.getScheduleTimeOptions();

   assert.equal(timeInput.disabled, false);
   assert.equal(durationInput.disabled, true);
   assert.equal(durationInput.value, String(durationMinutes));
   assert.equal(durationField.classList.contains('is-disabled'), true);
   assert.deepEqual(options, {
      startTime,
      durationMinutes: null,
   });
});


test('Test_MakeScheduleItemTimeFields_TestPickerChange_ExpectSynced', () => {
   const originalInit = ConsoleDateFactory.initTimePicker;
   const changedTime = '2:30 PM';
   let capturedOptions = null;
   const calendarContainer = { classList: { add() {} } };
   const instance = {
      calendarContainer,
      input: { value: '1:15 PM' },
      clear() {},
      set() {},
   };

   ConsoleDateFactory.initTimePicker = (_inputEl, options) => {
      capturedOptions = options;
      options.onReady([], '', instance);
      return instance;
   };

   try {
      const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
         timeLabel: 'Schedule time',
         durationLabel: 'Duration',
      });
      capturedOptions.onChange([], changedTime, instance);
      const options = fields.getScheduleTimeOptions();

      assert.deepEqual(options, {
         startTime: changedTime,
         durationMinutes: null,
      });
   } finally {
      ConsoleDateFactory.initTimePicker = originalInit;
   }
});


test('Test_MakeScheduleItemTimeFields_TestPickerChangeWhileLocked_ExpectEmpty', () => {
   const originalInit = ConsoleDateFactory.initTimePicker;
   let capturedOptions = null;
   const calendarContainer = { classList: { add() {} } };
   const instance = {
      calendarContainer,
      input: { value: '1:15 PM' },
      clear() {},
      set() {},
   };

   ConsoleDateFactory.initTimePicker = (_inputEl, options) => {
      capturedOptions = options;
      options.onReady([], '', instance);
      return instance;
   };

   try {
      const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
         timeLabel: 'Schedule time',
         durationLabel: 'Duration',
      });
      fields.setFixedTimeScheduleMode({ lockTimes: true });
      capturedOptions.onChange([], '3:00 PM', instance);
      const options = fields.getScheduleTimeOptions();

      assert.deepEqual(options, {
         startTime: '',
         durationMinutes: null,
      });
   } finally {
      ConsoleDateFactory.initTimePicker = originalInit;
   }
});
