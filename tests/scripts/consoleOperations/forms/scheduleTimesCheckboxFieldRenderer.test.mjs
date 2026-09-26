import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduleTimesCheckboxFieldRenderer } from '../../../../scripts/consoleOperations/forms/scheduleTimesCheckboxFieldRenderer.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_RenderScheduleTimesListMessage_TestMessage_ExpectPlaceholder', () => {
   const message = 'No times';
   const listEl = document.createElement('div');

   ScheduleTimesCheckboxFieldRenderer.renderScheduleTimesListMessage(listEl, message);

   const placeholderEl = listEl.children[Position.FIRST];
   assert.equal(placeholderEl.className, ScheduleTimesCheckboxFieldRenderer.SCHEDULE_TIMES_PLACEHOLDER_CLASS);
   assert.equal(placeholderEl.textContent, message);
});


test('Test_RenderSingleSelectedScheduleTime_TestTime_ExpectSingleRow', () => {
   const time = '10:00';
   const listEl = document.createElement('div');

   ScheduleTimesCheckboxFieldRenderer.renderSingleSelectedScheduleTime(listEl, time);

   const rowEl = listEl.children[Position.FIRST];
   assert.equal(rowEl.className, ScheduleTimesCheckboxFieldRenderer.SCHEDULE_TIMES_SINGLE_CLASS);
   assert.equal(rowEl.dataset.scheduleTime, time);
});
