import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleSchedulePresetFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSchedulePresetFieldBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateSchedulePresetField_TestDefaults_ExpectPresets', () => {
   const fieldEl = ConsoleSchedulePresetFieldBuilder.createSchedulePresetField({
      inputId: 'preset',
   });
   const selectEl = fieldEl.children[1];
   assert.equal(selectEl.id, 'preset');
   assert.equal(selectEl.children.length, 4);
});
