import assert from 'node:assert/strict';
import { test } from 'node:test';

import { PanelNavigator } from '../../../../scripts/consoleOperations/shell/panelNavigator.js';

function createClassList() {
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

function createPanel(id) {
   return {
      id,
      classList: createClassList(),
   };
}

function createButton(panelId) {
   return {
      dataset: {
         panelTarget: panelId,
      },
      classList: createClassList(),
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

function createDocumentMock({ panels, buttons }) {
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

function createUrlState(href = 'https://example.test/console-operations.html') {
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
   const urlState = createUrlState();
   const restaurantPanel = createPanel('restaurantOpeningSchedulePanel');
   const giftShopPanel = createPanel('giftShopOpeningSchedulePanel');
   const restaurantButton = createButton('restaurantOpeningSchedulePanel');
   const giftShopButton = createButton('giftShopOpeningSchedulePanel');
   const doc = createDocumentMock({
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
   const urlState = createUrlState();
   const panel = createPanel('giftShopOpeningSchedulePanel');
   const button = createButton('giftShopOpeningSchedulePanel');
   const doc = createDocumentMock({
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
   const urlState = createUrlState(
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
