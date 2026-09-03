import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   ITINERARY_PANEL_VIEW_QUERY_PARAM,
   getItineraryPanelViewFromUrl,
   normalizeItineraryPanelView,
   setItineraryPanelViewInUrl,
} from '../../scripts/itinerary/panel/itineraryPanelViewUrl.js';
import { ITINERARY_PANEL_VIEWS } from '../../scripts/itinerary/panel/components/itineraryPanelViews.js';

test('normalizeItineraryPanelView falls back to list for unknown values', () => {
   assert.equal(normalizeItineraryPanelView('dayPlanner'), 'dayPlanner');
   assert.equal(normalizeItineraryPanelView('invalid'), ITINERARY_PANEL_VIEWS.list);
   assert.equal(normalizeItineraryPanelView(null), ITINERARY_PANEL_VIEWS.list);
});

test('getItineraryPanelViewFromUrl reads the view query param', () => {
   const location = {
      href: `https://example.test/itinerary.html?${ITINERARY_PANEL_VIEW_QUERY_PARAM}=dayPlanner`,
   };

   assert.equal(
      getItineraryPanelViewFromUrl(location),
      ITINERARY_PANEL_VIEWS.dayPlanner
   );
});

test('setItineraryPanelViewInUrl updates the view query param', () => {
   const location = {
      href: 'https://example.test/itinerary.html',
   };
   const history = {
      replaceState(_state, _title, url) {
         location.href = url;
      },
   };

   setItineraryPanelViewInUrl('dayPlanner', { location, history });

   assert.equal(
      getItineraryPanelViewFromUrl(location),
      ITINERARY_PANEL_VIEWS.dayPlanner
   );
});
