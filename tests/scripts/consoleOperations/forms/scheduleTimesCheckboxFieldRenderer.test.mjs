import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleTimesCheckboxFieldRenderer } from '../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxFieldRenderer.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_RenderScheduleTimesListMessage_TestMessage_ExpectPlaceholder', () => {
   const listEl = document.createElement('div');
   ScheduleTimesCheckboxFieldRenderer.renderScheduleTimesListMessage(listEl, 'No times');
   assert.equal(listEl.children[0].className, ScheduleTimesCheckboxFieldRenderer.SCHEDULE_TIMES_PLACEHOLDER_CLASS);
   assert.equal(listEl.children[0].textContent, 'No times');
});

test('Test_RenderSingleSelectedScheduleTime_TestTime_ExpectSingleRow', () => {
   const listEl = document.createElement('div');
   ScheduleTimesCheckboxFieldRenderer.renderSingleSelectedScheduleTime(listEl, '10:00');
   assert.equal(listEl.children[0].className, ScheduleTimesCheckboxFieldRenderer.SCHEDULE_TIMES_SINGLE_CLASS);
   assert.equal(listEl.children[0].dataset.scheduleTime, '10:00');
});
