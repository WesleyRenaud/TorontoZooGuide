import assert from 'node:assert/strict';
import test from 'node:test';

import { PanelNavigator } from '../../../../scripts/consoleOperations/shell/panelNavigator.js';
import { PanelNavigatorUrlHelper } from '../../../../scripts/consoleOperations/shell/panelNavigatorUrlHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createLocation(href) {
   return { href };
}

test('Test_UpdateConsolePanelUrl_TestSetAndClear_ExpectReplaceState', () => {
   const calls = [];
   const location = _createLocation('https://example.test/console');
   const history = {
      replaceState(_state, _title, url) {
         calls.push(String(url));
      },
   };

   PanelNavigatorUrlHelper.updateConsolePanelUrl('animals', { location, history });
   PanelNavigatorUrlHelper.updateConsolePanelUrl('', { location, history });

   assert.match(calls[0], /panel=animals/);
   assert.equal(new URL(calls[1]).searchParams.has(PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM), false);
});

test('Test_GetPanelIdFromUrl_TestPresentAndMissing_ExpectPanelId', () => {
   assert.equal(
      PanelNavigatorUrlHelper.getPanelIdFromUrl(
         _createLocation('https://example.test/console?panel=animals')
      ),
      'animals'
   );
   assert.equal(
      PanelNavigatorUrlHelper.getPanelIdFromUrl(_createLocation('https://example.test/console')),
      ''
   );
   assert.equal(PanelNavigatorUrlHelper.getPanelIdFromUrl(null), '');
});

test('Test_FindMenuButtonForPanel_TestMatchingButton_ExpectButton', () => {
   const button = document.createElement('button');
   button.className = 'console-operations-menu-btn';
   button.dataset.panelTarget = 'animals';
   document.body.appendChild(button);

   assert.equal(
      PanelNavigatorUrlHelper.findMenuButtonForPanel(document, 'animals'),
      button
   );
});
