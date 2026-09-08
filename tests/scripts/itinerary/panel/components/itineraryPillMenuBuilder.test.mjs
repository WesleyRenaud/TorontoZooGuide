import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPillMenuBuilder } from '../../../../../scripts/itinerary/panel/components/itineraryPillMenuBuilder.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ResolvePillStrip_TestClosest_ExpectStripOrNull', () => {
   const strip = document.createElement('div');
   strip.className = 'itinerary-day-pill-strip';
   const pill = document.createElement('div');
   strip.appendChild(pill);
   pill.closest = (selector) => (selector === '.itinerary-day-pill-strip' ? strip : null);

   assert.equal(ItineraryPillMenuBuilder.resolvePillStrip(pill), strip);
   assert.equal(ItineraryPillMenuBuilder.resolvePillStrip({}), null);
});

test('Test_BuildPillMenuButtonDots_TestDefault_ExpectThreeDots', () => {
   const dots = ItineraryPillMenuBuilder.buildPillMenuButtonDots();
   assert.equal(dots.className, 'itinerary-day-open-pill-menu-dots');
   assert.equal(dots.children.length, 3);
});

test('Test_RenderMenuPanel_TestItems_ExpectButtons', () => {
   const menuPanel = document.createElement('div');
   menuPanel.appendChild(document.createElement('span'));

   ItineraryPillMenuBuilder.renderMenuPanel(menuPanel, [
      { label: 'Remove' },
      { label: 'Edit' },
   ]);

   assert.equal(menuPanel.children.length, 2);
   assert.equal(menuPanel.children[0].textContent, 'Remove');
   assert.equal(menuPanel.children[0].getAttribute('role'), 'menuitem');
});

test('Test_BindMenuPanelActions_TestClick_ExpectCloseAndAction', async () => {
   const menuPanel = document.createElement('div');
   const closes = [];
   const actions = [];

   ItineraryPillMenuBuilder.renderMenuPanel(menuPanel, [{ label: 'Remove' }]);
   ItineraryPillMenuBuilder.bindMenuPanelActions(
      menuPanel,
      [{
         label: 'Remove',
         onAction: async () => { actions.push('remove'); },
      }],
      () => { closes.push(true); }
   );

   await menuPanel.children[0].listeners.click({ stopPropagation() {} });
   assert.deepEqual(closes, [true]);
   assert.deepEqual(actions, ['remove']);
});
