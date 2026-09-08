import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsolePanelShellBuilder } from '../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreatePanelShell_TestConfig_ExpectSection', () => {
   const child = document.createElement('div');
   const panelEl = ConsolePanelShellBuilder.createPanelShell({
      panelId: 'animals',
      title: 'Animals',
      bodyChildren: [child],
   });
   assert.equal(panelEl.tagName.toUpperCase(), 'SECTION');
   assert.equal(panelEl.id, 'animals');
   assert.match(panelEl.textContent, /Animals/);
});
