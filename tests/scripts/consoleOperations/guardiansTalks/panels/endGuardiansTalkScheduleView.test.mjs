import assert from 'node:assert/strict';
import test from 'node:test';

import { EndGuardiansTalkScheduleView } from '../../../../../scripts/consoleOperations/guardiansTalks/panels/endGuardiansTalkScheduleView.js';
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

test('Test_CreateEndGuardiansTalkSchedulePanel_TestDefault_ExpectPanel', () => {
   const panelEl = EndGuardiansTalkScheduleView.createEndGuardiansTalkSchedulePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'endGuardiansTalkSchedulePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.endGuardiansTalkSchedule));
   assert.ok(_findById(panelEl, 'endGuardiansTalkScheduleLocation'));
   assert.ok(_findById(panelEl, 'endGuardiansTalkScheduleTalkName'));
   assert.ok(_findById(panelEl, 'endGuardiansTalkScheduleTimes'));
   assert.ok(_findById(panelEl, 'endGuardiansTalkScheduleEndDate'));
   assert.ok(_findById(panelEl, 'submitEndGuardiansTalkSchedule'));
   assert.ok(_findById(panelEl, 'endGuardiansTalkScheduleStatus'));
});
