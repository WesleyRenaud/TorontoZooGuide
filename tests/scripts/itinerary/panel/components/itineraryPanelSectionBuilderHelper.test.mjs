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
   bodyInner.appendChild(document.createElement('div'));
   bodyInner.appendChild(document.createElement('div'));

   ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight(body, bodyInner);

   assert.equal(body.style.display, '');
   assert.equal(body.style.maxHeight, 'none');
   assert.equal(body.style.overflowY, 'hidden');
});

test('Test_UpdateSectionBodyHeight_TestManyItems_ExpectMaxHeight', () => {
   const body = document.createElement('div');
   const bodyInner = document.createElement('div');

   for (let index = 0; index < 5; index += 1) {
      const item = document.createElement('div');
      item.getBoundingClientRect = () => ({
         height: 20,
         width: 0,
         top: 0,
         left: 0,
         right: 0,
         bottom: 20,
      });
      bodyInner.appendChild(item);
   }

   window.getComputedStyle = () => ({
      rowGap: '4',
      gap: '4',
      paddingTop: '2',
      paddingBottom: '2',
   });
   globalThis.getComputedStyle = window.getComputedStyle;

   ItineraryPanelSectionBuilderHelper.updateSectionBodyHeight(body, bodyInner);

   assert.equal(body.style.maxHeight, '72px');
   assert.equal(body.style.overflowY, 'auto');
   assert.equal(body.style.overflowX, 'hidden');
});
