import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationStationOpenView } from '../../../../../scripts/consoleOperations/transportation/panels/transportationStationOpenView.js';
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

test('Test_CreateTransportationStationOpenPanel_TestDefault_ExpectPanel', () => {
   const panelEl = TransportationStationOpenView.createTransportationStationOpenPanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'transportationStationOpenPanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.transportationStationOpen));
   assert.ok(_findById(panelEl, 'transportationStationOpenTransportationStation'));
   assert.ok(_findById(panelEl, 'submitTransportationStationOpen'));
   assert.ok(_findById(panelEl, 'transportationStationOpenStatus'));
});
