import assert from 'node:assert/strict';
import test from 'node:test';

import { TransportationRouteView } from '../../../../../scripts/consoleOperations/transportation/panels/transportationRouteView.js';
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

test('Test_CreateTransportationRoutePanel_TestDefault_ExpectPanel', () => {
   const panelEl = TransportationRouteView.createTransportationRoutePanel();

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'transportationRoutePanel');
   assert.equal(panelEl.className, 'console-operations-panel');
   assert.ok(panelEl.textContent.includes(Strings.panelTitles.transportationRoute));
   assert.ok(_findById(panelEl, 'transportationRouteSummer'));
   assert.ok(_findById(panelEl, 'transportationRouteWinter'));
   assert.ok(_findById(panelEl, 'transportationRouteStartDate'));
   assert.ok(_findById(panelEl, 'transportationRouteEndDate'));
   assert.ok(_findById(panelEl, 'submitTransportationRoute'));
   assert.ok(_findById(panelEl, 'transportationRouteStatus'));
});
