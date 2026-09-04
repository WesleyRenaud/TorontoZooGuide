import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemTimeFields } from '../../../../../scripts/itinerary/panel/components/scheduleItemTimeFields.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function getTimeInput(fields) {
   const timeField = fields.fields[0];

   return timeField.children.find((child) => (
      child.className?.includes('schedule-item-time-input')
   ));
}

function getDurationInput(fields) {
   const durationField = fields.fields[1];

   return durationField.children.find((child) => (
      child.className?.includes('schedule-item-duration-input')
   ));
}

function getTimeField(fields) {
   return fields.fields[0];
}

function getDurationField(fields) {
   return fields.fields[1];
}

installDomTestHooks({
   after: () => {
      delete globalThis.fetch;
   },
});

test('Test_MakeScheduleItemTimeFields_TestSubmit_ExpectInputValue', () => {
   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = getTimeInput(fields);

   timeInput.value = '12:00 PM';

   assert.deepEqual(fields.getScheduleTimeOptions(), {
      startTime: '12:00 PM',
      durationMinutes: null,
   });
});

test('Test_MakeScheduleItemTimeFields_TestFixedTime_ExpectDisabledEmpty', () => {
   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = getTimeInput(fields);
   const durationInput = getDurationInput(fields);
   const timeField = getTimeField(fields);
   const durationField = getDurationField(fields);

   timeInput.value = '12:00 PM';
   durationInput.value = '30';

   fields.setFixedTimeScheduleMode({ lockTimes: true });

   assert.equal(timeInput.disabled, true);
   assert.equal(timeInput.value, '');
   assert.equal(durationInput.disabled, true);
   assert.equal(durationInput.value, '');
   assert.equal(timeField.classList.contains('is-disabled'), true);
   assert.equal(durationField.classList.contains('is-disabled'), true);
   assert.deepEqual(fields.getScheduleTimeOptions(), {
      startTime: '',
      durationMinutes: null,
   });
});

test('Test_MakeScheduleItemTimeFields_TestClearFixedTime_ExpectEnabled', () => {
   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = getTimeInput(fields);
   const durationInput = getDurationInput(fields);
   const timeField = getTimeField(fields);
   const durationField = getDurationField(fields);

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
   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const durationInput = getDurationInput(fields);

   durationInput.value = '25';

   assert.equal(durationInput.disabled, false);
   assert.deepEqual(fields.getScheduleTimeOptions(), {
      startTime: '',
      durationMinutes: 25,
   });
});

test('Test_MakeScheduleItemTimeFields_TestFixedDuration_ExpectEditableStart', () => {
   const fields = ScheduleItemTimeFields.makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = getTimeInput(fields);
   const durationInput = getDurationInput(fields);
   const durationField = getDurationField(fields);

   timeInput.value = '10:00 AM';
   durationInput.value = '30';

   fields.setFixedDurationScheduleMode({
      lockDuration: true,
      durationMinutes: 75,
   });

   assert.equal(timeInput.disabled, false);
   assert.equal(durationInput.disabled, true);
   assert.equal(durationInput.value, '75');
   assert.equal(durationField.classList.contains('is-disabled'), true);
   assert.deepEqual(fields.getScheduleTimeOptions(), {
      startTime: '10:00 AM',
      durationMinutes: null,
   });
});
