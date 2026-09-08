import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryRenderer } from '../../../scripts/itinerary/itineraryRenderer.js';
import { RenderView } from '../../../scripts/itinerary/panel/renderView.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_GetItineraryPanelBody_TestMissingPanel_ExpectNull', () => {
   assert.equal(ItineraryRenderer.getItineraryPanelBody(), null);
});

test('Test_GetItineraryPanelBody_TestPresentPanel_ExpectBody', () => {
   const body = document.createElement('div');
   const originalQuery = document.querySelector;
   document.querySelector = (selector) => {
      if (selector === '.itinerary-panel .side-panel-body') {
         return body;
      }
      return originalQuery.call(document, selector);
   };

   try {
      assert.equal(ItineraryRenderer.getItineraryPanelBody(), body);
   } finally {
      document.querySelector = originalQuery;
   }
});

test('Test_RenderItineraryPanel_TestBodyEl_ExpectDelegatesToRenderView', () => {
   const originalRender = RenderView.renderItineraryPanelInto;
   const calls = [];

   RenderView.renderItineraryPanelInto = (bodyEl) => {
      calls.push(bodyEl);
      return 'rendered';
   };

   try {
      const bodyEl = document.createElement('div');
      assert.equal(ItineraryRenderer.renderItineraryPanel(bodyEl), 'rendered');
      assert.deepEqual(calls, [bodyEl]);
   } finally {
      RenderView.renderItineraryPanelInto = originalRender;
   }
});
