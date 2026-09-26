import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelView } from '../../../../scripts/itinerary/panel/components/itineraryPanelView.js';
import { ItineraryPanelViewResolver } from '../../../../scripts/itinerary/panel/itineraryPanelViewResolver.js';
import { ItineraryPanelViewStore } from '../../../../scripts/itinerary/panel/itineraryPanelViewStore.js';


test('Test_ResetActiveItineraryPanelView_TestList_ExpectList', () => {
   const originalSet = ItineraryPanelViewResolver.setItineraryPanelViewInUrl;
   ItineraryPanelViewResolver.setItineraryPanelViewInUrl = () => {};
   const view = ItineraryPanelView.ITINERARY_PANEL_VIEWS.list;

   try {
      ItineraryPanelViewStore.resetActiveItineraryPanelView(view);

      const activeView = ItineraryPanelViewStore.getActiveItineraryPanelView();

      assert.equal(activeView, view);
   } finally {
      ItineraryPanelViewResolver.setItineraryPanelViewInUrl = originalSet;
      ItineraryPanelViewStore.resetActiveItineraryPanelView(ItineraryPanelView.ITINERARY_PANEL_VIEWS.list);
   }
});


test('Test_SetActiveItineraryPanelView_TestDayPlanner_ExpectUrlUpdated', () => {
   const originalSet = ItineraryPanelViewResolver.setItineraryPanelViewInUrl;
   const urls = [];
   ItineraryPanelViewResolver.setItineraryPanelViewInUrl = (nextView) => { urls.push(nextView); };
   const view = ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner;

   try {
      ItineraryPanelViewStore.resetActiveItineraryPanelView(ItineraryPanelView.ITINERARY_PANEL_VIEWS.list);
      ItineraryPanelViewStore.setActiveItineraryPanelView(view);

      const activeView = ItineraryPanelViewStore.getActiveItineraryPanelView();

      assert.equal(activeView, view);
      assert.deepEqual(urls, [view]);
   } finally {
      ItineraryPanelViewResolver.setItineraryPanelViewInUrl = originalSet;
      ItineraryPanelViewStore.resetActiveItineraryPanelView(ItineraryPanelView.ITINERARY_PANEL_VIEWS.list);
   }
});
