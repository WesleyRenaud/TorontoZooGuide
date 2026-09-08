import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionHoursScheduleView } from '../../../../../scripts/consoleOperations/attractions/panels/attractionHoursScheduleView.js';
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

test('Test_CreateAttractionHoursSchedulePanel_TestDefault_ExpectPanel', () => {
   const panelEl = AttractionHoursScheduleView.createAttractionHoursSchedulePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'attractionHoursSchedulePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.attractionHoursSchedule));
   assert.ok(_findById(panelEl, 'attractionHoursScheduleAttraction'));
   assert.ok(_findById(panelEl, 'attractionHoursScheduleStartDate'));
   assert.ok(_findById(panelEl, 'attractionHoursScheduleEndDate'));
   assert.ok(_findById(panelEl, 'attractionHoursScheduleWeekdayStartTime'));
   assert.ok(_findById(panelEl, 'attractionHoursScheduleWeekdayEndTime'));
   assert.ok(_findById(panelEl, 'attractionHoursScheduleWeekendHolidayStartTime'));
   assert.ok(_findById(panelEl, 'attractionHoursScheduleWeekendHolidayEndTime'));
   assert.ok(_findById(panelEl, 'submitAttractionHoursSchedule'));
   assert.ok(_findById(panelEl, 'attractionHoursScheduleStatus'));
});
