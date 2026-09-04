import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { ItineraryPillMenu } from '../../../../../scripts/itinerary/panel/components/itineraryPillMenu.js';
import { installDocument, teardownDocument } from '../../../helpers/domMock.mjs';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';

let documentListeners = {};

beforeEach(() => {
   installDocument();
   documentListeners = {};
   document.addEventListener = (eventName, handler) => {
      documentListeners[eventName] = handler;
   };
   document.removeEventListener = (eventName, handler) => {
      if (documentListeners[eventName] === handler) {
         delete documentListeners[eventName];
      }
   };
});

afterEach(() => {
   teardownDocument();
});

test('Test_BuildPillMenuNodes_TestAccessible_ExpectHiddenPanel', () => {
   const { menu, menuButton, menuPanel } = ItineraryPillMenu.buildPillMenuNodes('Scheduled item options', [
      { label: 'Unschedule' },
      { label: 'Remove' },
   ]);

   assert.ok(menu.classList.contains('itinerary-day-open-pill-menu'));
   assert.equal(menuButton.getAttribute('aria-label'), 'Scheduled item options');
   assert.equal(menuButton.getAttribute('aria-haspopup'), 'menu');
   assert.equal(menuButton.getAttribute('aria-expanded'), 'false');
   assert.ok(menuButton.querySelector('.itinerary-day-open-pill-menu-dots'));
   assert.equal(menuPanel.getAttribute('role'), 'menu');
   assert.equal(menuPanel.hidden, true);
   assert.equal(
      menuPanel.querySelectorAll('.itinerary-day-open-pill-menu-item').length,
      2
   );
   assert.equal(
      menuPanel.querySelectorAll('.itinerary-day-open-pill-menu-item')[0]?.textContent,
      'Unschedule'
   );
});

test('Test_BindPillMenu_TestMenuButton_ExpectToggle', () => {
   const pill = createDomNode('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const { menu, menuButton, menuPanel } = ItineraryPillMenu.buildPillMenuNodes('Menu', [
      { label: 'Remove', onAction: () => {} },
   ]);

   pill.appendChild(menu);
   ItineraryPillMenu.bindPillMenu(pill, {
      menuButton,
      menuPanel,
      menuItems: [{ label: 'Remove', onAction: () => {} }],
   });

   menuButton.click();

   assert.equal(menuPanel.hidden, false);
   assert.equal(menuButton.getAttribute('aria-expanded'), 'true');
   assert.ok(pill.classList.contains('itinerary-day-open-pill--menu-open'));

   menuButton.click();

   assert.equal(menuPanel.hidden, true);
   assert.equal(menuButton.getAttribute('aria-expanded'), 'false');
   assert.equal(pill.classList.contains('itinerary-day-open-pill--menu-open'), false);
});

test('Test_BindPillMenu_TestOutsideClick_ExpectClosed', () => {
   const pill = createDomNode('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const outside = createDomNode('div');
   const { menu, menuButton, menuPanel } = ItineraryPillMenu.buildPillMenuNodes('Menu', [
      { label: 'Remove', onAction: () => {} },
   ]);

   pill.appendChild(menu);
   document.body.appendChild(outside);
   ItineraryPillMenu.bindPillMenu(pill, {
      menuButton,
      menuPanel,
      menuItems: [{ label: 'Remove', onAction: () => {} }],
   });

   menuButton.click();
   documentListeners.click?.({ target: outside });

   assert.equal(menuPanel.hidden, true);
   assert.equal(menuButton.getAttribute('aria-expanded'), 'false');
});

test('Test_BindPillMenu_TestMenuItemAction_ExpectInvokeAndClose', async () => {
   let removed = false;
   const pill = createDomNode('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const menuItems = [{ label: 'Remove', onAction: async () => { removed = true; } }];
   const { menu, menuButton, menuPanel } = ItineraryPillMenu.buildPillMenuNodes('Menu', menuItems);

   pill.appendChild(menu);
   ItineraryPillMenu.bindPillMenu(pill, { menuButton, menuPanel, menuItems });

   menuButton.click();
   menuPanel.querySelector('.itinerary-day-open-pill-menu-item')?.click();

   assert.equal(removed, true);
   assert.equal(menuPanel.hidden, true);
});

test('Test_BindPillMenu_TestGetMenuItems_ExpectRefreshOnReopen', () => {
   const pill = createDomNode('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   let menuItems = [{ label: 'First', onAction: () => {} }];
   const { menu, menuButton, menuPanel } = ItineraryPillMenu.buildPillMenuNodes('Menu', menuItems);

   pill.appendChild(menu);
   ItineraryPillMenu.bindPillMenu(pill, {
      menuButton,
      menuPanel,
      getMenuItems: () => menuItems,
   });

   menuButton.click();
   assert.equal(
      menuPanel.querySelector('.itinerary-day-open-pill-menu-item')?.textContent,
      'First'
   );

   menuButton.click();
   menuItems = [{ label: 'Second', onAction: () => {} }];
   menuButton.click();

   assert.equal(
      menuPanel.querySelector('.itinerary-day-open-pill-menu-item')?.textContent,
      'Second'
   );
});
