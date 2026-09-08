import assert from 'node:assert/strict';
import { test } from 'node:test';

import { PanelNavigator } from '../../../../scripts/consoleOperations/shell/panelNavigator.js';

function _createClassList() {
   const classes = new Set();

   return {
      add: className => classes.add(className),
      remove: className => classes.delete(className),
      contains: className => classes.has(className),
      toggle: (className, enabled) => {
         if (enabled) {
            classes.add(className);
            return true;
         }

         classes.delete(className);
         return false;
      },
   };
}

function _createPanel(id) {
   return {
      id,
      classList: _createClassList(),
   };
}

function _createButton(panelId) {
   return {
      dataset: {
         panelTarget: panelId,
      },
      classList: _createClassList(),
      clickCount: 0,
      ariaCurrent: undefined,
      setAttribute(name, value) {
         if (name === 'aria-current') {
            this.ariaCurrent = value;
         }
      },
      removeAttribute(name) {
         if (name === 'aria-current') {
            this.ariaCurrent = undefined;
         }
      },
      click() {
         this.clickCount += 1;
      },
   };
}

function _createDocumentMock({ panels, buttons }) {
   return {
      querySelectorAll(selector) {
         if (selector === '.console-operations-panel') {
            return panels;
         }

         if (selector === '.console-operations-menu-btn') {
            return buttons;
         }

         return [];
      },
   };
}

function _createUrlState(href = 'https://example.test/console-operations.html') {
   const location = { href };
   const history = {
      replaceState(_state, _title, url) {
         location.href = String(url);
      },
   };

   return {
      history,
      location,
   };
}

test('Test_CreateConsolePanelNavigator_TestActivate_ExpectUrlAndRestore', () => {
   const urlState = _createUrlState();
   const restaurantPanel = _createPanel('restaurantOpeningSchedulePanel');
   const giftShopPanel = _createPanel('giftShopOpeningSchedulePanel');
   const restaurantButton = _createButton('restaurantOpeningSchedulePanel');
   const giftShopButton = _createButton('giftShopOpeningSchedulePanel');
   const doc = _createDocumentMock({
      panels: [restaurantPanel, giftShopPanel],
      buttons: [restaurantButton, giftShopButton],
   });

   const navigator = PanelNavigator.createConsolePanelNavigator(doc, urlState);

   navigator.activatePanel(giftShopPanel);

   const url = new URL(urlState.location.href);

   assert.equal(
      url.searchParams.get(PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM),
      'giftShopOpeningSchedulePanel'
   );
   assert.equal(giftShopPanel.classList.contains('active'), true);
   assert.equal(giftShopButton.classList.contains('active'), true);
   assert.equal(giftShopButton.ariaCurrent, 'page');
   assert.equal(restaurantButton.ariaCurrent, undefined);

   navigator.restorePanelFromUrl();

   assert.equal(giftShopButton.clickCount, 1);
   assert.equal(restaurantButton.clickCount, 0);
});

test('Test_CreateConsolePanelNavigator_TestHide_ExpectUrlCleared', () => {
   const urlState = _createUrlState();
   const panel = _createPanel('giftShopOpeningSchedulePanel');
   const button = _createButton('giftShopOpeningSchedulePanel');
   const doc = _createDocumentMock({
      panels: [panel],
      buttons: [button],
   });
   const navigator = PanelNavigator.createConsolePanelNavigator(doc, urlState);

   navigator.activatePanel(panel);
   navigator.hidePanels();

   assert.equal(
      new URL(urlState.location.href).searchParams.has(
         PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM
      ),
      false
   );
   assert.equal(panel.classList.contains('active'), false);
   assert.equal(button.classList.contains('active'), false);
});

test('Test_ClearConsolePanelUrlParam_TestClear_ExpectRemoved', () => {
   const urlState = _createUrlState(
      'https://example.test/console-operations.html?panel=giftShopOpeningSchedulePanel'
   );

   PanelNavigator.clearConsolePanelUrlParam(urlState);

   assert.equal(
      new URL(urlState.location.href).searchParams.has(
         PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM
      ),
      false
   );
});
