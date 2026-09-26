import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelSectionBuilderHelper } from '../../../../../scripts/itinerary/panel/components/itineraryPanelSectionBuilderHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_UpdateSectionBodyHeight_TestEmpty_ExpectHidden', () => {
   const body = document.createElement('div');
   const bodyInner = document.createElement('div');

   ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight(body, bodyInner);

   assert.equal(body.style.display, 'none');
   assert.equal(body.style.maxHeight, 'none');
   assert.equal(body.style.overflowY, 'hidden');
});


test('Test_UpdateSectionBodyHeight_TestFewItems_ExpectNoScroll', () => {
   const body = document.createElement('div');
   const bodyInner = document.createElement('div');
   const itemCount = ItineraryPanelSectionBuilderHelper.MAX_VISIBLE_ITEMS - 1;

   for (let index = 0; index < itemCount; index += 1) {
      bodyInner.appendChild(document.createElement('div'));
   }

   ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight(body, bodyInner);

   assert.equal(body.style.display, '');
   assert.equal(body.style.maxHeight, 'none');
   assert.equal(body.style.overflowY, 'hidden');
});


test('Test_UpdateSectionBodyHeight_TestManyItems_ExpectMaxHeight', () => {
   const itemHeight = 20;
   const rowGap = 4;
   const paddingTop = 2;
   const paddingBottom = 2;
   const itemCount = ItineraryPanelSectionBuilderHelper.MAX_VISIBLE_ITEMS + 2;
   const visibleItemCount = ItineraryPanelSectionBuilderHelper.MAX_VISIBLE_ITEMS;
   const itemsHeight = itemHeight * visibleItemCount;
   const totalGap = rowGap * Math.max(0, visibleItemCount - 1);
   const maxHeight = Math.ceil(itemsHeight + totalGap + paddingTop + paddingBottom);
   const body = document.createElement('div');
   const bodyInner = document.createElement('div');

   for (let index = 0; index < itemCount; index += 1) {
      const item = document.createElement('div');
      item.getBoundingClientRect = () => ({
         height: itemHeight,
         width: 0,
         top: 0,
         left: 0,
         right: 0,
         bottom: itemHeight,
      });
      bodyInner.appendChild(item);
   }

   window.getComputedStyle = () => ({
      rowGap: String(rowGap),
      gap: String(rowGap),
      paddingTop: String(paddingTop),
      paddingBottom: String(paddingBottom),
   });
   globalThis.getComputedStyle = window.getComputedStyle;

   ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight(body, bodyInner);

   assert.equal(body.style.maxHeight, `${maxHeight}px`);
   assert.equal(body.style.overflowY, 'auto');
   assert.equal(body.style.overflowX, 'hidden');
});
