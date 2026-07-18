import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduleItemTimeFields } from '../../scripts/itinerary/panel/components/scheduleItemTimeFields.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

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

test('makeScheduleItemTimeFields reads input value when submitting', () => {
   const fields = makeScheduleItemTimeFields({
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

test('makeScheduleItemTimeFields disables empty fields for fixed-time schedule items', () => {
   const fields = makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = getTimeInput(fields);
   const durationInput = getDurationInput(fields);
   const timeField = getTimeField(fields);
   const durationField = getDurationField(fields);

   timeInput.value = '12:00 PM';
   durationInput.value = '30';

   fields.setFixedTimeScheduleMode({ enabled: true });

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

test('makeScheduleItemTimeFields re-enables fields after fixed-time mode is cleared', () => {
   const fields = makeScheduleItemTimeFields({
      timeLabel: 'Schedule time',
      durationLabel: 'Duration',
   });
   const timeInput = getTimeInput(fields);
   const durationInput = getDurationInput(fields);
   const timeField = getTimeField(fields);
   const durationField = getDurationField(fields);

   fields.setFixedTimeScheduleMode({ enabled: true });
   fields.reset();

   assert.equal(timeInput.disabled, false);
   assert.equal(timeInput.value, '');
   assert.equal(durationInput.disabled, false);
   assert.equal(durationInput.value, '');
   assert.equal(timeField.classList.contains('is-disabled'), false);
   assert.equal(durationField.classList.contains('is-disabled'), false);
});

test('makeScheduleItemTimeFields allows duration without a start time', () => {
   const fields = makeScheduleItemTimeFields({
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
