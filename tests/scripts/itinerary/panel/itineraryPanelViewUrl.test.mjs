import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryPanelViews } from '../../../../scripts/itinerary/panel/components/itineraryPanelViews.js';
import { ItineraryPanelViewUrl } from '../../../../scripts/itinerary/panel/itineraryPanelViewUrl.js';

test('Test_NormalizeItineraryPanelView_TestUnknownValues_ExpectListFallback', () => {
   assert.equal(ItineraryPanelViewUrl.normalizeItineraryPanelView('dayPlanner'), 'dayPlanner');
   assert.equal(
      ItineraryPanelViewUrl.normalizeItineraryPanelView('invalid'),
      ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list
   );
   assert.equal(
      ItineraryPanelViewUrl.normalizeItineraryPanelView(null),
      ItineraryPanelViews.ITINERARY_PANEL_VIEWS.list
   );
});

test('Test_GetItineraryPanelViewFromUrl_TestViewQueryParam_ExpectDayPlanner', () => {
   const location = {
      href: `https://example.test/itinerary.html?${ItineraryPanelViewUrl.ITINERARY_PANEL_VIEW_QUERY_PARAM}=dayPlanner`,
   };

   assert.equal(
      ItineraryPanelViewUrl.getItineraryPanelViewFromUrl(location),
      ItineraryPanelViews.ITINERARY_PANEL_VIEWS.dayPlanner
   );
});

test('Test_SetItineraryPanelViewInUrl_TestViewQueryParam_ExpectUpdated', () => {
   const location = {
      href: 'https://example.test/itinerary.html',
   };
   const history = {
      replaceState(_state, _title, url) {
         location.href = url;
      },
   };

   ItineraryPanelViewUrl.setItineraryPanelViewInUrl('dayPlanner', { location, history });

   assert.equal(
      ItineraryPanelViewUrl.getItineraryPanelViewFromUrl(location),
      ItineraryPanelViews.ITINERARY_PANEL_VIEWS.dayPlanner
   );
});
