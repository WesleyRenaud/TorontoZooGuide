import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import {
   ITINERARY_PANEL_VIEWS,
   makeItineraryPanelViews,
} from '../../scripts/itinerary/panel/components/itineraryPanelViews.js';
import {
   installDocument,
   teardownDocument,
} from './helpers/domMock.mjs';

afterEach(() => {
   teardownDocument();
});

test('makeItineraryPanelViews toggles between list and day planner views', () => {
   installDocument();

   let selectedView = '';
   const {
      root,
      listView,
      dayPlannerView,
   } = makeItineraryPanelViews({
      activeView: ITINERARY_PANEL_VIEWS.list,
      onViewChange: (view) => {
         selectedView = view;
      },
   });

   const toggle = root.children.find((child) => (
      child.className === 'itin-panel-view-toggle'
   ));
   const buttons = toggle.children;

   assert.equal(buttons.length, 2);
   assert.equal(listView.hidden, false);
   assert.equal(dayPlannerView.hidden, true);

   buttons[1].listeners.click();

   assert.equal(selectedView, ITINERARY_PANEL_VIEWS.dayPlanner);
   assert.equal(listView.hidden, true);
   assert.equal(dayPlannerView.hidden, false);
});
