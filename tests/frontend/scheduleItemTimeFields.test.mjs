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
