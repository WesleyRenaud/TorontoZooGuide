import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPillMenuBuilder } from '../../../../../scripts/itinerary/panel/components/itineraryPillMenuBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ResolvePillStrip_TestClosest_ExpectStrip', () => {
   const strip = document.createElement('div');
   strip.className = 'itinerary-day-pill-strip';
   const pill = document.createElement('div');
   strip.appendChild(pill);
   pill.closest = (selector) => (selector === `.${strip.className}` ? strip : null);

   const resolved = ItineraryPillMenuBuilder.resolvePillStrip(pill);

   assert.equal(resolved, strip);
});


test('Test_ResolvePillStrip_TestMissing_ExpectNull', () => {
   const pill = {};

   const resolved = ItineraryPillMenuBuilder.resolvePillStrip(pill);

   assert.equal(resolved, null);
});


test('Test_BuildPillMenuButtonDots_TestDefault_ExpectThreeDots', () => {
   const dots = ItineraryPillMenuBuilder.buildPillMenuButtonDots();

   assert.equal(dots.className, 'itinerary-day-open-pill-menu-dots');
   assert.equal(dots.children.length, 3);
});


test('Test_RenderMenuPanel_TestItems_ExpectButtons', () => {
   const removeLabel = 'Remove';
   const editLabel = 'Edit';
   const menuItems = [
      { label: removeLabel },
      { label: editLabel },
   ];
   const menuPanel = document.createElement('div');
   menuPanel.appendChild(document.createElement('span'));

   ItineraryPillMenuBuilder.renderMenuPanel(menuPanel, menuItems);

   assert.equal(menuPanel.children.length, menuItems.length);
   assert.equal(menuPanel.children.at(Position.FIRST).textContent, removeLabel);
   assert.equal(menuPanel.children.at(Position.FIRST).getAttribute('role'), 'menuitem');
});


test('Test_BindMenuPanelActions_TestClick_ExpectCloseAndAction', async () => {
   const removeLabel = 'Remove';
   const menuPanel = document.createElement('div');
   const closes = [];
   const actions = [];
   const menuItems = [{
      label: removeLabel,
      onAction: async () => { actions.push('remove'); },
   }];

   ItineraryPillMenuBuilder.renderMenuPanel(menuPanel, menuItems);
   ItineraryPillMenuBuilder.bindMenuPanelActions(
      menuPanel,
      menuItems,
      () => { closes.push(true); }
   );
   await menuPanel.children.at(Position.FIRST).listeners.click({ stopPropagation() {} });

   assert.deepEqual(closes, [true]);
   assert.deepEqual(actions, ['remove']);
});


test('Test_BindMenuPanelActions_TestMissingOnAction_ExpectSkipped', () => {
   const menuItems = [{ label: 'Remove' }];
   const menuPanel = document.createElement('div');

   ItineraryPillMenuBuilder.renderMenuPanel(menuPanel, menuItems);
   ItineraryPillMenuBuilder.bindMenuPanelActions(
      menuPanel,
      menuItems,
      () => {}
   );

   assert.equal(menuPanel.children.at(Position.FIRST).listeners?.click, undefined);
});
