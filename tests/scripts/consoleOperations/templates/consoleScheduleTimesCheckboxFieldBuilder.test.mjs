import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateScheduleTimesCheckboxField_TestDefaults_ExpectPlaceholder', () => {
   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label: 'Schedule times',
      inputId: 'schedule-times',
      helpText: 'Pick times',
   });

   assert.match(fieldEl.textContent, /Schedule times/);
   assert.match(fieldEl.textContent, /Pick times/);
   assert.match(fieldEl.textContent, new RegExp(Strings.placeholders.selectWildEncounterFirst));

   const listEl = fieldEl.querySelector('#schedule-times')
      ?? fieldEl.children[1];
   assert.equal(listEl.id, 'schedule-times');
   assert.equal(listEl.className, 'console-operations-schedule-times-list');
});
