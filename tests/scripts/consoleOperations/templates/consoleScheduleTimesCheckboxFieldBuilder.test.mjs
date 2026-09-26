import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleScheduleTimesCheckboxFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleScheduleTimesCheckboxFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateScheduleTimesCheckboxField_TestDefaults_ExpectPlaceholder', () => {
   const label = 'Schedule times';
   const inputId = 'schedule-times';
   const helpText = 'Pick times';

   const fieldEl = ConsoleScheduleTimesCheckboxFieldBuilder.createScheduleTimesCheckboxField({
      label,
      inputId,
      helpText,
   });

   const listEl = fieldEl.querySelector(`#${inputId}`) ?? fieldEl.children[Position.SECOND];
   assert.match(fieldEl.textContent, new RegExp(label));
   assert.match(fieldEl.textContent, new RegExp(helpText));
   assert.match(fieldEl.textContent, new RegExp(Strings.placeholders.selectWildEncounterFirst));
   assert.equal(listEl.id, inputId);
   assert.equal(listEl.className, 'console-operations-schedule-times-list');
});
