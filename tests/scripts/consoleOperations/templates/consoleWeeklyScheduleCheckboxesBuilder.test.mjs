import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleWeeklyScheduleCheckboxesBuilder } from '../../../../scripts/consoleOperations/templates/consoleWeeklyScheduleCheckboxesBuilder.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateWeeklyScheduleCheckboxes_TestDaysAndHolidays_ExpectGrid', () => {
   const mondayId = 'mon';
   const dayIds = {
      monday: mondayId,
      tuesday: 'tue',
      wednesday: 'wed',
      thursday: 'thu',
      friday: 'fri',
      saturday: 'sat',
      sunday: 'sun',
      holidays: 'hol',
   };

   const fieldEl = ConsoleWeeklyScheduleCheckboxesBuilder.createWeeklyScheduleCheckboxes({
      dayIds,
   });

   assert.match(fieldEl.textContent, new RegExp(Strings.labels.openOnTheseDays));
   assert.match(fieldEl.textContent, new RegExp(Strings.schedule.dayLabels.monday));
   assert.match(fieldEl.textContent, new RegExp(Strings.schedule.dayLabels.holidays));
   assert.ok(
      fieldEl.querySelector(`#${mondayId}`)
      || fieldEl.textContent.includes(Strings.schedule.dayLabels.monday)
   );
});


test('Test_CreateWeeklyScheduleCheckboxes_TestWithoutHolidays_ExpectWeekdaysOnly', () => {
   const dayIds = {
      monday: 'mon',
      tuesday: 'tue',
      wednesday: 'wed',
      thursday: 'thu',
      friday: 'fri',
      saturday: 'sat',
      sunday: 'sun',
      holidays: 'hol',
   };

   const fieldEl = ConsoleWeeklyScheduleCheckboxesBuilder.createWeeklyScheduleCheckboxes({
      includeHolidays: false,
      dayIds,
   });

   assert.equal(fieldEl.textContent.includes(Strings.schedule.dayLabels.holidays), false);
});
