import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryPanelView } from '../../../../scripts/itinerary/panel/components/itineraryPanelView.js';
import { ItineraryPanelViewResolver } from '../../../../scripts/itinerary/panel/itineraryPanelViewResolver.js';


test('Test_NormalizeItineraryPanelView_TestDayPlanner_ExpectDayPlanner', () => {
   const view = ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner;

   const normalized = ItineraryPanelViewResolver.normalizeItineraryPanelView(view);

   assert.equal(normalized, view);
});


test('Test_NormalizeItineraryPanelView_TestInvalid_ExpectListFallback', () => {
   const view = 'invalid';

   const normalized = ItineraryPanelViewResolver.normalizeItineraryPanelView(view);

   assert.equal(normalized, ItineraryPanelView.ITINERARY_PANEL_VIEWS.list);
});


test('Test_NormalizeItineraryPanelView_TestNull_ExpectListFallback', () => {
   const view = null;

   const normalized = ItineraryPanelViewResolver.normalizeItineraryPanelView(view);

   assert.equal(normalized, ItineraryPanelView.ITINERARY_PANEL_VIEWS.list);
});


test('Test_GetItineraryPanelViewFromUrl_TestViewQueryParam_ExpectDayPlanner', () => {
   const view = ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner;
   const location = {
      href: `https://example.test/itinerary.html?${ItineraryPanelViewResolver.ITINERARY_PANEL_VIEW_QUERY_PARAM}=${view}`,
   };

   const panelView = ItineraryPanelViewResolver.getItineraryPanelViewFromUrl(location);

   assert.equal(panelView, view);
});


test('Test_GetItineraryPanelViewFromUrl_TestNullLocation_ExpectList', () => {
   const location = null;

   const panelView = ItineraryPanelViewResolver.getItineraryPanelViewFromUrl(location);

   assert.equal(panelView, ItineraryPanelView.ITINERARY_PANEL_VIEWS.list);
});


test('Test_SetItineraryPanelViewInUrl_TestViewQueryParam_ExpectUpdated', () => {
   const view = ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner;
   const location = {
      href: 'https://example.test/itinerary.html',
   };
   const history = {
      replaceState(_state, _title, url) {
         location.href = url;
      },
   };

   ItineraryPanelViewResolver.setItineraryPanelViewInUrl(view, { location, history });

   const panelView = ItineraryPanelViewResolver.getItineraryPanelViewFromUrl(location);
   assert.equal(panelView, view);
});


test('Test_SetItineraryPanelViewInUrl_TestNullLocation_ExpectNoThrow', () => {
   const view = ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner;
   const history = {
      replaceState() {},
   };

   ItineraryPanelViewResolver.setItineraryPanelViewInUrl(view, {
      location: null,
      history,
   });

   assert.equal(view, ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner);
});


test('Test_SetItineraryPanelViewInUrl_TestMissingReplaceState_ExpectNoThrow', () => {
   const view = ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner;
   const location = {
      href: 'https://example.test/itinerary.html',
   };

   ItineraryPanelViewResolver.setItineraryPanelViewInUrl(view, {
      location,
      history: {},
   });

   assert.equal(location.href, 'https://example.test/itinerary.html');
});
