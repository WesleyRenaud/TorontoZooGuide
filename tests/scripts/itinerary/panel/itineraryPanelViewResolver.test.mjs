import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryPanelView } from '../../../../scripts/itinerary/panel/components/itineraryPanelView.js';
import { ItineraryPanelViewResolver } from '../../../../scripts/itinerary/panel/itineraryPanelViewResolver.js';

test('Test_NormalizeItineraryPanelView_TestUnknownValues_ExpectListFallback', () => {
   assert.equal(ItineraryPanelViewResolver.normalizeItineraryPanelView('dayPlanner'), 'dayPlanner');
   assert.equal(
      ItineraryPanelViewResolver.normalizeItineraryPanelView('invalid'),
      ItineraryPanelView.ITINERARY_PANEL_VIEWS.list
   );
   assert.equal(
      ItineraryPanelViewResolver.normalizeItineraryPanelView(null),
      ItineraryPanelView.ITINERARY_PANEL_VIEWS.list
   );
});

test('Test_GetItineraryPanelViewFromUrl_TestViewQueryParam_ExpectDayPlanner', () => {
   const location = {
      href: `https://example.test/itinerary.html?${ItineraryPanelViewResolver.ITINERARY_PANEL_VIEW_QUERY_PARAM}=dayPlanner`,
   };

   assert.equal(
      ItineraryPanelViewResolver.getItineraryPanelViewFromUrl(location),
      ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner
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

   ItineraryPanelViewResolver.setItineraryPanelViewInUrl('dayPlanner', { location, history });

   assert.equal(
      ItineraryPanelViewResolver.getItineraryPanelViewFromUrl(location),
      ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner
   );
});
