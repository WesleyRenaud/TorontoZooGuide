import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkScheduleView } from '../../../../../scripts/consoleOperations/guardiansTalks/panels/guardiansTalkScheduleView.js';
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

test('Test_CreateGuardiansTalkSchedulePanel_TestDefault_ExpectPanel', () => {
   const panelEl = GuardiansTalkScheduleView.createGuardiansTalkSchedulePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'guardiansTalkSchedulePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.guardiansTalkSchedule));
   assert.ok(_findById(panelEl, 'guardiansTalkScheduleLocation'));
   assert.ok(_findById(panelEl, 'guardiansTalkScheduleTalkName'));
   assert.ok(_findById(panelEl, 'guardiansTalkScheduleStartDate'));
   assert.ok(_findById(panelEl, 'guardiansTalkScheduleEndDate'));
   assert.ok(_findById(panelEl, 'guardiansTalkScheduleScheduleRows'));
   assert.ok(_findById(panelEl, 'guardiansTalkScheduleAddScheduleRow'));
   assert.ok(_findById(panelEl, 'guardiansTalkScheduleMessage'));
   assert.ok(_findById(panelEl, 'submitGuardiansTalkSchedule'));
   assert.ok(_findById(panelEl, 'guardiansTalkScheduleStatus'));
});
