import assert from 'node:assert/strict';
import test from 'node:test';

import { ItemRowHelper } from '../../../../../scripts/itinerary/panel/components/itemRowHelper.js';
import { ItemView } from '../../../../../scripts/itinerary/panel/components/itemView.js';
import { ItineraryPanelHelper } from '../../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_MakeItemRow_TestContentAndActions_ExpectRow', () => {
   const originalName = ItemRowHelper.createItemNameElement;
   const originalSafeImg = ItineraryPanelHelper.safeImg;
   const linkClicks = [];
   const actions = [];

   ItemRowHelper.createItemNameElement = () => {
      const el = document.createElement('div');
      el.className = 'itin-panel-name';
      el.textContent = 'Lion';
      return el;
   };
   ItineraryPanelHelper.safeImg = (src) => {
      const img = document.createElement('img');
      img.src = src;
      return img;
   };

   try {
      const row = ItemView.makeItemRow({
         name: 'Lion',
         imageSrc: 'lion.jpg',
         metaLines: ['Africa', '', 'Savanna'],
         alertLine: 'Low visibility',
         alertTone: 'default',
         linkText: 'Details',
         onLinkClick: () => linkClicks.push(true),
         actionLabel: 'Remove',
         onAction: () => actions.push('remove'),
         secondaryActionLabel: 'Keep',
         onSecondaryAction: () => actions.push('keep'),
      });

      assert.ok(row.classList.contains('itin-panel-item'));
      assert.ok(row.querySelector('.itin-panel-thumb'));
      assert.match(row.textContent, /Africa/);
      assert.match(row.textContent, /Savanna/);
      assert.match(row.textContent, /Low visibility/);

      const link = row.children[0].children
         .find((child) => child.classList?.contains('itin-panel-text'))
         ?.children
         .find((child) => child.classList?.contains('itin-panel-link'));
      link.listeners.click({ stopPropagation() {} });
      assert.deepEqual(linkClicks, [true]);

      const actionButtons = row.children
         .find((child) => child.classList?.contains('itin-panel-item-actions'))
         ?.children ?? [];
      assert.equal(actionButtons.length, 2);
      actionButtons[0].listeners.click({ stopPropagation() {} });
      actionButtons[1].listeners.click({ stopPropagation() {} });
      assert.deepEqual(actions, ['remove', 'keep']);

      const positive = ItemView.makeItemRow({
         name: 'Tiger',
         alertLine: 'Improved',
         alertTone: 'positive',
      });
      assert.ok(
         positive.children[0].children
            .find((child) => child.classList?.contains('itin-panel-text'))
            ?.children
            .some((child) => child.classList?.contains('itin-panel-alert-positive'))
      );
   } finally {
      ItemRowHelper.createItemNameElement = originalName;
      ItineraryPanelHelper.safeImg = originalSafeImg;
   }
});
