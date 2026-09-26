import assert from 'node:assert/strict';
import test from 'node:test';

import { ItemRowHelper } from '../../../../../scripts/itinerary/panel/components/itemRowHelper.js';
import { ItemView } from '../../../../../scripts/itinerary/panel/components/itemView.js';
import { ItineraryPanelHelper } from '../../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_MakeItemRow_TestContentAndActions_ExpectRow', () => {
   const originalName = ItemRowHelper.createItemNameElement;
   const originalSafeImg = ItineraryPanelHelper.safeImg;
   const species = 'African Lion';
   const imageSrc = 'lion.jpg';
   const region = 'Africa';
   const enclosure = 'Savanna';
   const alertLine = 'Low visibility';
   const linkClicks = [];
   const actions = [];
   const removeLabel = 'remove';
   const keepLabel = 'keep';

   ItemRowHelper.createItemNameElement = () => {
      const el = document.createElement('div');
      el.className = 'itin-panel-name';
      el.textContent = species;
      return el;
   };
   ItineraryPanelHelper.safeImg = (src) => {
      const img = document.createElement('img');
      img.src = src;
      return img;
   };

   try {
      const row = ItemView.makeItemRow({
         name: species,
         imageSrc,
         metaLines: [region, '', enclosure],
         alertLine,
         alertTone: 'default',
         linkText: 'Details',
         onLinkClick: () => linkClicks.push(true),
         actionLabel: 'Remove',
         onAction: () => actions.push(removeLabel),
         secondaryActionLabel: 'Keep',
         onSecondaryAction: () => actions.push(keepLabel),
      });
      const link = row.children.at(Position.FIRST).children
         .find((child) => child.classList?.contains('itin-panel-text'))
         ?.children
         .find((child) => child.classList?.contains('itin-panel-link'));
      link.listeners.click({ stopPropagation() {} });
      const actionButtons = row.children
         .find((child) => child.classList?.contains('itin-panel-item-actions'))
         ?.children ?? [];
      actionButtons.at(Position.FIRST).listeners.click({ stopPropagation() {} });
      actionButtons.at(Position.SECOND).listeners.click({ stopPropagation() {} });

      assert.ok(row.classList.contains('itin-panel-item'));
      assert.ok(row.querySelector('.itin-panel-thumb'));
      assert.match(row.textContent, new RegExp(region));
      assert.match(row.textContent, new RegExp(enclosure));
      assert.match(row.textContent, new RegExp(alertLine));
      assert.deepEqual(linkClicks, [true]);
      assert.equal(actionButtons.length, 2);
      assert.deepEqual(actions, [removeLabel, keepLabel]);
   } finally {
      ItemRowHelper.createItemNameElement = originalName;
      ItineraryPanelHelper.safeImg = originalSafeImg;
   }
});


test('Test_MakeItemRow_TestPositiveAlert_ExpectPositiveClass', () => {
   const originalName = ItemRowHelper.createItemNameElement;
   const originalSafeImg = ItineraryPanelHelper.safeImg;
   const species = 'Amur Tiger';
   const alertLine = 'Improved';
   const alertTone = 'positive';

   ItemRowHelper.createItemNameElement = () => {
      const el = document.createElement('div');
      el.className = 'itin-panel-name';
      el.textContent = species;
      return el;
   };
   ItineraryPanelHelper.safeImg = (src) => {
      const img = document.createElement('img');
      img.src = src;
      return img;
   };

   try {
      const row = ItemView.makeItemRow({
         name: species,
         alertLine,
         alertTone,
      });
      const hasPositiveAlert = row.children.at(Position.FIRST).children
         .find((child) => child.classList?.contains('itin-panel-text'))
         ?.children
         .some((child) => child.classList?.contains(`itin-panel-alert-${alertTone}`));

      assert.ok(hasPositiveAlert);
   } finally {
      ItemRowHelper.createItemNameElement = originalName;
      ItineraryPanelHelper.safeImg = originalSafeImg;
   }
});
