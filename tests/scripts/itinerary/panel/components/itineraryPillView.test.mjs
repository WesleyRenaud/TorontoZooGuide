import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { ItineraryPillView } from '../../../../../scripts/itinerary/panel/components/itineraryPillView.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
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
   const menuAriaLabel = 'Scheduled item options';
   const unscheduleLabel = 'Unschedule';
   const menuItems = [
      { label: unscheduleLabel },
      { label: 'Remove' },
   ];

   const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes(
      menuAriaLabel,
      menuItems
   );

   assert.ok(menu.classList.contains('itinerary-day-open-pill-menu'));
   assert.equal(menuButton.getAttribute('aria-label'), menuAriaLabel);
   assert.equal(menuButton.getAttribute('aria-haspopup'), 'menu');
   assert.equal(menuButton.getAttribute('aria-expanded'), 'false');
   assert.ok(menuButton.querySelector('.itinerary-day-open-pill-menu-dots'));
   assert.equal(menuPanel.getAttribute('role'), 'menu');
   assert.equal(menuPanel.hidden, true);
   assert.equal(
      menuPanel.querySelectorAll('.itinerary-day-open-pill-menu-item').length,
      menuItems.length
   );
   assert.equal(
      menuPanel.querySelectorAll('.itinerary-day-open-pill-menu-item')[Position.FIRST]?.textContent,
      unscheduleLabel
   );
});


test('Test_BindPillMenu_TestMenuButton_ExpectToggle', () => {
   const pill = createDomNode('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const menuItems = [{ label: 'Remove', onAction: () => {} }];
   const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes('Menu', menuItems);

   pill.appendChild(menu);
   ItineraryPillView.bindPillMenu(pill, {
      menuButton,
      menuPanel,
      menuItems,
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
   const menuItems = [{ label: 'Remove', onAction: () => {} }];
   const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes('Menu', menuItems);

   pill.appendChild(menu);
   document.body.appendChild(outside);
   ItineraryPillView.bindPillMenu(pill, {
      menuButton,
      menuPanel,
      menuItems,
   });
   menuButton.click();
   documentListeners.click?.({ target: outside });

   assert.equal(menuPanel.hidden, true);
   assert.equal(menuButton.getAttribute('aria-expanded'), 'false');
});


test('Test_BindPillMenu_TestPanelClick_ExpectStopPropagation', () => {
   const pill = createDomNode('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const menuItems = [{ label: 'Remove', onAction: () => {} }];
   const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes('Menu', menuItems);
   const stopped = [];

   pill.appendChild(menu);
   ItineraryPillView.bindPillMenu(pill, {
      menuButton,
      menuPanel,
      menuItems,
   });
   menuButton.click();
   menuPanel.listeners.click({
      stopPropagation() {
         stopped.push(true);
      },
   });

   assert.equal(menuPanel.hidden, false);
   assert.deepEqual(stopped, [true]);
});


test('Test_BindPillMenu_TestCleanup_ExpectUnbind', () => {
   const pill = createDomNode('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const menuItems = [{ label: 'Remove', onAction: () => {} }];
   const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes('Menu', menuItems);

   pill.appendChild(menu);
   ItineraryPillView.bindPillMenu(pill, {
      menuButton,
      menuPanel,
      menuItems,
   });
   menuButton.click();
   pill.__tzgCleanup?.();

   assert.equal(menuPanel.hidden, true);
   assert.equal(documentListeners.click, undefined);
});


test('Test_BindPillMenu_TestMenuItemAction_ExpectInvokeAndClose', async () => {
   let removed = false;
   const pill = createDomNode('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   const menuItems = [{ label: 'Remove', onAction: async () => { removed = true; } }];
   const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes('Menu', menuItems);

   pill.appendChild(menu);
   ItineraryPillView.bindPillMenu(pill, { menuButton, menuPanel, menuItems });
   menuButton.click();
   menuPanel.querySelector('.itinerary-day-open-pill-menu-item')?.click();

   assert.equal(removed, true);
   assert.equal(menuPanel.hidden, true);
});


test('Test_BindPillMenu_TestGetMenuItems_ExpectRefreshOnReopen', () => {
   const firstLabel = 'Unschedule';
   const secondLabel = 'Remove';
   const pill = createDomNode('span', 'itinerary-day-open-pill itinerary-day-open-pill--with-menu');
   let menuItems = [{ label: firstLabel, onAction: () => {} }];
   const { menu, menuButton, menuPanel } = ItineraryPillView.buildPillMenuNodes('Menu', menuItems);

   pill.appendChild(menu);
   ItineraryPillView.bindPillMenu(pill, {
      menuButton,
      menuPanel,
      getMenuItems: () => menuItems,
   });
   menuButton.click();
   const firstText = menuPanel.querySelector('.itinerary-day-open-pill-menu-item')?.textContent;
   menuButton.click();
   menuItems = [{ label: secondLabel, onAction: () => {} }];
   menuButton.click();

   assert.equal(firstText, firstLabel);
   assert.equal(
      menuPanel.querySelector('.itinerary-day-open-pill-menu-item')?.textContent,
      secondLabel
   );
});
