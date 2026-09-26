import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { ItineraryPanelView } from '../../../../../scripts/itinerary/panel/components/itineraryPanelView.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import {
   installDocument,
   teardownDocument,
} from '../../../helpers/domMock.mjs';

afterEach(() => {
   teardownDocument();
});


test('Test_MakeItineraryPanelViews_TestListActive_ExpectDayPlannerHidden', () => {
   installDocument();

   const { root, listView, dayPlannerView } = ItineraryPanelView.makeItineraryPanelViews({
      activeView: ItineraryPanelView.ITINERARY_PANEL_VIEWS.list,
      onViewChange: () => {},
   });
   const toggle = root.children.find((child) => (
      child.className === 'itin-panel-view-toggle'
   ));
   const buttons = toggle.children;

   assert.equal(
      buttons.length,
      Object.keys(ItineraryPanelView.ITINERARY_PANEL_VIEWS).length
   );
   assert.equal(listView.hidden, false);
   assert.equal(dayPlannerView.hidden, true);
});


test('Test_MakeItineraryPanelViews_TestToggleClick_ExpectDayPlanner', () => {
   installDocument();
   let selectedView = '';

   const { listView, dayPlannerView, root } = ItineraryPanelView.makeItineraryPanelViews({
      activeView: ItineraryPanelView.ITINERARY_PANEL_VIEWS.list,
      onViewChange: (view) => {
         selectedView = view;
      },
   });
   const toggle = root.children.find((child) => (
      child.className === 'itin-panel-view-toggle'
   ));
   const buttons = toggle.children;
   buttons.at(Position.SECOND).listeners.click();

   assert.equal(selectedView, ItineraryPanelView.ITINERARY_PANEL_VIEWS.dayPlanner);
   assert.equal(listView.hidden, true);
   assert.equal(dayPlannerView.hidden, false);
});
