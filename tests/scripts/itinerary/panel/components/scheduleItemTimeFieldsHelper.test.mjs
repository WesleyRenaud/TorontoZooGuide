import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleItemTimeFieldsHelper } from '../../../../../scripts/itinerary/panel/components/scheduleItemTimeFieldsHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateFieldLabel_TestText_ExpectLabel', () => {
   const labelEl = ScheduleItemTimeFieldsHelper.createFieldLabel('Start');
   assert.equal(labelEl.tagName.toUpperCase(), 'LABEL');
   assert.equal(labelEl.className, 'schedule-item-field-label');
   assert.equal(labelEl.textContent, 'Start');
});

test('Test_ReadPickerTimeValue_TestSources_ExpectFormattedClock', () => {
   assert.equal(
      ScheduleItemTimeFieldsHelper.readPickerTimeValue(null, '13:05', { value: '' }),
      '1:05 PM'
   );
});
