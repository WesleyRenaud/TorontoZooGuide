import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { makeScheduleItemTimeFields } from '../../scripts/itinerary/panel/components/scheduleItemTimeFields.js';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

function getTimeInput(fields) {
   const timeField = fields.fields[0];

   return timeField.children.find((child) => (
      child.className?.includes('schedule-item-time-input')
   ));
}

beforeEach(() => {
   installTestWindow();
   installDocument();
});

afterEach(() => {
   teardownDocument();
   delete globalThis.fetch;
   delete globalThis.window;
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
