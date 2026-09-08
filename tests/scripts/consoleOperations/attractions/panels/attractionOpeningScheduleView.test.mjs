import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionOpeningScheduleView } from '../../../../../scripts/consoleOperations/attractions/panels/attractionOpeningScheduleView.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _findById(node, id) {
   if (node?.id === id) {
      return node;
   }

   for (const child of node?.children ?? []) {
      const found = _findById(child, id);
      if (found) {
         return found;
      }
   }

   return null;
}

installDomTestHooks();

test('Test_CreateAttractionOpeningSchedulePanel_TestDefault_ExpectPanel', () => {
   const panelEl = AttractionOpeningScheduleView.createAttractionOpeningSchedulePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'attractionOpeningSchedulePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.attractionOpeningSchedule));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleAttraction'));
   assert.ok(_findById(panelEl, 'attractionOpeningSchedulePreset'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleStartDate'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleEndDate'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleMonday'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleTuesday'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleWednesday'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleThursday'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleFriday'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleSaturday'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleSunday'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleHolidaysOnly'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleMessage'));
   assert.ok(_findById(panelEl, 'submitAttractionOpeningSchedule'));
   assert.ok(_findById(panelEl, 'attractionOpeningScheduleStatus'));
});
