import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleSchedulePresetFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleSchedulePresetFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateSchedulePresetField_TestDefaults_ExpectPresets', () => {
   const inputId = 'preset';
   const presets = [
      Strings.schedule.presetLabels.everyDay,
      Strings.schedule.presetLabels.custom,
      Strings.schedule.presetLabels.weekendsOnly,
      Strings.schedule.presetLabels.weekendsAndHolidays,
   ];

   const fieldEl = ConsoleSchedulePresetFieldBuilder.createSchedulePresetField({
      inputId,
   });

   const selectEl = fieldEl.children[Position.SECOND];
   assert.equal(selectEl.id, inputId);
   assert.equal(selectEl.children.length, presets.length);
});
