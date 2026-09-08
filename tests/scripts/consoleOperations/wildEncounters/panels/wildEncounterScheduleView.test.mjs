import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterScheduleView } from '../../../../../scripts/consoleOperations/wildEncounters/panels/wildEncounterScheduleView.js';
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

test('Test_CreateWildEncounterSchedulePanel_TestDefault_ExpectPanel', () => {
   const panelEl = WildEncounterScheduleView.createWildEncounterSchedulePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'wildEncounterSchedulePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.wildEncounterSchedule));
   assert.ok(_findById(panelEl, 'wildEncounterScheduleName'));
   assert.ok(_findById(panelEl, 'wildEncounterScheduleStartDate'));
   assert.ok(_findById(panelEl, 'wildEncounterScheduleEndDate'));
   assert.ok(_findById(panelEl, 'wildEncounterScheduleScheduleRows'));
   assert.ok(_findById(panelEl, 'wildEncounterScheduleAddScheduleRow'));
   assert.ok(_findById(panelEl, 'wildEncounterScheduleMessage'));
   assert.ok(_findById(panelEl, 'submitWildEncounterSchedule'));
   assert.ok(_findById(panelEl, 'wildEncounterScheduleStatus'));
});
