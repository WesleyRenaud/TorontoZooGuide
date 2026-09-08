import assert from 'node:assert/strict';
import test from 'node:test';

import { CreateEventView } from '../../../../../scripts/consoleOperations/events/panels/createEventView.js';
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

test('Test_CreateCreateEventPanel_TestDefault_ExpectPanel', () => {
   const panelEl = CreateEventView.createCreateEventPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'createEventPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.createEvent));
   assert.ok(_findById(panelEl, 'createEventName'));
   assert.ok(_findById(panelEl, 'createEventLocation'));
   assert.ok(_findById(panelEl, 'createEventDescription'));
   assert.ok(_findById(panelEl, 'createEventLink'));
   assert.ok(_findById(panelEl, 'createEventStartDate'));
   assert.ok(_findById(panelEl, 'createEventEndDate'));
   assert.ok(_findById(panelEl, 'submitCreateEvent'));
   assert.ok(_findById(panelEl, 'createEventStatus'));
});
