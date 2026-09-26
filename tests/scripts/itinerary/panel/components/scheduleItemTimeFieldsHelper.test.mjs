import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemTimeFieldsHelper } from '../../../../../scripts/itinerary/panel/components/scheduleItemTimeFieldsHelper.js';
import { ItineraryItemFormatter } from '../../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateFieldLabel_TestText_ExpectLabel', () => {
   const text = 'Start';

   const labelEl = ScheduleItemTimeFieldsHelper.createFieldLabel(text);

   assert.equal(labelEl.tagName.toUpperCase(), 'LABEL');
   assert.equal(labelEl.className, 'schedule-item-field-label');
   assert.equal(labelEl.textContent, text);
});


test('Test_ReadPickerTimeValue_TestDateString_ExpectFormattedClock', () => {
   const dateStr = '13:05';
   const inputEl = { value: '' };

   const clockTime = ScheduleItemTimeFieldsHelper.readPickerTimeValue(null, dateStr, inputEl);

   assert.equal(clockTime, ItineraryItemFormatter.formatClockTime(dateStr));
});
