import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelViewStore } from '../../../../scripts/itinerary/panel/itineraryPanelViewStore.js';
import { ItineraryPanelViewResolver } from '../../../../scripts/itinerary/panel/itineraryPanelViewResolver.js';

test('Test_ActiveItineraryPanelView_TestGetSetReset_ExpectValue', () => {
   const originalSet = ItineraryPanelViewResolver.setItineraryPanelViewInUrl;
   const urls = [];
   ItineraryPanelViewResolver.setItineraryPanelViewInUrl = (view) => { urls.push(view); };

   try {
      ItineraryPanelViewStore.resetActiveItineraryPanelView('list');
      assert.equal(ItineraryPanelViewStore.getActiveItineraryPanelView(), 'list');

      ItineraryPanelViewStore.setActiveItineraryPanelView('day');
      assert.equal(ItineraryPanelViewStore.getActiveItineraryPanelView(), 'day');
      assert.deepEqual(urls, ['day']);
   } finally {
      ItineraryPanelViewResolver.setItineraryPanelViewInUrl = originalSet;
      ItineraryPanelViewStore.resetActiveItineraryPanelView('list');
   }
});
