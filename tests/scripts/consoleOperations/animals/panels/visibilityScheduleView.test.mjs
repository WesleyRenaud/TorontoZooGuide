import assert from 'node:assert/strict';
import test from 'node:test';

import { VisibilityScheduleView } from '../../../../../scripts/consoleOperations/animals/panels/visibilityScheduleView.js';
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

test('Test_CreateVisibilitySchedulePanel_TestDefault_ExpectPanel', () => {
   const panelEl = VisibilityScheduleView.createVisibilitySchedulePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'visibilitySchedulePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.visibilitySchedule));
   assert.ok(_findById(panelEl, 'visibilityScheduleExhibit'));
   assert.ok(_findById(panelEl, 'visibilityScheduleSpecies'));
   assert.ok(_findById(panelEl, 'visibilityScheduleSpeciesResults'));
   assert.ok(_findById(panelEl, 'visibilityScheduleStartDate'));
   assert.ok(_findById(panelEl, 'visibilityScheduleEndDate'));
   assert.ok(_findById(panelEl, 'visibilityScheduleDailyStartTime'));
   assert.ok(_findById(panelEl, 'visibilityScheduleDailyEndTime'));
   assert.ok(_findById(panelEl, 'visibilityScheduleMessage'));
   assert.ok(_findById(panelEl, 'submitVisibilitySchedule'));
   assert.ok(_findById(panelEl, 'visibilityScheduleStatus'));
});
