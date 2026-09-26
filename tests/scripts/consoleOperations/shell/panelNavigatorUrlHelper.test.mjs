import assert from 'node:assert/strict';
import test from 'node:test';

import { PanelNavigator } from '../../../../scripts/consoleOperations/shell/panelNavigator.js';
import { PanelNavigatorUrlHelper } from '../../../../scripts/consoleOperations/shell/panelNavigatorUrlHelper.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createLocation(href) {
   return { href };
}


test('Test_UpdateConsolePanelUrl_TestSet_ExpectReplaceState', () => {
   const panelId = 'animals';
   const calls = [];
   const location = _createLocation('https://example.test/console');
   const history = {
      replaceState(_state, _title, url) {
         calls.push(String(url));
      },
   };

   PanelNavigatorUrlHelper.updateConsolePanelUrl(panelId, { location, history });

   assert.match(calls.at(Position.FIRST), new RegExp(`${PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM}=${panelId}`));
});


test('Test_UpdateConsolePanelUrl_TestClear_ExpectParamRemoved', () => {
   const calls = [];
   const location = _createLocation('https://example.test/console');
   const history = {
      replaceState(_state, _title, url) {
         calls.push(String(url));
      },
   };

   PanelNavigatorUrlHelper.updateConsolePanelUrl('', { location, history });

   assert.equal(
      new URL(calls.at(Position.FIRST)).searchParams.has(PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM),
      false
   );
});


test('Test_GetPanelIdFromUrl_TestPresent_ExpectPanelId', () => {
   const panelId = 'animals';
   const location = _createLocation(`https://example.test/console?panel=${panelId}`);

   const resolved = PanelNavigatorUrlHelper.getPanelIdFromUrl(location);

   assert.equal(resolved, panelId);
});


test('Test_GetPanelIdFromUrl_TestMissing_ExpectEmpty', () => {
   const location = _createLocation('https://example.test/console');

   const resolved = PanelNavigatorUrlHelper.getPanelIdFromUrl(location);

   assert.equal(resolved, '');
});


test('Test_GetPanelIdFromUrl_TestNull_ExpectEmpty', () => {
   const location = null;

   const resolved = PanelNavigatorUrlHelper.getPanelIdFromUrl(location);

   assert.equal(resolved, '');
});


test('Test_FindMenuButtonForPanel_TestMatchingButton_ExpectButton', () => {
   const panelId = 'animals';
   const button = document.createElement('button');
   button.className = 'console-operations-menu-btn';
   button.dataset.panelTarget = panelId;
   document.body.appendChild(button);

   const found = PanelNavigatorUrlHelper.findMenuButtonForPanel(document, panelId);

   assert.equal(found, button);
});


test('Test_GetDefaultLocation_TestGlobals_ExpectValue', () => {
   const originalLocation = globalThis.location;
   const location = { href: 'https://example.test/' };

   try {
      globalThis.location = location;
      const resolved = PanelNavigatorUrlHelper.getDefaultLocation();

      assert.equal(resolved, location);
   } finally {
      globalThis.location = originalLocation;
   }
});


test('Test_GetDefaultHistory_TestGlobals_ExpectValue', () => {
   const originalHistory = globalThis.history;
   const history = { replaceState() {} };

   try {
      globalThis.history = history;
      const resolved = PanelNavigatorUrlHelper.getDefaultHistory();

      assert.equal(resolved, history);
   } finally {
      globalThis.history = originalHistory;
   }
});


test('Test_UpdateConsolePanelUrl_TestMissingLocation_ExpectNoOp', () => {
   const panelId = 'animals';

   assert.doesNotThrow(() => {
      PanelNavigatorUrlHelper.updateConsolePanelUrl(panelId, {
         location: null,
         history: { replaceState() {} },
      });
   });
});


test('Test_UpdateConsolePanelUrl_TestMissingHistory_ExpectNoOp', () => {
   const panelId = 'animals';

   assert.doesNotThrow(() => {
      PanelNavigatorUrlHelper.updateConsolePanelUrl(panelId, {
         location: _createLocation('https://example.test/'),
         history: {},
      });
   });
});
