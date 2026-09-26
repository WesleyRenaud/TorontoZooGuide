import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreatePanelShell_TestConfig_ExpectSection', () => {
   const panelId = 'animals';
   const title = 'Animals';
   const child = document.createElement('div');

   const panelEl = ConsolePanelShellBuilder.createPanelShell({
      panelId,
      title,
      bodyChildren: [child],
   });

   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, panelId);
   assert.match(panelEl.textContent, new RegExp(title));
});
